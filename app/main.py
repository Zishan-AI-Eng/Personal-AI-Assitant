import json
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChaTMessageHistory
from dotenv import load_dotenv

load_dotenv()



app=FastAPI(title="Personal Assistant Chatbot")

class ChatRequest(BaseModel):
    session_id: str
    message: str




with open("profile_data.json") as f:
    profile_data = json.load(f)
    my_profile = json.dumps(profile_data,indent=2)



llm=ChatGroq(
    model="llama3-70b-8192",
    temperature=0.1,    
)


system_instruction = f""" 
                    You are Zeeshan Khan's Personal AI Assistant embedded in his potfolio website.
                    You job is only to answer the questions about Zeeshan based on the following json
                    profile data :
                    {profile_data}
                    {my_profile}
                    </profile_data>

                    Rules:
                    1. If the user asks about Zeeshan's skills, experience, education, or projects, answer concisely and professionally using ONLY the data above.
                    2. If the user asks you to write code, do unrelated math, or asks about anything OUTSIDE of Zeeshan's profile, politely decline and steer the conversation back to Zeeshan's professional capabilities.
                    3. Keep answers relatively short (under 3-4 sentences) unless the user asks for detailed information.
                    """



prompt=ChatPromptTemplate.from_messages(
    [
        ("system", system_instruction),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ]

)


chain= prompt |llm


def get_session_history(session_id: str):
    return SQLChaTMessageHistory(session_id,"sqlite://chat_memory.db")


agent_with_memory=RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)


@app.post("/chat")
async def chat(request:ChatRequest):

    response=agent_with_memory.invoke(
        {"question":request.message},
         config={"configurable ":  {"session_id": request.session_id}}
    )

    return {"response": response.content}