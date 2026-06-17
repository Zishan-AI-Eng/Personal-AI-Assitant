from core.config import get_llm
from langchain_core.prompts import ChatPromptTemplate


def process_greeting(user_query: str) -> str:
    """Handles small talk and steers the conversation to Zeeshan's portfolio."""
    llm = get_llm(temperature=0.3) # Thori si creativity allow karte hain

    system_instruction = """
    You are the polite and welcoming AI Assistant for Zeeshan Khan, an AI Engineer.
    The user has just greeted you or made small talk. 
    
    Rule 1: Briefly and warmly respond to their greeting.
    Rule 2: Immediately pivot and ask if they would like to know about Zeeshan's AI projects, his LangGraph experience, or his work in Agentic AI.
    Rule 3: Keep it under 2 sentences.
    """

    prompt = ChatPromptTemplate.from_messages([
        ('system', system_instruction),
        ('human', '{user_query}')
    ])

    chain = prompt | llm
    response = chain.invoke({'user_query': user_query})
    
    return response.content