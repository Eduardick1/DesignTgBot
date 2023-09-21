from middlewares import RedisterCheckMiddleWare
from createBot import dp, bot
from commands import command_router
from parserdesign import parse_router
from messageHandlers import spam_router
from DataBase import client, redis_reg, redis_bot
import asyncio


async def main():
    dp.message.middleware.register(RedisterCheckMiddleWare())
    dp.include_routers(parse_router, command_router, spam_router)
    await dp.start_polling(bot) 

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    try:
        redis_reg.ping()
        redis_bot.ping()
        print("Redis connected!")
    except Exception as e:
        print(e)
except Exception as e:
    print(e)
    pass
asyncio.run(main())




