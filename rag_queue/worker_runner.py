from redis import Redis
from rq import Queue
from rq.job import Job
import time
from queues.worker import process_queue

conn = Redis(host="localhost", port=6379)
queue = Queue(connection=conn)

print("🚀 Worker started...")
print("Listening for jobs...")

while True:
    # Get job ID from queue
    try:
        job_id = queue.pop_job_id()
    except:
        job_id = None
    
    if job_id:
        job = Job.fetch(job_id, connection=conn)
        print(f"Processing job {job.id}: {job.args}")
        try:
            # Execute the job function directly
            result = process_queue(*job.args, **job.kwargs)
            # Save result back to job using RQ's API
            job.save_meta()
            job._result = result
            job._status = 'finished'
            job.save()
            print(f"Job {job.id} completed successfully.")
        except Exception as e:
            print(f"Job {job.id} failed: {e}")
            job._exc_info = str(e)
            job._status = 'failed'
            job.save()
    else:
        time.sleep(1)
