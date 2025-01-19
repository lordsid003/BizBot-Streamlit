from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List

# Business Chatbot: Idea -> Taglines, Advertisement Info, Available web domains, marketing schemes and competitors
idea_prompt = PromptTemplate(
    input_variables=["category", "idea"],
    template=
    """
        You are a business counsellor for {category}. Generate organization names for this business idea: {idea}
    """,
    validate_template=True
)

# Pipelining: User -> Sequential Chain -> Output -> Sequential Chain (before response generation)
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

class Idea(BaseModel):
    name: str = Field("Business Name:")

class Data(BaseModel):
    taglines: List[str] = Field("List of taglines:")
    domains: List[str] = Field("List of web domains:")
    strats: List[str] = Field("List of marketing strategies:")
    comp: List[str] = Field("List of competitors:")