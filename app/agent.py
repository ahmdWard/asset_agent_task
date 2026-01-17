from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate

from fastapi import HTTPException


from langchain_classic.agents import AgentExecutor, create_react_agent ### the libirary moved after version 1 (old docs)
import re


from app.routes.crud import asset_crud
from app.config import get_settings

settings = get_settings()

class AssetAgent:
    def __init__(self, db: Session):
        self.db = db
        self.referenced_asset_ids = []
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.OPEN_API_KEY, 
            temperature=0,
            max_tokens=300 # forget to add max token causing reach limit 
        )

        self.tools = [
            Tool(
                name="search_assets",
                func=self.search_asset_tool,
                description="Useful for when you need to answer questions about what assets exist. Returns a list of asset names, values, and categories."
            ),
             Tool(
                name="get_asset_by_id",
                func=self._get_asset_by_id,
                description="""Get detailed information about a specific asset by ID.
                Use this when you have an asset ID and need full details.
                Input should be the asset ID string.
                Returns complete asset information."""
            )
        ]

        template = """Answer the following questions as best you can. You have access to the following tools:
        IMPORTANT: When referencing specific assets in your answer, always include their ID.
        {tools} Use the following format: Question: 
        the input question you must answerThought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        Begin! Question: {input}
        Thought: {agent_scratchpad}"""

        self.prompt = PromptTemplate.from_template(template)


    def _extract_asset_ids(self, text: str) -> list:
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        return re.findall(uuid_pattern, text, re.IGNORECASE)

    def search_asset_tool(self, query: str = "") -> str:
        try:
            assets = asset_crud.get_all(self.db, limit=100)
            if not assets:
                return "The database is currently empty."
            
            result = []
            for asset in assets:
                result.append(
                    f"ID: {asset.id}\n"
                    f"  Name: {asset.name}\n"
                    f"  Value: ${asset.value}\n"
                    f"  Category: {asset.category}\n"
                    f"  Status: {asset.status}\n"
                    f"  Purchase Date: {asset.purchase_date}"
                )
            return "Current Assets in Database:\n" + "\n".join(result)
        except Exception as e:
            return f"Error accessing database: {str(e)}"
        
    def _get_asset_by_id(self, asset_id: str) -> str:
        try:
            asset = asset_crud.get_by_id(self.db, asset_id.strip())
            
            if not asset:
                return f"Asset with ID {asset_id} not found."
            
            self.referenced_asset_ids.append(asset.id)
            
            return (
                f"Asset Details:\n"
                f"ID: {asset.id}\n"
                f"Name: {asset.name}\n"
                f"Category: {asset.category}\n"
                f"Value: ${asset.value}\n"
                f"Status: {asset.status}\n"
                f"Purchase Date: {asset.purchase_date}\n"
                f"Description: {asset.description or 'N/A'}\n"
                f"Created: {asset.created_at}\n"
                f"Updated: {asset.updated_at}"
            )
        
        except Exception as e:
            return f"Error getting asset: {str(e)}"
    

    def query(self, question: str) -> dict:
        """The single entry point for the API"""
        self.referenced_asset_ids = []

        try:
            agent = create_react_agent(self.llm, self.tools, self.prompt)
            
            executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=False,  ## convert it to true when you need to see the reasonoing 
                handle_parsing_errors=True,
                max_iterations=2
            )
            
            result = executor.invoke({"input": question})
            
            extracted_ids = self._extract_asset_ids(result["output"])
            if extracted_ids:
                self.referenced_asset_ids.extend(extracted_ids)
            
            unique_sources = list(set(self.referenced_asset_ids))
            
            if not unique_sources and "asset" in result["output"].lower():
                if "intermediate_steps" in result:
                    for step in result["intermediate_steps"]:
                        if len(step) >= 2:
                            tool_output = str(step[1])
                            ids = self._extract_asset_ids(tool_output)
                            unique_sources.extend(ids)
                    unique_sources = list(set(unique_sources))
            
            return {
                "answer": result["output"],
                "sources": unique_sources,
                "query_type": "success",
                "assets_found": len(unique_sources) if unique_sources else None
            }
        except HTTPException:
            raise
        except Exception as e:
            error_str = str(e).lower()

            if "rate limit" in error_str or "429" in error_str:
                raise HTTPException(
                    status_code=429,
                    detail="OpenAI rate limit reached. Please retry later."
                )

            raise HTTPException(
                status_code=500,
                detail="Internal agent error"
            )