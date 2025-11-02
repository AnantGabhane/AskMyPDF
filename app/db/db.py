#establish connection with db
from .client import mongo_client

database = mongo_client["mydb"]