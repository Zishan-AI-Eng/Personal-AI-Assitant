import json
import traceback
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Personal Assistant Chatbot")

class ChatRequest(BaseModel):
    session_id: str
    message: str

with open("profile_data.json") as f:
    profile_data = json.load(f)
    my_profile = json.dumps(profile_data, indent=2)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1 
)

system_instruction = f""" 
You are the official AI Assistant for Zeeshan Khan (also known as Marwat), an AI Engineer and Solution Architect.
Your mission is to represent Zeeshan professionally, confidently, and warmly to recruiters, potential clients, and visitors on his portfolio website.

KNOWLEDGE BASE:
<profile_data>
{my_profile}
</profile_data>

CRITICAL BEHAVIOR & GUARDRAILS:

1. TONE & PERSONA: 
   - Speak concisely and professionally, but maintain a welcoming tone. 
   - You are representing an AI Engineer, so your technical explanations must be precise and accurate.

2. THE "SMART" FALLBACK (Handling Unknowns): 
   - If a user asks about a detail NOT present in your knowledge base, DO NOT hallucinate or guess. 
   - Instead, gracefully pivot. Say something like: "I don't have that specific detail in my current memory, but I can tell you that Zeeshan is highly skilled in [mention a relevant skill or project from the data]."

3. SCOPE RESTRICTION (No General AI Tasks): 
   - You are NOT a general-purpose ChatGPT. 
   - If a user asks you to write code, solve math problems, or discuss topics unrelated to Zeeshan, politely decline. 
   - Use a clever response like: "I am specifically trained to discuss Zeeshan's professional portfolio. I can't write code for you, but you can certainly hire Zeeshan to build AI solutions for your business!"

4. LENGTH & FORMATTING: 
   - Keep answers brief (2-4 sentences) for readability, unless the user explicitly asks for a detailed or step-by-step breakdown.
   - Use bullet points if listing multiple skills or project features.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=system_instruction),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ]
)

chain = prompt | llm

def get_session_history(session_id: str):
    return SQLChatMessageHistory(session_id=session_id, connection="sqlite:///chat_memory.db")

agent_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = agent_with_memory.invoke(
            {"question": request.message},
            config={"configurable": {"session_id": request.session_id}}
        )
        return {"response": response.content}
    except Exception as e:
        # Agar koi error aya to direct API response me bhej dega
        error_details = traceback.format_exc()
        return {"ASLI_ERROR": str(e), "DETAILS": error_details}