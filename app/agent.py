from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate

from langchain_classic.agents import AgentExecutor, create_react_agent ### the libirary moved after version 1 (old docs)

from app.routes.crud import asset_crud
from app.config import get_settings

settings = get_settings()

class AssetAgent:
    def __init__(self, db: Session):
        self.db = db
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.OPEN_API_KEY, 
            temperature=0,
        )

        self.tools = [
            Tool(
                name="search_assets",
                func=self.search_asset_tool,
                description="Useful for when you need to answer questions about what assets exist. Returns a list of asset names, values, and categories."
            )
        ]

        template = """Answer the following questions as best you can. You have access to the following tools:
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

    def search_asset_tool(self, query: str = "") -> str:
        try:
            assets = asset_crud.get_all(self.db, limit=100)
            if not assets:
                return "The database is currently empty."
            
            data = [f"- {a.name}: ${a.value} ({a.category})" for a in assets]
            return "Current Assets in Database:\n" + "\n".join(data)
        except Exception as e:
            return f"Error accessing database: {str(e)}"

    def query(self, question: str) -> dict:
        """The single entry point for the API"""
        try:
            agent = create_react_agent(self.llm, self.tools, self.prompt)
            
            executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True, 
                handle_parsing_errors=True,
                max_iterations=5
            )
            
            result = executor.invoke({"input": question})
            
            return {
                "answer": result["output"],
                "query_type": "react_agent",
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"Agent Error: {str(e)}",
                "query_type": "error",
                "success": False
            }