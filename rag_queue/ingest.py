from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# 👉 Load PDF
loader = PyPDFLoader("UIDAI.pdf")
docs = loader.load()

# 👉 Split (smaller = avoids timeout)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

documents = splitter.split_documents(docs)

# 👉 (optional) limit for safety
documents = documents[:50]

# 👉 Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# 👉 Store in Qdrant
QdrantVectorStore.from_documents(
    documents,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learn_rag_new",
    timeout=120  # ✅ important
)

print("✅ Ingestion complete")