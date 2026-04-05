from fastapi import FastAPI, Query
from client.rq_client import queue
from queues.worker import process_queue


app = FastAPI()


@app.get('/')
def root():
    return {"status": "Server is up and running"}


@app.post('/chat')
def chat(
    query:str = Query(..., description="The chat query of user")
):
    job = queue.enqueue(process_queue, query)
    return {"status": "queued", "job_id": job.id}

@app.get("/job-status")
def get_result(
    job_id : str = Query(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    if not job:
        return {"status": "error", "message": "Job not found"}
    
    return {
        "job_id": job.id,
        "status": job.get_status(),
        "result": job.result
    }


