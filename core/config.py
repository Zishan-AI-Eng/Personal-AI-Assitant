import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm(temperature: float = 0.1):
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        groq_api_key=GROQ_API_KEY
    )