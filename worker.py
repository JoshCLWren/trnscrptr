import os
import urllib.parse as urlparse
from redis import Redis
from rq import Queue, Connection

if os.environ.get("env", "development") != "development" or os.environ.get("env") is False:
    from rq import Queue, Connection
    from rq.worker import HerokuWorker as Worker
else:
    from rq import Worker, Queue, Connection

listen = ["high", "default", "low"]


redis_url = os.getenv("REDISTOGO_URL")
if not redis_url:
    raise RuntimeError("Set up Redis To Go first.")

urlparse.uses_netloc.append("redis")
url = urlparse.urlparse(redis_url)
conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
