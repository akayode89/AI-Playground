"""
Create a simple assistant that uses any LLM and should be pydantic, 
when we ask about any product it should give you two information product Name, 
product details tentative price in USD (integer). use chat Prompt Template.
"""
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser



# Setting environment variables
os.environ["OPENAI_API_KEY"]==os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"]==os.getenv("LANGCHAIN_API_KEY")
os.environ["GROQ_API_KEY"]==os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_PROJECT"]==os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"

# Get model
model = ChatOpenAI(model='o1-mini')


class Product(BaseModel):
    product_description: str = Field(description="Details description of the product")
    product_price: str = Field(description="The price of the product")

#@st.cache
def get_product_details(query):
    parser = JsonOutputParser(pydantic_object=Product)

    # Prompt Template
    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    response = chain.invoke({"query": query})

    return response

# UI Definition
def product_input():
    st.title("Product Search Engine")
    return st.text_input("Enter a product name:")

if __name__=="__main__":
    user_input = product_input()
    if user_input:
        product_search = get_product_details(user_input)
        st.write(product_search)

if __name__ == "__main__":
    user_input = product_input()
    if user_input:
        product_search = get_product_details(user_input)

        # Ensure product_search contains valid data before rendering
        if isinstance(product_search, dict):  # Assuming response is a dict
            st.write(product_search)
        else:
            st.error("Invalid product details retrieved.")
