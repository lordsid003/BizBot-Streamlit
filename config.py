from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class Name(BaseModel):
    name: str = Field(description="Name of business:")

class Data(BaseModel):
    taglines: List[str] = Field(description="List of taglines")
    domains: List[str] = Field(description="List of web domains")
    strategies: List[str] = Field(description="List of marketing strategies")
    competitors: List[str] = Field(description="List of market competitors")

class SequenceChain(BaseModel):
    name: Name
    data: Data