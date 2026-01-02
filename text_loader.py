from langchain_community.document_loaders import TextLoader

def load_text(file_name: str):
    """Load documents from a text file."""
    loader = TextLoader(
        file_name,
        encoding="utf-8",
        autodetect_encoding=True
    )
    return loader.load()
