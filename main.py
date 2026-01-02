from text_loader import load_text
from text_splitter import split_documents
from vector_store import create_vector_store
from agents.agent import create_rag_agent
from utils.utils import ask


if __name__ == "__main__":
    file_name = "revnix_data.txt"
    documents = load_text(file_name)
    print("Documents loaded successfully")

    chunks = split_documents(documents)
    print("Documents split successfully")

    vector_store = create_vector_store(chunks)
    print("Vector store ready")

    agent = create_rag_agent(vector_store)
    print("Agent created successfully")

    print("\nYou can now ask questions about Revnix. Type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("Question: ").strip()
            if user_input.lower() == "exit" or not user_input:
                print("Exiting...")
                break
            answer = ask(agent, user_input)
            print("\nAnswer:", answer, "\n")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
