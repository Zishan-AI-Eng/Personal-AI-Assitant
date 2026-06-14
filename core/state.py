from langchain_community.chat_message_histories import SQLChatMessageHistory
from core.config import DATABASE_URL


def get_session_history(session_id:str):
    """
    Manages chat histories using postgresql database (Supabase).
    creates tables if they don't exist and retrieves chat history for a given session_id.
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the environment variables.")
    
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=DATABASE_URL
    )