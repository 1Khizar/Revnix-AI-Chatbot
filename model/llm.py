import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Initialize GROQ LLM
llm = ChatGroq(
    model="meta-llama/llama-guard-4-12b",
    temperature=0.3,
    max_tokens=1024,
    api_key=os.getenv("GROQ_API_KEY")
)