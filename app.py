from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import uvicorn

# Import your existing modules
from text_loader import load_text
from text_splitter import split_documents
from vector_store import create_vector_store
from agents.agent import create_rag_agent
from utils.utils import ask

app = FastAPI(title="Revnix Chatbot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global agent variable
agent = None

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    status: str

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG agent on startup"""
    global agent
    try:
        print("Loading documents...")
        file_name = "revnix_data.txt"
        documents = load_text(file_name)
        
        print("Splitting documents...")
        chunks = split_documents(documents)
        
        print("Creating vector store...")
        vector_store = create_vector_store(chunks)
        
        print("Creating agent...")
        agent = create_rag_agent(vector_store)
        
        print("✓ Revnix Chatbot is ready!")
    except Exception as e:
        print(f"Error during startup: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    html_path = Path("templates/index.html")
    if html_path.exists():
        return html_path.read_text()
    return "<h1>Template not found</h1>"

@app.post("/api/chat", response_model=QuestionResponse)
async def chat(request: QuestionRequest):
    """Handle chat requests"""
    global agent
    
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        answer = ask(agent, request.question)
        return QuestionResponse(answer=answer, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_ready": agent is not None
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)