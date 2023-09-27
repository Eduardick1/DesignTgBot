from middlewares import RedisterCheckMiddleWare, Command_manager
from createBot import dp, bot
from errors import error_router
from commands import command_router
from parserdesign import parse_router
from messageHandlers import spam_router
from registration import register_router
from DataBase import client, redis_reg, redis_bot
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

async def main(): #Отформатировать тексты!!!! Криво вставляются токены при демо режиме 
    dp.message.middleware.register(RedisterCheckMiddleWare())
    dp.message.middleware.register(Command_manager())
    dp.include_routers(error_router, parse_router, command_router, register_router, spam_router)
    #await bot.set_webhook(url=f'{os.getenv("WEBHOOK")}', drop_pending_updates=True)
    await dp.start_polling(bots=bot, close_bot_session=True)
    
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




