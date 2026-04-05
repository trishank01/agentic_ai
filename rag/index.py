from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()


pdf_path = Path(__file__).parent / 'UIDAI.pdf'


# Load this file in python program

loader = PyPDFLoader(file_path=pdf_path)

docs = loader.load()

# print(docs[12])


# split the docs into smaller chunks

# split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # Size of each chunk
    chunk_overlap=200,  # Overlap between chunks to keep context
    add_start_index=True # Good for tracking where chunks came from

)

chunks = text_splitter.split_documents(documents=docs)

print(f"Split {len(docs)} documents into {len(chunks)} chunks.")


# Vector Emeddings

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333", 
    collection_name="learning_rag"
)

print(vector_store)