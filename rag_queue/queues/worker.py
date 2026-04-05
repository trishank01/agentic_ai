from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

openai_client = OpenAI()

# Vector Emeddings

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)






def process_queue(query:str):
    # Vector database
    vector_db = QdrantVectorStore.from_existing_collection(
      embedding=embedding_model,
      url="http://localhost:6333", 
      collection_name="learn_rag_new"
    )
    print("Searching Chunks", query)
    search_results = vector_db.similarity_search(query=query)

    content = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata.get('page_label', 'N/A')}\nFile Location: {result.metadata['source']}" for result in search_results])
    SYSTEM_PROMPT = f"""

    You are a helpfull AI Assistant who answers user query on the available content retrieved from a PDF file along with page_contents and page number.

    You should only answer the user based on the following context and navigate the user to open the right page number to know more.

    if there is no relevent answer then tell your to ask relevent question

    Context: 
    {content}
    """


    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content":SYSTEM_PROMPT},
            {"role": "user", "content":query},
        ],
    )
    print("here is your query --> ", response.choices[0].message.content)
    return response.choices[0].message.content








