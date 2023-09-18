from pymongo.mongo_client import MongoClient
from aioredis import Redis
#from aiogram.fsm.storage.redis import RedisStorage
uri = "mongodb+srv://design:12345678q@designerandrewdb.atq3pav.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
db = client.designerBot
coll = db.users_id

redis = Redis(decode_responses=True)


#print(coll.update_one({'_id': 563423},{"$set" : {'name': "ElinnuskA"}}))

#print(coll.find_one({'_id': 563423})['tokenpix'])