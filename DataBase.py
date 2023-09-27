from pymongo.mongo_client import MongoClient
from redis import Redis
from dotenv import load_dotenv
import os
load_dotenv()

# Create new client and connect to the server
client = MongoClient(os.getenv('uri_db'))
db = client.designerBot
coll = db.users_id

redis_reg = Redis(db=0, decode_responses=True)
redis_bot = Redis(db=1, decode_responses=True)

