# import os
# from dotenv import load_dotenv
# load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from config import Idea, Data, idea_prompt, data_prompt

class Model(object):
    def __init__(self) -> None:
        self.llm = ChatGroq(
            temperature=0.8, # confidence of model
            model="llama-3.1-8b-instant",
            # api_key=os.getenv("GROQ_API_KEY")
            api_key=st.secrets["GROQ_API_KEY"]
        )

    def generate_content(self, category: str, idea: str):
        # Chain Initialization (Resources not allocated)
        sequential_idea_chain = idea_prompt | self.llm.with_structured_output(Idea)
        sequential_data_chain = data_prompt | self.llm.with_structured_output(Data)
        try:
            idea_dict = {"category": category, "idea": idea}
            # Running State
            business_name = sequential_idea_chain.invoke(idea_dict)
            # Pipelining
            data_dict = {"category": category, "name": business_name.name}
            response = sequential_data_chain.invoke(data_dict)
            return response, business_name
        except:
            return "Error"
        
if __name__ == "__main__":
    print(f"Welcome user")
    idea: str = input("Enter a business idea: ")
    category: str = input("Enter category: ")
    model = Model()
    response = model.generate_content(category=category, idea=idea)
    print(response)