import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def get_llm(temperature: float = 0.1):
    """
    Initializes and returns the primary LLM instance.

    """
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
    )



