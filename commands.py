from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from createBot import bot, FSM_
from DataBase import redis_bot as redis
from keybords import istart_kb, mainInfo, cancelkb 

command_router = Router()


@command_router.message(Command('start', ignore_case=True), StateFilter(None))
async def startM(message: types.Message):
    await bot.send_message(text=f"<b>Привет, {message.from_user.first_name}</b>\
                                \n\n🔎 <b>Поиск</b> - начать поиск медиа\
                                \n\n📖 <b>Информация</b> - познакомиться с ботом получше",
                            chat_id=message.chat.id, reply_markup=istart_kb())       

@command_router.callback_query(F.data == "start")
async def startC(message: types.CallbackQuery):
    await message.answer()
    try:
        await bot.edit_message_text(text=f"<b>Привет, {message.from_user.first_name}</b>\
                                    \n\n🔎 <b>Поиск</b> - начать поиск медиа\
                                    \n\n📖 <b>Информация</b> - познакомиться с ботом получше",
                                    chat_id=message.message.chat.id, message_id=message.message.message_id, reply_markup=istart_kb())
    except Exception as e:
        print(f"Commands 29: {e}")
        await bot.send_message(text=f"<b>Привет, {message.from_user.first_name}</b>\
                                    \n\n🔎 <b>Поиск</b> - начать поиск медиа\
                                    \n\n📖 <b>Информация</b> - познакомиться с ботом получше",
                               chat_id=message.message.chat.id, reply_markup=istart_kb())


@command_router.message(Command('search', ignore_case=True), StateFilter(None))
async def searchM(message: types.Message, state: FSMContext): 
    d1 = await bot.send_message(text="В любой момент можешь воспользоваться командой <b>Отмена</b>",
                                chat_id=message.chat.id, reply_markup=cancelkb)
    redis.sadd('todelete', d1.message_id)
    await state.set_state(FSM_.req)
    d2 = await bot.send_message(text="Для поиска фото, придумай ключевые слова(теги):", 
                                chat_id=message.chat.id)
    redis.sadd('todelete', d2.message_id)

@command_router.callback_query(F.data == "search")
async def searchC(message: types.CallbackQuery, state: FSMContext):
    await message.answer()
    try: 
        d1 = await bot.edit_message_text(text="В любой момент можешь воспользоваться командой <b>Отмена</b>",
                                        chat_id=message.message.chat.id, message_id=message.message.message_id, reply_markup=cancelkb)
    except Exception as e:
        print(f"Commands 66: {e}")
        d1 = await bot.send_message(text="В любой момент можешь воспользоваться командой <b>Отмена</b>", 
                                   chat_id=message.message.chat.id, reply_markup=cancelkb)
    redis.sadd('todelete', d1.message_id)
    await state.set_state(FSM_.req)
    d2 = await bot.send_message(text="Для поиска фото, придумай ключевые слова(теги):", 
                                chat_id=message.message.chat.id) 
    redis.sadd('todelete', d2.message_id)


@command_router.callback_query(F.data == "delete_photo")
async def delete_photoC(message: types.CallbackQuery):
    await message.answer()
    await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id) 


@command_router.message(Command('info', ignore_case=True), StateFilter(None))
async def mainInfoM(message: types.Message):
    await bot.send_message(text="📖 ЗДЕСЬ БУДЕТ ОБЩАЯ ИНФОРМАЦИЯ\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                           chat_id=message.chat.id, reply_markup=mainInfo('info'))
                   
@command_router.callback_query(F.data == "info")
async def mainInfoC(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, 
                                text="📖 ЗДЕСЬ БУДЕТ ОБЩАЯ ИНФОРМАЦИЯ\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                reply_markup=mainInfo(message)) 

@command_router.callback_query(F.data == "services")
async def servicesinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(text="О сервисах...📚\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                chat_id=message.message.chat.id, message_id=message.message.message_id, 
                                reply_markup=mainInfo(message))

@command_router.callback_query(F.data == "requests")
async def requestsinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(text="О запросах...🔎\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                chat_id=message.message.chat.id, message_id=message.message.message_id, 
                                reply_markup=mainInfo(message))

@command_router.callback_query(F.data == "commands")
async def commandsinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(text="О коммандах...💬\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                chat_id=message.message.chat.id, message_id=message.message.message_id, 
                                reply_markup=mainInfo(message))

@command_router.callback_query(F.data == "register")
async def registerinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(text="О регистрациях токенов...✏️\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳",
                                chat_id=message.message.chat.id, message_id=message.message.message_id, 
                                reply_markup=mainInfo(message))

@command_router.callback_query(F.data == "aboutbot")
async def aboutinfo(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(text="О доступных возможностях бота...🤖\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                chat_id=message.message.chat.id, message_id=message.message.message_id, 
                                reply_markup=mainInfo(message))