from pymongo.mongo_client import MongoClient
from redis import Redis
from dotenv import load_dotenv
import os
load_dotenv()

# Create a new client and connect to the server
client = MongoClient(os.getenv('uri_db'))
db = client.designerBot
coll = db.users_id

redis_reg = Redis(decode_responses=True, db=0)
redis_bot = Redis(decode_responses=True, db=1)

