from typing import List
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def get_embedding_engine(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(model_name=model_name)


def build_spec_vectorstore(documents: List[Document], persist_dir: str = "./.chroma_db") -> Chroma:
    """Indexes document chunks into ChromaDB."""
    embeddings = get_embedding_engine()
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    return vectorstore
