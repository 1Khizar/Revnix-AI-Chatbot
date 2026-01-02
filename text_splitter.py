from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents, chunk_size=600, chunk_overlap=200):
    """Split documents into smaller chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

