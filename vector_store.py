import os
from uuid import uuid4
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from embeddings import embeddings

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing in .env")

def create_vector_store(chunks):
    """Create or connect to a Pinecone vector store and add document chunks."""
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "revnix-chatbot-index"

    # Create index if it doesn't exist
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec={"serverless": {"cloud": "aws", "region": PINECONE_ENV}}
        )

    # Connect to index
    index = pc.Index(index_name)
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    # Add documents only if empty
    stats = index.describe_index_stats()
    if stats["total_vector_count"] == 0:
        uuids = [str(uuid4()) for _ in chunks]
        vector_store.add_documents(documents=chunks, ids=uuids)

    return vector_store

def get_retriever(vector_store, k=3):
    return vector_store.as_retriever(search_kwargs={"k": k})
