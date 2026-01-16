from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from app.config import get_settings


settings = get_settings()


class AssetAgent:

    def __init__(self,db: Session):
        self.db =db

        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            api_key=settings.OPEN_API_KEY,
            temperature=0
        )

    def query(self, question: str) -> dict:
        """Process a question """
        try:
            response = self.llm.invoke(question)
            
            return {
                "answer": response.content,
                "query_type": "simple_llm",
                "sources": []
            }
        except Exception as e:
            return {
                "answer": f"Error: {str(e)}",
                "query_type": "error",
                "sources": []
            }
