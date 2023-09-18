from aiogram import types, Router, F
from aiogram.filters import Command
from createBot import bot
from keybords import istartkb, mainInfo

command_router = Router()


@command_router.message(F.text.lower().contains("старт") | F.text.lower().contains("start"))
async def startM(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    try:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-1,
                                    text=f"<b>Привет, {message.from_user.first_name}</b>\n\nМожешь сразу воспользоваться кнопкой '<b>Поиск</b>'\n\nТакже доступна команда '<b>Информация</b>', чтобы познакомиться с ботом по-лучше", # type: ignore
                                    reply_markup=istartkb)
    except Exception as e:
        print(f"Commands 13: {e}")
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
        except Exception as e:
            print(f"Commands 22: {e}")
            pass
        finally:
            await bot.send_message(chat_id=message.chat.id,
                                    text=f"<b>Привет, {message.from_user.first_name}</b>\n\nМожешь сразу воспользоваться кнопкой '<b>Поиск</b>'\n\nТакже доступна команда '<b>Информация</b>', чтобы познакомиться с ботом получше", # type: ignore
                                    reply_markup=istartkb)
        

@command_router.callback_query(F.data == "start")
async def startC(message: types.CallbackQuery):
    await message.answer()
    try:
        await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, #type:ignore
                                    text=f"<b>Привет, {message.from_user.first_name}</b>\n\nМожешь сразу воспользоваться кнопкой '<b>Поиск</b>'\n\nТакже доступна команда '<b>Информация</b>', чтобы познакомиться с ботом по-лучше",
                                    reply_markup=istartkb)
    except Exception as e:
        print(f"Commands 31: {e}")
        await bot.send_message(chat_id=message.message.chat.id, #type:ignore
                               text=f"<b>Привет, {message.from_user.first_name}</b>\n\nМожешь сразу воспользоваться кнопкой '<b>Поиск</b>'\n\nТакже доступна команда '<b>Информация</b>', чтобы познакомиться с ботом получше",
                               reply_markup=istartkb)

@command_router.callback_query(F.data == "delete_photo")
async def delete_photoC(message: types.CallbackQuery):
    await message.answer()
    await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id) #type:ignore


@command_router.message(F.text.lower().contains("инфо") | F.text.lower().contains("info"))
async def mainInfoM(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    try:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-1,
                                    text="ЗДЕСЬ БУДЕТ ОБЩАЯ ИНФОРМАЦИЯ РАБОТА В ПРОЦЕССЕ", 
                                    reply_markup=mainInfo('info')) #type:ignore
    except Exception as e:
        print(f"Commands 52: {e}")
        try:    
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
        except Exception as e:
            print(f"Commands 58: {e}")
            pass
        finally:
            await bot.send_message(chat_id=message.chat.id, text="ЗДЕСЬ БУДЕТ ОБЩАЯ ИНФОРМАЦИЯ РАБОТА В ПРОЦЕССЕ",
                                    reply_markup=mainInfo('info'))#type:ignore
     
        
            
@command_router.callback_query(F.data == "info")
async def mainInfoC(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, #type:ignore
                                text="ЗДЕСЬ БУДЕТ ОБЩАЯ ИНФОРМАЦИЯ РАБОТА В ПРОЦЕССЕ", 
                                reply_markup=mainInfo(message))#type:ignore 

@command_router.callback_query(F.data == "services")
async def servicesinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, #type:ignore
                                text="О сервисах...", 
                                reply_markup=mainInfo(message))#type:ignore

@command_router.callback_query(F.data == "requests")
async def requestsinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, #type:ignore
                                text="О запросах....", 
                                reply_markup=mainInfo(message))#type:ignore

@command_router.callback_query(F.data == "commands")
async def commandsinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, #type:ignore
                                text="О коммандах....", 
                                reply_markup=mainInfo(message))#type:ignore

@command_router.callback_query(F.data == "register")
async def registerinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, #type:ignore
                                text="О регистрациях токенов....", 
                                reply_markup=mainInfo(message))#type:ignore

@command_router.callback_query(F.data == "aboutbot")
async def aboutinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, #type:ignore
                                text="О доступных возможностях бота....", 
                                reply_markup=mainInfo(message))#type:ignore




    

    
    
    
    
    

    

    
    
    
