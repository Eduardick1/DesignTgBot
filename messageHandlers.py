from aiogram import types, Router
from asyncio import sleep
from createBot import bot

spam_router = Router()

@spam_router.message()
async def Spam(message: types.Message):
        await bot.send_message(chat_id=message.chat.id, text="<b>[ANTISPAM]</b>", parse_mode="HTML")
        await sleep(1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)



    