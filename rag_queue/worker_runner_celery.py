"""
Celery-based worker for RAG queue system.
This is a cross-platform alternative to RQ that works on Windows, Linux, and Mac.

To use this:
1. Install Celery: pip install celery
2. Start Redis (already running via Docker)
3. Start worker: celery -A worker_runner_celery worker --loglevel=info
4. Start beat (for scheduled tasks): celery -A worker_runner_celery beat --loglevel=info
"""

from dotenv import load_dotenv
from celery import Celery
from celery.signals import task_postrun
import os

load_dotenv()

# Create Celery app
app = Celery(
    'rag_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',  # Store results in Redis
    include=['worker_runner_celery']
)

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes timeout
    worker_prefetch_multiplier=1,  # Process one task at a time
)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_queue(self, query: str):
    """
    Process a RAG query using Celery.
    
    Args:
        query: The user's query string
        
    Returns:
        The AI-generated response
    """
    from langchain_openai import OpenAIEmbeddings
    from langchain_qdrant import QdrantVectorStore
    from openai import OpenAI
    
    # Update task state to show it's started
    self.update_state(state='STARTED', meta={'progress': 'Loading embeddings...'})
    
    # Initialize models
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
    openai_client = OpenAI()
    
    try:
        self.update_state(state='STARTED', meta={'progress': 'Searching vector database...'})
        
        # Vector database
        vector_db = QdrantVectorStore.from_existing_collection(
            embedding=embedding_model,
            url="http://localhost:6333",
            collection_name="learn_rag_new"
        )
        
        print(f"Searching Chunks: {query}")
        search_results = vector_db.similarity_search(query=query)
        
        content = "\n\n\n".join([
            f"Page Content: {result.page_content}\n"
            f"Page Number: {result.metadata.get('page_label', 'N/A')}\n"
            f"File Location: {result.metadata['source']}"
            for result in search_results
        ])
        
        SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers user queries on the available content 
retrieved from a PDF file along with page contents and page number.

You should only answer the user based on the following context and navigate 
the user to open the right page number to know more.

If there is no relevant answer then tell the user to ask a relevant question.

Context:
{content}
"""
        
        self.update_state(state='STARTED', meta={'progress': 'Generating response with AI...'})
        
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
        )
        
        result = response.choices[0].message.content
        print(f"Query result: {result}")
        
        return result
        
    except Exception as exc:
        print(f"Task failed: {exc}")
        # Retry the task
        raise self.retry(exc=exc)


# Optional: Scheduled task example (runs every hour)
@app.task
def cleanup_old_jobs():
    """Example scheduled task to clean up old data."""
    print("Running cleanup task...")
    # Add cleanup logic here
    return "Cleanup completed"


# Celery Beat schedule (for periodic tasks)
app.conf.beat_schedule = {
    'cleanup-every-hour': {
        'task': 'worker_runner_celery.cleanup_old_jobs',
        'schedule': 3600.0,  # Every hour
    },
}


if __name__ == '__main__':
    print("Celery worker configuration loaded.")
    print("To start the worker, run:")
    print("  celery -A worker_runner_celery worker --loglevel=info -P solo")
    print("")
    print("For Windows, use '-P solo' or '-P threads' to avoid fork issues:")
    print("  celery -A worker_runner_celery worker --loglevel=info -P solo")
