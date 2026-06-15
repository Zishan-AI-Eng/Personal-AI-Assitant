from core.config import get_llm
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
import json


with open("./data/profile_data.json") as f:
    my_profile = json.dumps(json.load(f), indent=2)


def process_portfolio(user_query:str, chat_history:list) ->str:

    llm=get_llm(temperature=0.1)

    system_instruction = """
    You are the official AI Assistant for Zeeshan Khan, an AI Engineer and Solution Architect.
    Base your answers strictly on this <knowledge_base>:
    
    {profile_data}
    
    CRITICAL RULES:
    1. Keep responses concise (2-4 sentences max).
    2. Maintain a highly professional and polite tone.
    3. Do not guess or hallucinate skills not mentioned in the knowledge base.
    """

    prompt=ChatPromptTemplate.from_messages(
        [('system',system_instruction),
         MessagesPlaceholder(variable_name='history'),
         ('human',{user_query})
         ]
    )

    chain = prompt |llm

    response=chain.invoke({
        'profile_data':my_profile,
        'history':chat_history,
        'user_query':user_query
    })


    return response.content