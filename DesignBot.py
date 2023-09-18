
from createBot import dp, bot
from commands import command_router
from parserdesign import parse_router
from messageHandlers import spam_router
from middlewares import DataBaseMiddleWare
from DataBase import client, redis
import asyncio


async def main():
    #await redis.flushall()
    dp.update.middleware.register(DataBaseMiddleWare())
    dp.include_routers(parse_router, command_router, spam_router)
    await dp.start_polling(bot) 

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    try:
        redis.ping()
        print("Redis connected!")
    except Exception as e:
        print(e)
except Exception as e:
    print(e)
    pass
asyncio.run(main())




