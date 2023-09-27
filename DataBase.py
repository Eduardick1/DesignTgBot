from pymongo.mongo_client import MongoClient
from redis import Redis
from dotenv import load_dotenv
import os
load_dotenv()

# Create new client and connect to the server
client = MongoClient(os.getenv('uri_db'))
db = client.designerBot
coll = db.users_id

redis_reg = Redis(host="containers-us-west-185.railway.app", password="Dz459YIDQ0Z8rZYp3FAj", port=5812, username='default', db=0, decode_responses=True)
redis_bot = Redis(host="containers-us-west-185.railway.app", password="Dz459YIDQ0Z8rZYp3FAj", port=5812, username='default', db=1, decode_responses=True)

