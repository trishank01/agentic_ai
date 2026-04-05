from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()
openai_client = OpenAI()




# Vector Emeddings

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
      embedding=embedding_model,
      url="http://localhost:6333", 
      collection_name="learning_rag"
)

# Take user input

user_query = input("Ask something: ")

# Relevnet chunks from the vector db

search_results = vector_db.similarity_search(query=user_query)

content = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])


SYSTEM_PROMOT = F"""

You are a helpfull AI Assistant who answers user query on the available content retrieved from a PDF file along with page_contents and page number.

You should only answer the user based on the following context and navigate the user to open the right page number to know more.


Context: 
{content}
"""


res = openai_client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content":SYSTEM_PROMOT},
         {"role": "user", "content":user_query}

    ]
)


# Relevent chunks from the vector db
print("here is your query --> ", res.choices[0].message.content)