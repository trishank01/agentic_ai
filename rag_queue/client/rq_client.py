# from redis import Redis
# from rq import Queue
# conn = Redis(host="localhost", port=6379)

# queue = Queue(connection=Redis(
#      host="localhost",
#      port="6379"
# ))

# # ✅ Correct check
# print(conn.ping())

from redis import Redis
from rq import Queue

conn = Redis(host="localhost", port=6379)

queue = Queue(connection=conn)