import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from config import Name, Data, SequenceChain

# Load .env variables
load_dotenv()

# UI and Interfaces
st.title("BizBot: AI Business IdeaMaker")
st.subheader("Business Idea Generator")
category: str = st.sidebar.selectbox("Select a business category", (
    "Food & Beverage",
    "Clothing & Apparals",
    "Healthcare & Fitness", 
    "Education",
    "Social Impact",
    "Environmental Impact",
    "Technology & Hardware",
    "Others"
))
idea = st.text_input(label="Business Canvas", placeholder="Explore business ideas...", max_chars=200)
display_items = ["Brand Name", "Taglines", "Web Domains", "Marketing Strategies", "Competitors"]

# LLM config
llm = ChatGroq(
    temperature=0.6,
    model="llama3-70b-8192",
    api_key=os.getenv("LLAMA_API_KEY")
)

name_prompt = PromptTemplate(
    input_variables=["idea", "category"],
    template=
        """
            You are a business counsellor for {category}. Generate organization names for this business idea: {idea}
        """,
    validate_template=True
)

data_prompt = PromptTemplate(
    input_variables=["name", "category"],
    template=
        """
            Based on the business name: {name} for this industry: {category}, provide a detailed data with the following sections:\n"
            Business Taglines:\n
            - List of taglines\n
            Web Domains:\n
            - List of web domains\n  
            Marketing strategies:\n
            - List of marketing strategies\n
            Competitors:\n
            - List of market competitors\n
            Generate exactly 4 items in each category
        """,
        validate_template=True
)

# Sequential chaining 
name_sequence = name_prompt | llm.with_structured_output(Name)

def chain(idea: str, category: str):
    formatted_name_prompt = {"idea": idea, "category": category}
    name_response = name_sequence.invoke(formatted_name_prompt)
    business_name = Name(name=name_response.name)
    formatted_data_prompt = {"name": business_name.name, "category": category}
    # Sequential chaining with multiple input-output nodes
    data_response = (data_prompt | llm.with_structured_output(Data)).invoke(formatted_data_prompt)
    result = SequenceChain(
        name=business_name,
        data=data_response
    )
    return result

def handlePress():
    if category and idea != "":
        result = chain(idea, category)
        st.header("# " + result.name.name)

        st.subheader("Taglines")
        for taglines in result.data.taglines:
            st.write("- " + taglines)

        st.subheader("Web Domains")
        for domains in result.data.domains:
            st.write("- " + domains)

        st.subheader("Marketing Strategies")
        for strategies in result.data.strategies:
            st.write("- " + strategies)

        st.subheader("Competitors")
        for competitors in result.data.competitors:
            st.write("- " + competitors)
        
    elif idea == "":
        for item in display_items:
            st.subheader(item)
            st.write("- Generates " + item.lower())
    else:
        pass

st.button(label="Generate", on_click=handlePress())