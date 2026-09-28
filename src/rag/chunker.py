from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_spec_document(text: str, chunk_size: int = 1200, chunk_overlap: int = 150) -> List[Document]:
    """Splits specifications into chunks while preserving table boundaries."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n[TABLE_START]", "\n\n", "\n", " "]
    )
    docs = splitter.create_documents([text])
    return docs
