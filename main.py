import logging
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from agents.router_agent import route_query
from agents.portfolio_agent import process_portfolio
from core.state import get_session_history
from agents.reject_agent import process_reject


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



app=FastAPI(
    title='AI Portfolio Assistant'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    session_id: str
    user_query: str
    chat_history: Optional[list] = []



@app.post("/chat")
def chat_endpoint(request:ChatRequest):
    try:
        logger.info(f"Incoming request: {request}")

        route=route_query(request.user_query)
        logger.info(f"Session:{request.session_id} routed to: {route}")

        if route=="Portfolio":
            history_instance=get_session_history(request.session_id)
            chat_history=history_instance.get_messages()

            response_content=process_portfolio(request.user_query,chat_history)

            history_instance.add_user_message(request.user_query)
            history_instance.add_ai_message(response_content)
        

        else:
            response_content=process_reject(request.user_query)

        return {"response":response_content}
    
    except Exception as e:
        logger.error(f"Error in chat endpoint for session {request.session_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.")