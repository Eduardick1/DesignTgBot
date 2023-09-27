from aiogram import types, Router, F
from asyncio import sleep
from createBot import bot
from DataBase import redis_reg, redis_bot

spam_router = Router()

# @spam_router.message(F.text.lower().contains('flushdb'))
# async def flushdb(message: types.Message):
#         await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
#         redis_reg.flushdb(asynchronous=True)


@spam_router.message()
async def Spam(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        d = await bot.send_message(chat_id=message.chat.id, text="<b>🗿[ANTISPAM]🗿</b>")
        await sleep(1)
        await bot.delete_message(chat_id=message.chat.id, message_id=d.message_id)
    except:
        pass




    