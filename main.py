import logging
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from typing import Optional
from agents.greeting_agent import process_greeting


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
    session_id: Optional[str] = "default-session"
    user_query: str = Field(..., min_length=1) 
    chat_history: Optional[list] = [] 



@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Session {request.session_id} received query: {request.user_query}")

        # 2. Routing logic
        route = route_query(request.user_query)
        
        if route == "Portfolio":
            history_instance = get_session_history(request.session_id)
           
            chat_history = history_instance.get_messages() 

            response_content = process_portfolio(request.user_query, chat_history)

           
            history_instance.add_user_message(request.user_query)
            history_instance.add_ai_message(response_content)

        elif route == "Greeting":
            response_content = process_greeting(request.user_query)

            history_instance = get_session_history(request.session_id)
            history_instance.add_user_message(request.user_query)
            history_instance.add_ai_message(response_content)

            
        else:
            response_content = process_reject(request.user_query)

        return {"response": response_content}
    
    except Exception as e:
        logger.error(f"Critical error in session {request.session_id}: {str(e)}", exc_info=True)
        
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")