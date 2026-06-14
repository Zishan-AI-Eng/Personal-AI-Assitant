from pydantic import BaseModel,Field
from langchain_core.prompts import ChatPromptTemplate
from typing import Literal
from core.config import get_llm


class RouterDecision(BaseModel):
        
        route:Literal['Portfolio','Reject']=Field(
        description="The destination route based on user intent."
        )



def route_query(user_query:str) ->str:
        
        llm=get_llm(temperature=0.0)

        structured_llm=llm.with_structured_output(RouterDecision)

        system_prompt = """You are a Semantic Router for Zeeshan Khan's AI Portfolio Assistant.
    Analyze the user's input and classify it into one of two routes:
    
    1. 'PORTFOLIO': If the user asks about Zeeshan's skills, resume, projects, experience, education, or how to contact him.
    2. 'REJECT': If the user asks to write code/scripts, solve math/logic problems, write essays, or asks about general world trivia.
    
    Base your decision strictly on the user's intent."""
        
        prompt=ChatPromptTemplate.from_messages(
                [("system", system_prompt),
                 ("human", user_query)]
        )

        chain = prompt | structured_llm

        try:
            result= chain.invoke({'user_query': user_query})
            return result.route
        
        except Exception as e:
               return "REJECT"

