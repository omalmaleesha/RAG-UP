from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from services.vectorstore import VectorStoreService


def main():
    # Load PDF
    loader = PyPDFLoader("data/example.pdf")
    docs = loader.load()

    print(f"Loaded {len(docs)} pages from PDF.")

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )

    chunks = splitter.split_documents(docs)

    print(f"Created {len(chunks)} chunks.")

    # Initialize vector store
    vector_db = VectorStoreService()

    # Clear old documents first
    vector_db.reset()

    # Add new chunks
    vector_db.add_documents(chunks)

    print(f"Inserted {len(chunks)} chunks into vector DB.")

    # Check whether documents exist
    vector_db.has_documents()


if __name__ == "__main__":
    main()
    
    
    
    
# Documents upload need to be done by a UI or need method to
# find what is the data and what is the type