from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from services.vectorstore import VectorStoreService


def main():
    loader = TextLoader("data/university.txt", encoding="utf-8")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(docs)
    vector_db = VectorStoreService()

    # Optional: clear old documents first
    vector_db.db.reset_collection()
    vector_db.db.add_documents(chunks)
    print(f"Inserted {len(chunks)} chunks.")


if __name__ == "__main__":
    main()