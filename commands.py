from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from keybords import istart_kb, mainInfo, unreg_kb, get_reg, cancelkb 
from DataBase import redis_bot as redis
from createBot import bot, FSM_


command_router = Router()

#====================🢃🢃🢃===COMMAND_START===🢃🢃🢃====================================================================================================================

@command_router.message(Command('start', ignore_case=True), StateFilter(None))
async def startM(message: types.Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await bot.send_message(chat_id=message.chat.id, reply_markup=istart_kb(),
                                text=f"<b>Привет, {message.from_user.first_name}</b>\
                                    \n\n🔎 <b>Поиск</b> - начать поиск медиа\
                                    \n\n📖 <b>Информация</b> - познакомиться с ботом")       

@command_router.callback_query(F.data == "start")
async def startC(callback: types.CallbackQuery):
    await callback.answer()
    async with ChatActionSender.typing(bot=bot, chat_id=callback.message.chat.id):    
        try:
            await bot.edit_message_text(text=f"<b>Привет, {callback.from_user.first_name}</b>\
                                        \n\n🔎 <b>Поиск</b> - начать поиск медиа\
                                        \n\n📖 <b>Информация</b> - познакомиться с ботом",
                                        chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=istart_kb())
        except Exception as e:
            print(f"Commands 29: {e}")
            await bot.send_message(text=f"<b>Привет, {callback.from_user.first_name}</b>\
                                        \n\n🔎 <b>Поиск</b> - начать поиск медиа\
                                        \n\n📖 <b>Информация</b> - познакомиться с ботом",
                                chat_id=callback.message.chat.id, reply_markup=istart_kb())

#====================🢃🢃🢃===COMMAND_SEARCH===🢃🢃🢃=====================================================================================================================

@command_router.message(Command('search', ignore_case=True), StateFilter(None))
async def searchM(message: types.Message, state: FSMContext): 
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        d1 = await bot.send_message(text="В любой момент можешь воспользоваться командой <b>Отмена</b>",
                                    chat_id=message.chat.id, reply_markup=cancelkb)
        await state.set_state(FSM_.req)
        d2 = await bot.send_message(text="Для поиска фото, придумай ключевые слова(теги):", 
                                    chat_id=message.chat.id)
        redis.sadd('todelete', [d1.message_id, d2.message_id])

@command_router.callback_query(F.data == "search")
async def searchC(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with ChatActionSender.typing(bot=bot, chat_id=callback.message.chat.id):
        try: 
            d1 = await bot.edit_message_text(text="В любой момент можешь воспользоваться командой <b>Отмена</b>",
                                            chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=cancelkb)
        except Exception as e:
            print(f"Commands 66: {e}")
            d1 = await bot.send_message(text="В любой момент можешь воспользоваться командой <b>Отмена</b>", 
                                    chat_id=callback.message.chat.id, reply_markup=cancelkb)
        await state.set_state(FSM_.req)
        d2 = await bot.send_message(text="Для поиска фото, придумай ключевые слова(теги):", 
                                    chat_id=callback.message.chat.id) 
        redis.sadd('todelete', [d1.message_id, d2.message_id])

#====================🢃🢃🢃===ABILITY_to_DELETE_PHOTO===🢃🢃🢃=====================================================================================================================

@command_router.callback_query(F.data == "delete_photo")
async def delete_photoC(callback: types.CallbackQuery):
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id) 

#====================🢃🢃🢃===COMMAND_REGISTRATION===🢃🢃🢃=====================================================================================================================

@command_router.callback_query(F.data == 'registration')
async def register(callback: types.CallbackQuery):
    callback.answer()

    def get_registerText() -> str:
        if len(get_reg()) == 0:
            return "<b>Привет, {}</b>\n\nВозможно ты первый раз работаешь с этим ботом\
                    \n\nТебе следует настроить API каждого сервиса, тоесть подключить твои аккаунты для корректной работы и для возможности пользоваться всем функционалом бота:\
                    \n <i>PixaBay</i>, <i>Pexels</i>, <i>Unsplash</i>\
                    \n\nЭта первоначальная настройка займёт от 5 до 10 минут, в дальнейшем тебе не нужно будет этим заниматься, так как бот тебя запомнит\
                    \n\nВыбери сервис, с которого хочешь начать" 
        else:
            return "<b>Привет, {}</b>\n\nУ тебя ещё есть незарегестрированные токены\
                    \n\nДля корректной работы и для возможности пользоваться всем функционалом бота, тебе следует настроить оставшиеся сервисы"
        
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, 
                                    text=get_registerText().format(callback.from_user.first_name),
                                    reply_markup=unreg_kb())

#====================🢃🢃🢃===COMMAND_INFO=and=INFO_block===🢃🢃🢃=====================================================================================================================

@command_router.message(Command('info', ignore_case=True), StateFilter(None))
async def mainInfoM(message: types.Message):
    await bot.send_message(text="📖 ЗДЕСЬ БУДЕТ ОБЩАЯ ИНФОРМАЦИЯ\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                           chat_id=message.chat.id, reply_markup=mainInfo('info'))
                   
@command_router.callback_query(F.data == "info")
async def mainInfoC(callback: types.CallbackQuery):
    await callback.answer()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, 
                                text="📖 ЗДЕСЬ БУДЕТ ОБЩАЯ ИНФОРМАЦИЯ\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                reply_markup=mainInfo(callback)) 

@command_router.callback_query(F.data == "services")
async def servicesinfo(callback: types.CallbackQuery):
    await callback.answer()
    await bot.edit_message_text(text="О сервисах...📚\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                chat_id=callback.message.chat.id, message_id=callback.message.message_id, 
                                reply_markup=mainInfo(callback))

@command_router.callback_query(F.data == "requests")
async def requestsinfo(callback: types.CallbackQuery):
    await callback.answer()
    await bot.edit_message_text(text="О запросах...🔎\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                chat_id=callback.message.chat.id, message_id=callback.message.message_id, 
                                reply_markup=mainInfo(callback))

@command_router.callback_query(F.data == "commands")
async def commandsinfo(callback: types.CallbackQuery):
    await callback.answer()
    await bot.edit_message_text(text="О коммандах...💬\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                chat_id=callback.message.chat.id, message_id=callback.message.message_id, 
                                reply_markup=mainInfo(callback))

@command_router.callback_query(F.data == "register")
async def registerinfo(callback: types.CallbackQuery):
    await callback.answer()
    await bot.edit_message_text(text="О регистрациях токенов...✏️\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳",
                                chat_id=callback.message.chat.id, message_id=callback.message.message_id, 
                                reply_markup=mainInfo(callback))

@command_router.callback_query(F.data == "aboutbot")
async def aboutinfo(callback: types.CallbackQuery):
    await callback.answer()
    await bot.edit_message_text(text="О доступных возможностях бота...🤖\n\n🏗️[РАБОТА В ПРОЦЕССЕ]⏳", 
                                chat_id=callback.message.chat.id, message_id=callback.message.message_id, 
                                reply_markup=mainInfo(callback))