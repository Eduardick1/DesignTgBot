from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from keybords import istart_kb, exception_kb, typeskb
from DataBase import coll, redis_bot, redis_reg
from createBot import bot, FSM_
from commands import startC

from fake_useragent import UserAgent
from googletrans import Translator
from dotenv import load_dotenv
from asyncio import sleep
import httpx
import os

load_dotenv()

parse_router = Router()

#====================🢃🢃🢃===CANCEL_FSM===🢃🢃🢃=====================================================================================================================

@parse_router.callback_query(F.data == "cancel")
async def cancelFSM(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await state.clear()
        setRedis = redis_bot.smembers('todelete')
        for d in setRedis:
            await bot.delete_message(chat_id = callback.message.chat.id, message_id = int(d))
        redis_bot.delete(['todelete', 'req', 'hits'])
        await startC(callback)

#====================🢃🢃🢃===FSM_COLLECTING_REQUEST===🢃🢃🢃====================================================================================================================

@parse_router.message(FSM_.req, F.text)
async def collect_request(message: Message, state: FSMContext):
    if message.text[0] == "/": 
        await message.delete()
        d = await bot.send_message(text = "❗ Запрос не может начинаться с символа <i>/</i>",
                                    chat_id = message.chat.id)
        await sleep(1)
        await bot.delete_message(chat_id = message.chat.id, message_id = d.message_id)
    else:
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
            await state.update_data(req = str(message.text))
            redis_bot.set('req', Translator().translate(message.text).text)
            await state.set_state(FSM_.hits)
            d1 = await bot.send_message(text = "Введи <b>количество</b> необходимых медиа:", 
                                        chat_id = message.chat.id)
            redis_bot.sadd('todelete', [message.message_id, d1.message_id])


@parse_router.message(FSM_.hits, F.text.regexp('[0-9]+')) #ПОДУМАТЬ НА РЕФАКТОРИНГОМ
async def collect_hits(message: Message, state: FSMContext):
    try:
        if int(message.text) < 1 or int(message.text) > 10: 
            raise ValueError
        else:
            async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
                await bot.send_message(text = f"Выбери тип медиа:", chat_id = message.chat.id, reply_markup=typeskb())
                await state.clear()
                redis_bot.set('hits', int(message.text)) 
                redis_bot.sadd('todelete', message.message_id)
                setRedis = redis_bot.smembers('todelete')
                for d in setRedis:
                    await bot.delete_message(chat_id = message.chat.id, message_id = int(d))
                redis_bot.delete('todelete')
    except ValueError:
        await message.delete()
        d = await bot.send_message(text = "❗ <b>Проверь вводимое число</b>\n\nОно должно быть:\nЦелым\n<i>1</i> - Минимум\n<i>10</i> - Максимум", 
                                    chat_id = message.chat.id)
        await sleep(1)
        await bot.delete_message(chat_id = message.chat.id, message_id = d.message_id)
    except: pass

#====================🢃🢃🢃===CHOOSING_TYPE_MEDIA===🢃🢃🢃=====================================================================================================================

@parse_router.callback_query(F.data == "typeall")
async def typeall(callback: CallbackQuery):
    await callback.answer()
    await bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = exception_kb(callback), 
                                text = f"📌 <b>Твой запрос:</b>\n<i>{redis_bot.get('req')}</i>\
                                    \n\n📌 <b>Количество фото:</b> <i>{int(redis_bot.get('hits'))}</i>\
                                    \n\nВыбери сервис, с которого хочешь получить медиа 🤔:") 


@parse_router.callback_query((F.data == "vector") | (F.data == "illustration"))
async def typeother(callback: CallbackQuery):
    await callback.answer()
    await bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id,  
                                text = f"📌 <b>Твой запрос:</b>\n<i>{redis_bot.get('req')}</i>\
                                    \n\n📌 <b>Количество фото:</b> <i>{int(redis_bot.get('hits'))}</i>\
                                    \n\n<b>Тип медиа:</b> <i>{callback.data}</i>\
                                    \n\nМедиа будут предоставлены сервисом <i>PixaBay</i>")
    await parsing_pix(callback, type = callback.data)
    await sleep(2)
    await bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)

#====================🢃🢃🢃===PARSING_PIXABAY_service===🢃🢃🢃=====================================================================================================================

@parse_router.callback_query(F.data == "pixabay") #
async def parsing_pix(callback: CallbackQuery, type: str = "all"):
    if callback.data != "all":
        await callback.answer()
        await bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id) 
    url = f"https://pixabay.com/api/?key={redis_reg.get('tokenpix')}&q={str(redis_bot.get('req')).replace(',', '%2C')}&image_type = {type}&per_page = {30}" 
    r = httpx.get(url, headers = {"User-Agent": f"{UserAgent().random}"}, follow_redirects = True)
    print(f"Pix status: {r.status_code}")
    if r.status_code == 200:
        rpix = r.json()
        if rpix["total"] == 0:
            await bot.send_message(chat_id = callback.message.chat.id, reply_markup = exception_kb(callback), 
                                    text = f"❗ <i>{rpix['total']}</i> доступных фото из <i>PixaBay</i>\
                                    \n\n{'Попробуй другой сервис, либо измени <b>Запрос</b>! 🔎' if callback.data != 'all' else ''}")
            if callback.data != 'pixabay': return False
        if rpix['total'] >= int(redis_bot.get('hits')):
            await bot.send_message(chat_id = callback.message.chat.id, text = f"✔️ Доступно <i>{rpix['total']}</i> фото из <i>PixaBay</i>",  
                                    reply_markup = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Перейти на PixaBay с данным запросом", 
                                                                                                                url = f"https://pixabay.com/photos/search/{redis_bot.get('req')}/")]]))
            async with ChatActionSender.upload_photo(bot = bot, chat_id = callback.message.chat.id):
                for photo in range(int(redis_bot.get('hits'))):
                    await sleep(1.1)
                    await bot.send_photo(chat_id = callback.from_user.id, photo = rpix["hits"][photo]["webformatURL"],
                                        caption=f"{rpix['hits'][photo]['webformatWidth']}x{rpix['hits'][photo]['webformatHeight']}", 
                                        reply_markup= InlineKeyboardMarkup( 
                                        inline_keyboard = [[InlineKeyboardButton(text = "❌", callback_data="delete_photo"), 
                                                        InlineKeyboardButton(text = "Подробнее ⭷", 
                                                                                url = rpix["hits"][photo]["pageURL"])]]))
        else:
            await bot.send_message(chat_id = callback.message.chat.id, text = f"✔️ Доступно только <i>{rpix['total']}</i> фото из <i>PixaBay</i>", 
                                    reply_markup = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Перейти на PixaBay с данным запросом", 
                                                                                                            url = f"https://pixabay.com/photos/search/{redis_bot.get('req')}/")]]))
            async with ChatActionSender.upload_photo(bot = bot, chat_id = callback.message.chat.id):
                for photo in range(rpix['total']):
                    await sleep(1.1)
                    await bot.send_photo(chat_id = callback.from_user.id, photo = rpix["hits"][photo]["webformatURL"],
                                        caption=f"{rpix['hits'][photo]['webformatWidth']}x{rpix['hits'][photo]['webformatHeight']}", 
                                        reply_markup= InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "❌", callback_data="delete_photo")], 
                                                                                            [InlineKeyboardButton(text = "Подробнее ⭷", 
                                                                                                                url = rpix["hits"][photo]["pageURL"])]]))
        if callback.data == "pixabay":
            await bot.send_message(chat_id = callback.message.chat.id, reply_markup = exception_kb(callback),
                                    text = "Можешь выбрать другой сервис, либо изменить <b>Запрос</b> 🔎,\
                                            \nа также перейти в раздел <b>Информация</b> 📖")
    else:
        if callback.data != 'pixabay': return False
        else: 
            await bot.send_message(chat_id = callback.message.chat.id, reply_markup = istart_kb(),
                                    text = f"❗ Во время поиска на <i>PixaBay</i> возникла ошибка: <i>{r.status_code}</i>\
                                            \n\nСообщи об этом в техподдержку!")

#====================🢃🢃🢃===PARSING_PEXELS_service===🢃🢃🢃=====================================================================================================================

@parse_router.callback_query(F.data == "pexel") #
async def parsing_pex(callback: CallbackQuery, demo: int = 0):
    if callback.data != "all":
        await callback.answer()
        await bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    PexDemoTok = f"{redis_reg.get('tokenpex') if demo == 0 else coll.find_one({'_id': int(os.getenv('admin_id'))})['tokenpex']}"
    url = f"https://api.pexels.com/v1/search?query={str(redis_bot.get('req')).replace(',', '%2C')}&per_page = {30}"
    r = httpx.get(url, headers = {"User-Agent": f"{UserAgent().random}", "Authorization": PexDemoTok}, follow_redirects = True)
    print(f"Pex status: {r.status_code}")
    if r.status_code == 200:
        rpex = r.json()
        if rpex['total_results'] == 0:
            await bot.send_message(chat_id = callback.message.chat.id, reply_markup = exception_kb(callback), 
                                    text = f"❗ <i>{rpex['total_results']}</i> доступных фото из <i>Pexels</i>\
                                            \n\n{'Попробуй другой сервис, либо измени <b>Запрос</b> 🔎' if callback.data != 'all' else ''}")
            if callback.data != 'pexel': return False
        if rpex['total_results'] >= int(redis_bot.get('hits')):
            await bot.send_message(chat_id = callback.message.chat.id, text = f"✔️ Доступно <i>{rpex['total_results']}</i> фото из <i>Pexels</i>",
                                    reply_markup = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Перейти на Pexels с данным запросом", 
                                                                                                                url = f"https://www.pexels.com/search/{redis_bot.get('req')}/")]]))
            async with ChatActionSender.upload_photo(bot = bot, chat_id = callback.message.chat.id):
                for photo in range(int(redis_bot.get('hits'))):
                    await sleep(1.1)
                    await bot.send_photo(chat_id = callback.from_user.id, photo = rpex["photos"][photo]["src"]["large"],
                                        reply_markup= InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "❌", callback_data="delete_photo")], 
                                                                                            [InlineKeyboardButton(text = "Подробнее ⭷", 
                                                                                                                url = rpex["photos"][photo]["url"])]]))
            if callback.data == 'pexel':
                await bot.send_message(chat_id = callback.message.chat.id, reply_markup = exception_kb(callback),  
                                        text = "Можешь выбрать другой сервис, либо изменить <b>Запрос</b> 🔎,\
                                                \nа также перейти в раздел <b>Информация</b> 📖")
        else:
            await bot.send_message(chat_id = callback.message.chat.id, 
                                    text = f"✔️ Доступно только <i>{rpex['total_results']}</i> фото из <i>Pexels</i>",
                                    reply_markup = InlineKeyboardMarkup( 
                                    inline_keyboard = [[InlineKeyboardButton(text = "Перейти на Pexels с данным запросом",
                                                                            url = f"https://www.pexels.com/search/{redis_bot.get('req')}/")]]))
            async with ChatActionSender.upload_photo(bot = bot, chat_id = callback.message.chat.id):
                for photo in range(rpex['total_results']):
                    await sleep(1.1)
                    await bot.send_photo(chat_id = callback.from_user.id, photo = rpex["photos"][photo]["src"]["large"],
                                        reply_markup= InlineKeyboardMarkup( 
                                        inline_keyboard = [[InlineKeyboardButton(text = "❌", callback_data="delete_photo"), 
                                                            InlineKeyboardButton(text = "Подробнее ⭷", url = rpex["photos"][photo]["url"])]]))
        if callback.data == 'pexel':
            await bot.send_message(chat_id = callback.message.chat.id, reply_markup = exception_kb(callback),  
                                    text = "Можешь выбрать другой сервис, либо изменить <b>Запрос</b> 🔎,\
                                            \nа также перейти в раздел <b>Информация</b> 📖")
    else:
        if callback.data != 'pexel': return False
        else:    
            await bot.send_message(chat_id = callback.message.chat.id, reply_markup = istart_kb(), 
                                    text = f"❗ Во время поиска на <i>Pexels</i> возникла ошибка: <i>{r.status_code}</i>\
                                            \n\nСообщи об этом в техподдержку!")

#====================🢃🢃🢃===PARSING_UNSPLASH_service===🢃🢃🢃=====================================================================================================================

@parse_router.callback_query(F.data == "splash")
async def parsing_spl(callback: CallbackQuery, demo: int = 0): 
    if callback.data == "splash":
        await callback.answer()
        await bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    SplDemoTok = f"{redis_reg.get('tokenspl') if demo == 0 else coll.find_one({'_id': int(os.getenv('admin_id'))})['tokenspl']}"
    url = f"https://api.unsplash.com/search/photos?query={str(redis_bot.get('req')).replace(' ', '-').replace(',', '%2C')}&per_page = {30}"#&client_id = {redis_reg.get('tokenspl')}"
    r = httpx.get(url, headers =  {"User-Agent": f"{UserAgent().random}", "Authorization": f"Client-ID {SplDemoTok}"}, follow_redirects = True)
    print(f"Spl status: {r.status_code}")
    if r.status_code == 200:
        rspl = r.json()
        if rspl['total'] == 0:
            await bot.send_message(chat_id = callback.message.chat.id, reply_markup = exception_kb(callback), 
                                    text = f"❗ <i>{rspl['total']}</i> доступных фото из <b>Unsplash</b>.\
                                    \n\n{'Попробуй другой сервис, либо измени <b>Запрос</b>! 🔎' if callback.data != 'all' else ''}")
            if callback.data != 'splash': return False
            if rspl['total'] >= int(redis_bot.get('hits')):
                await bot.send_message(chat_id = callback.message.chat.id, text = f"✔️ Доступно <i>{rspl['total']}</i> фото из <b>Unsplash</b>",
                                        reply_markup = InlineKeyboardMarkup(inline_keyboard = [
                                                    [InlineKeyboardButton(text = "Перейти на Unsplash с данным запросом", 
                                                                            url = f"https://unsplash.com/s/photos/{redis_bot.get('req')}")]]))
                async with ChatActionSender.upload_photo(bot = bot, chat_id = callback.message.chat.id):
                    for photo in range(int(redis_bot.get('hits'))):
                        await sleep(1.1)
                        await bot.send_photo(chat_id = callback.from_user.id, photo = rspl["results"][photo]["urls"]["small"], 
                                            reply_markup = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "❌", callback_data="delete_photo"), 
                                                                                            InlineKeyboardButton(text = "Подробнее ⭷",  url = rspl["results"][photo]["links"]["html"])]]))
            else:
                await bot.send_message(chat_id = callback.message.chat.id, text = f"✔️ Доступно только <i>{rspl['total']}</i> фото из <b>Unsplash</b>",
                                        reply_markup = InlineKeyboardMarkup(inline_keyboard = [
                                                    [InlineKeyboardButton(text = "Перейти на Unsplash с данным запросом", 
                                                                            url = f"https://unsplash.com/s/photos/{redis_bot.get('req')}")]]))
                async with ChatActionSender.upload_photo(bot = bot, chat_id = callback.message.chat.id):
                    for photo in range(rspl['total']):
                        await sleep(1.1)
                        await bot.send_photo(chat_id = callback.from_user.id, photo = rspl["results"][photo]["urls"]["small"], 
                                            reply_markup = InlineKeyboardMarkup(inline_keyboard = [
                                                        [InlineKeyboardButton(text = "❌", callback_data="delete_photo"), 
                                                        InlineKeyboardButton(text = "Подробнее ⭷",  url = rspl["results"][photo]["links"]["html"])]]))
            if callback.data == 'splash':
                await bot.send_message(chat_id = callback.message.chat.id, reply_markup = exception_kb(callback), 
                                        text = "Можешь выбрать другой сервис, либо изменить <b>Запрос</b> 🔎,\
                                            \nа также перейти в раздел <b>Информация</b> 📖")
    else:
        if callback.data != 'splash': return False
        else: 
            await bot.send_message(chat_id = callback.message.chat.id, reply_markup = istart_kb(),
                            text = f"❗ Во время поиска на <b>Unsplash</b> возникла ошибка: <i>{r.status_code}</i>\n\nСообщи об этом в техподдержку!")

#====================🢃🢃🢃===PARSING_ALL_SERVICES===🢃🢃🢃=====================================================================================================================

@parse_router.callback_query(F.data == "all") #Подумать на рефакторингом
async def parsing_all_services(callback: CallbackQuery):
    await callback.answer() 
    await bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)  
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):    
        if await parsing_pix(callback) == False:
            if await parsing_pex(callback) == False:
                if await parsing_spl(callback) == False:
                    await bot.send_message(chat_id = callback.message.chat.id, 
                                            text = f"❗ К сожалению, ни один из сервисов не смог найти что-либо по запросу: {redis_bot.get('req')}")
                    await sleep(2)
                    for i in range(1,5):
                        await bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id+i)
            else:
                if await parsing_spl(callback) == False:
                    pass
                pass
        else:
            if await parsing_pex(callback) == False:
                if await parsing_spl(callback) == False:
                    pass
                pass
            else:
                if await parsing_spl(callback) == False:
                    pass
        await bot.send_message(chat_id = callback.message.chat.id, reply_markup = istart_kb(),
                                text = "Можешь изменить <b>Запрос</b> 🔎,\
                                    \nа также перейти в раздел <b>Информация</b> 📖")

#====================🢃🢃🢃===DEMO_MODE===🢃🢃🢃=====================================================================================================================

@parse_router.callback_query(F.data == 'DEMO')
async def demo_mode(call: CallbackQuery):
    await call.answer()
    demo: int = coll.find_one({'_id': call.from_user.id})['demo']
    await parsing_pex(call, demo = demo)
    await parsing_spl(call, demo = demo)
    coll.update_one({'_id': call.from_user.id}, {"$set": {'demo': demo-1}})
