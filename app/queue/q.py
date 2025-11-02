from redis import Redis
from rq import Queue
import os

# Get Redis connection details from environment variables with fallbacks
REDIS_HOST = os.getenv("REDIS_HOST", "valkey")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_connection = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT
)

q = Queue(connection=redis_connection)