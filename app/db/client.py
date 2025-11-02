# mongo db client to establish connection with server
from pymongo import AsyncMongoClient
import os
import subprocess

# Get MongoDB connection string from environment variable with fallback
# Determine the host gateway IP dynamically for dev container environments
def get_host_gateway():
    """Get the Docker host gateway IP address"""
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True,
            text=True,
            check=True
        )
        # Parse output like: "default via 172.26.0.1 dev eth0"
        gateway = result.stdout.split()[2]
        return gateway
    except Exception:
        # Fallback to common Docker gateway or localhost
        return "172.17.0.1"

# Try to use environment variable first, otherwise construct from gateway
MONGO_HOST = os.getenv("MONGO_HOST", get_host_gateway())
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASS", "admin")

MONGO_URI = os.getenv("MONGO_URI", f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}")

mongo_client: AsyncMongoClient = AsyncMongoClient(MONGO_URI)