from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()


class LLMService:

    def __init__(self):

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("MODEL_NAME"),
            temperature=0
        )

    def get_llm(self):

        return self.llm