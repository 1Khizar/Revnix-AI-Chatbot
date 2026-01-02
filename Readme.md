# Revnix AI Chatbot - RAG System 🤖

A production-ready Retrieval-Augmented Generation (RAG) chatbot built with LangChain, FastAPI, and Pinecone. This intelligent assistant provides accurate, context-aware responses about Revnix Technologies and its products.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)](https://www.langchain.com/)

## 🌟 Features

- **Intelligent Document Processing**: Automated web scraping and content extraction
- **Semantic Search**: Vector-based retrieval using Pinecone
- **LLM-Powered Responses**: Groq's LLama 3.3 70B for accurate answers
- **RESTful API**: FastAPI backend with CORS support
- **Web Interface**: Clean, responsive chat UI
- **Real-time Responses**: Instant query processing
- **Context-Aware**: Maintains conversation context for better accuracy

## 🏗️ Architecture

```
┌─────────────────┐
│   Web Scraper   │ → Collects data from revnix.com
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Splitter  │ → Chunks documents (600 chars, 200 overlap)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Embeddings    │ → HuggingFace (all-MiniLM-L6-v2)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pinecone Store  │ → Vector database (384 dimensions)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   RAG Agent     │ → LangChain + Groq LLama 3.3
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Server │ → REST API endpoints
└─────────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- Pinecone account and API key
- Groq API key
- Cohere API key (optional)

## 🚀 Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd revnix-chatbot
```

1. **Create virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

1. **Set up environment variables**

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=us-east-1
```

## 📦 Project Structure

```
revnix-chatbot/
│
├── agents/
│   ├── __init__.py
│   └── agent.py              # RAG agent creation
│
├── model/
│   └── llm.py                # LLM configuration
│
├── prompt/
│   └── system_prompt.py      # System prompts
│
├── tools/
│   └── retriever_tool.py     # Vector retrieval tool
│
├── utils/
│   └── utils.py              # Helper functions
│
├── static/                   # Frontend assets
├── templates/                # HTML templates
│
├── app.py                    # FastAPI application
├── main.py                   # CLI interface
├── scraper.py                # Web scraping utility
├── text_loader.py            # Document loader
├── text_splitter.py          # Text chunking
├── vector_store.py           # Pinecone integration
├── embeddings.py             # Embedding model
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🎯 Usage

### Web Scraping (First Time Setup)

Scrape Revnix website data:

```bash
python scraper.py
```

This creates `revnix_data.txt` with all website content.

### CLI Interface

Run the chatbot in terminal:

```bash
python main.py
```

Example interaction:

```
Question: What services does Revnix offer?
Answer: Revnix offers specialized technology solutions including...
```

### Web Application

Start the FastAPI server:

```bash
python app.py
```

Or with uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Access the web interface at: `http://localhost:8000`

### API Endpoints

#### Chat Endpoint

```bash
POST /api/chat
Content-Type: application/json

{
  "question": "What is Revnix?"
}

Response:
{
  "answer": "Revnix is a tech company...",
  "status": "success"
}
```

#### Health Check

```bash
GET /api/health

Response:
{
  "status": "healthy",
  "agent_ready": true
}
```

## 🔧 Configuration

### Embeddings Model

Current: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)

To change the model, edit `embeddings.py`:

```python
embeddings = HuggingFaceEmbeddings(
    model_name="your-model-name"
)
```

### LLM Model

Current: `llama-3.3-70b-versatile` (Groq)

To change, edit `agents/agent.py`:

```python
llm = ChatGroq(model="your-model-name")
```

### Chunk Size

Modify in `text_splitter.py`:

```python
def split_documents(documents, chunk_size=600, chunk_overlap=200):
    # Adjust these values based on your needs
```

### Retrieval Settings

Change number of retrieved documents in `vector_store.py`:

```python
def get_retriever(vector_store, k=3):  # k = number of chunks
```


## 🚀 Deployment

### Docker (Recommended)

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t revnix-chatbot .
docker run -p 8000:8000 --env-file .env revnix-chatbot
```

### Cloud Platforms

- **Heroku**: Use Procfile
- **AWS**: Deploy on EC2 or ECS
- **Google Cloud**: Use Cloud Run
- **Railway**: Direct deployment from Git

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Framework | FastAPI |
| LLM | Groq (LLama 3.3 70B) |
| Embeddings | HuggingFace Transformers |
| Vector DB | Pinecone |
| Agent Framework | LangChain |
| Web Scraping | BeautifulSoup4 |
| HTTP Client | Requests |

## 📈 Future Enhancements

- [ ] Add conversation memory
- [ ] Implement user authentication
- [ ] Add streaming responses
- [ ] Multi-language support
- [ ] Chat history persistence
- [ ] Advanced analytics dashboard
- [ ] Voice input/output
- [ ] Mobile app integration

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Khizar Ishtiaq**

- GitHub: [@your-github-username]
- LinkedIn: [Your LinkedIn Profile]
- Email: <your.email@example.com>

## 🙏 Acknowledgments

- Revnix Technologies for the use case
- LangChain for the RAG framework
- Groq for lightning-fast LLM inference
- Pinecone for vector database infrastructure
- HuggingFace for embedding models

## 📞 Support

For issues and questions:

- Open an issue on GitHub
- Contact: <your.email@example.com>

---

⭐ If you find this project useful, please consider giving it a star!

**Built by Khizar Ishtiaq**
