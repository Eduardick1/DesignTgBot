from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from createBot import bot, FSM_
from keybords import istart_kb, exception_kb, typeskb
from commands import startC
from DataBase import coll, redis_bot, redis_reg
from asyncio import sleep
from googletrans import Translator
from fake_useragent import UserAgent
from dotenv import load_dotenv
import httpx
import os
load_dotenv()

parse_router = Router()


@parse_router.callback_query(F.data == "cancel")
async def cancelFSM(message: types.CallbackQuery, state: FSMContext):
    await message.answer()
    await state.clear()
    setRedis = redis_bot.smembers('todelete')
    for d in setRedis:
        try: await bot.delete_message(chat_id=message.message.chat.id, message_id=int(d))
        except: pass
    redis_bot.delete('todelete')
    await startC(message)

#==================================================================================================================================================================

@parse_router.message(FSM_.req, F.content_type == 'text')
async def collect_request(message: types.Message, state: FSMContext):
    if message.text[0] == "/": 
        await message.delete()
        d = await bot.send_message(text="❗ Запрос не может начинаться с символа '<i>/</i>'\
                                        \n\nЕсли хочешь воспользоваться командой, воспользуйся кнопкой <b>ОТМЕНА</b>",
                                    chat_id=message.chat.id)
        await sleep(1)
        await bot.delete_message(chat_id=message.chat.id, message_id=d.message_id)
    else:
        await state.update_data(req = str(message.text))
        redis_bot.set('req', Translator().translate(message.text).text)
        await state.set_state(FSM_.hits)
        d1 = await bot.send_message(text="Введи количество необходимых медиа:", 
                                    chat_id=message.chat.id)
        redis_bot.sadd('todelete', message.message_id)
        redis_bot.sadd('todelete', d1.message_id)

@parse_router.message(FSM_.hits, F.text.regexp('[0-9]+')) #ПОДУМАТЬ НА РЕФАКТОРИНГОМ
async def collect_hits(message: types.Message, state: FSMContext):
    try:
        if int(message.text) < 1: 
            raise ValueError
        else:
            redis_bot.set('hits', int(message.text)) 
            await state.clear()
            redis_bot.sadd('todelete', message.message_id)
            await bot.send_message(text=f"Выбери тип медиа:", 
                                   chat_id=message.chat.id, reply_markup=typeskb())
            setRedis = redis_bot.smembers('todelete')
            for d in setRedis:
                try: await bot.delete_message(chat_id=message.chat.id, message_id=int(d))
                except: pass
            redis_bot.delete('todelete')
    except ValueError:
        await message.delete()
        d = await bot.send_message(text="❗ <b>Проверь вводимое число!</b>\n\nКак минимум оно должно быть целым и больше <i>0</i>", 
        chat_id=message.chat.id)
        await sleep(1)
        await bot.delete_message(chat_id=message.chat.id, message_id=d.message_id)
    except: pass

@parse_router.callback_query(F.data == "typeall")
async def typeall(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, reply_markup=exception_kb(message), 
                                text=f"📌 <b>Твой запрос:</b>\n<i>{redis_bot.get('req')}</i>\
                                    \n\n📌 <b>Количество фото:</b> <i>{redis_bot.get('hits')}</i>\
                                    \n\nВыбери сервис, с которого хочешь получить медиа 🤔:") 


@parse_router.callback_query((F.data == "vector") | (F.data == "illustration"))
async def typeother(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,  
                                text=f"📌 <b>Твой запрос:</b>\n<i>{redis_bot.get('req')}</i>\
                                    \n\n📌 <b>Количество фото:</b> <i>{redis_bot.get('hits')}</i>\
                                    \n\n<b>Тип медиа:</b> <i>{message.data}</i>\
                                    \n\nМедиа будут предоставлены сервисом PixaBay<i></i>")
    await parspix(message, type = message.data)
    await sleep(3)
    await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)


@parse_router.callback_query(F.data == "pixabay")
async def parspix(message: types.CallbackQuery, type: str = "all"):
    if message.data != "all":
        await message.answer()
        try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id) 
        except: pass
    url = f"https://pixabay.com/api/?key={redis_reg.get('tokenpix')}&q={str(redis_bot.get('req')).replace(',', '%2C')}&image_type = {type}&per_page = {int(redis_bot.get('hits')) if int(redis_bot.get('hits'))>2 else 3}" 
    r = httpx.get(url, headers = {"User-Agent": f"{UserAgent().random}"}, follow_redirects=True)
    print(f"Pix status: {r.status_code}")
    if r.status_code == 200:
        rpix = r.json()
        if rpix["total"] == 0:
            await bot.send_message(chat_id=message.message.chat.id, 
                                    text=f"❗ <i>{rpix['total']}</i> фото доступно из <i>PixaBay</i>.\
                                    \n\n{'Попробуй другой сервис, либо измени запрос! 🔎' if message.data != 'all' else ''}",  
                                    reply_markup=exception_kb(message))
            if message.data != 'pixabay': return False
        else:
            if rpix['total'] >= int(redis_bot.get('hits')):
                await bot.send_message(chat_id=message.message.chat.id,
                                        text=f"✔️ Доступно <i>{rpix['total']}</i> фото из <i>PixaBay</i>",  
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти на PixaBay с данным запросом", 
                                                                                                                 url=f"https://pixabay.com/photos/search/{redis_bot.get('req')}/")]]))
                for photo in range(int(redis_bot.get('hits'))):
                    await sleep(1.1)
                    await bot.send_photo(chat_id=message.from_user.id, photo=rpix["hits"][photo]["webformatURL"],
                                        caption=f"{rpix['hits'][photo]['webformatWidth']}x{rpix['hits'][photo]['webformatHeight']}", 
                                        reply_markup= InlineKeyboardMarkup( 
                                        inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo"), 
                                                        InlineKeyboardButton(text="Подробнее ⇑", 
                                                                                url=rpix["hits"][photo]["pageURL"])]]))
                if message.data == "pixabay":
                    await bot.send_message(chat_id=message.message.chat.id, reply_markup=exception_kb(message),
                                            text="Можешь изменить <b>Запрос</b> 🔎, а также перейти в раздел <b>Информация</b> 📖")
            else:
                await bot.send_message(chat_id=message.message.chat.id, 
                                        text=f"✔️ Доступно только <i>{rpix['total']}</i> фото из <i>PixaBay</i>", 
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти на PixaBay с данным запросом", 
                                                                                                                url=f"https://pixabay.com/photos/search/{redis_bot.get('req')}/")]]))
                for photo in range(rpix['total']):
                    await sleep(1.1)
                    await bot.send_photo(chat_id=message.from_user.id, photo=rpix["hits"][photo]["webformatURL"],
                                        caption=f"{rpix['hits'][photo]['webformatWidth']}x{rpix['hits'][photo]['webformatHeight']}", 
                                        reply_markup= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo")], 
                                                                                            [InlineKeyboardButton(text="Подробнее ⇑", 
                                                                                                                url=rpix["hits"][photo]["pageURL"])]]))
                if message.data == "pixabay":
                    await bot.send_message(chat_id=message.message.chat.id, reply_markup=exception_kb(message),
                                            text="Можешь выбрать другой сервис либо изменить <b>Запрос</b> 🔎, а также перейти в раздел <b>Информация</b> 📖")
    else:
        if message.data != 'pixabay': return False
        else: 
            await bot.send_message(chat_id=message.message.chat.id, reply_markup=istart_kb(),
                                    text=f"❗ Во время поиска на <i>PixaBay</i> возникла ошибка: <i>{r.status_code}</i>\
                                            \n\nСообщи об этом техподдержке!")


@parse_router.callback_query(F.data == "pexel")
async def parspex(message: types.CallbackQuery, demo: int = 0):
    if message.data != "all":
        await message.answer()
        try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)
        except: pass
    pextok = f"{redis_reg.get('tokenpex') if demo == 0 else coll.find_one({'_id': int(os.getenv('admin_id'))})['tokenpex']}"
    PexHeaders = {"User-Agent": f"{UserAgent().random}", "Authorization":pextok}
    url = f"https://api.pexels.com/v1/search?query={str(redis_bot.get('req')).replace(',', '%2C')}&per_page = {redis_bot.get('hits')}"
    r = httpx.get(url, headers = PexHeaders, follow_redirects=True)
    print(f"Pex status: {r.status_code}")
    if r.status_code == 200:
        rpex = r.json()
        if rpex['total_results'] == 0:
            await bot.send_message(chat_id=message.message.chat.id, reply_markup=exception_kb(message), 
                                    text=f"❗ <i>{rpex['total_results']}</i> доступных фото из <i>Pexels</i>.\
                                    \n\n{'Попробуй другой сервис, либо измени запрос! 🔎' if message.data != 'all' else ''}")
            if message.data != 'pexel': return False
        else:
            if rpex['total_results'] >= int(redis_bot.get('hits')):
                await bot.send_message(chat_id=message.message.chat.id, text=f"✔️ Доступно <i>{rpex['total_results']}</i> фото из <i>Pexels</i>",
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти на Pexels с данным запросом", 
                                                                                                                url=f"https://www.pexels.com/search/{redis_bot.get('req')}/")]]))
                for photo in range(int(redis_bot.get('hits'))):
                    await sleep(1.1)
                    await bot.send_photo(chat_id=message.from_user.id, photo=rpex["photos"][photo]["src"]["large"],
                                        reply_markup= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo")], 
                                                                                            [InlineKeyboardButton(text="Подробнее ⇑", 
                                                                                                                url=rpex["photos"][photo]["url"])]]))
                if message.data == 'pexel':
                    await bot.send_message(chat_id=message.message.chat.id, reply_markup=exception_kb(message),  
                                        text="Можешь выбрать другой сервис либо изменить <b>Запрос</b> 🔎, а также перейти в раздел <b>Информация</b> 📖")
            else:
                await bot.send_message(chat_id=message.message.chat.id, 
                                        text=f"✔️ Доступно только <i>{rpex['total_results']}</i> фото из <i>Pexels</i>",
                                        reply_markup=InlineKeyboardMarkup( 
                                        inline_keyboard=[[InlineKeyboardButton(text="Перейти на Pexels с данным запросом",
                                                                                url=f"https://www.pexels.com/search/{redis_bot.get('req')}/")]]))
                for photo in range(rpex['total_results']):
                    await sleep(1.1)
                    await bot.send_photo(chat_id=message.from_user.id, photo=rpex["photos"][photo]["src"]["large"],
                                        reply_markup= InlineKeyboardMarkup( 
                                        inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo"), 
                                                        InlineKeyboardButton(text="Подробнее ⇑", 
                                                                            url=rpex["photos"][photo]["url"])]]))
                if message.data == 'pexel':
                    await bot.send_message(chat_id=message.message.chat.id, reply_markup=exception_kb(message),  
                                        text="Можешь выбрать другой сервис либо изменить <b>Запрос</b> 🔎, а также перейти в раздел <b>Информация</b> 📖")
    else:
        if message.data != 'pexel': return False
        else:    
            await bot.send_message(chat_id=message.message.chat.id, reply_markup=istart_kb(), 
                                text=f"❗ Во время поиска на <i>Pexels</i> возникла ошибка: <i>{r.status_code}</i>\
                                        \n\nСообщи об этом техподдержке!")


@parse_router.callback_query(F.data == "splash")
async def parsunspl(message: types.CallbackQuery, page: int = 1): #max hits is 30
    if message.data == "splash":
        await message.answer()
        try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)
        except: pass
    url = f"https://api.unsplash.com/search/photos?query={str(redis_bot.get('req')).replace(' ', '-').replace(',', '%2C')}&page = {page}&per_page = {redis_bot.get('hits')}&client_id={redis_reg.get('tokenspl')}"
    r = httpx.get(url, headers= {"User-Agent": f"{UserAgent().random}"}, follow_redirects=True)
    print(f"Spl status: {r.status_code}")
    if r.status_code == 200:
        rspl = r.json()
        if rspl['total'] == 0:
            await bot.send_message(chat_id=message.message.chat.id, reply_markup=exception_kb(message), 
                                    text=f"❗ <i>{rspl['total']}</i> доступных фото из <b>Unsplash</b>.\
                                    \n\n{'Попробуй другой сервис, либо измени запрос! 🔎' if message.data != 'all' else ''}")
            if message.data != 'splash': return False
        else:
            if rspl['total'] >= int(redis_bot.get('hits')):
                await bot.send_message(chat_id=message.message.chat.id, text=f"✔️ Доступно <i>{rspl['total']}</i> фото из <b>Unsplash</b>",
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton(text="Перейти на Unsplash с данным запросом", 
                                                                          url=f"https://unsplash.com/s/photos/{redis_bot.get('req')}")]]))
                for photo in range(int(redis_bot.get('hits'))):
                    await sleep(1.1)
                    await bot.send_photo(chat_id=message.from_user.id, photo=rspl["results"][photo]["urls"]["small"], 
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo"), 
                                                                                            InlineKeyboardButton(text="Подробнее ⇑", url=rspl["results"][photo]["links"]["html"])]]))
                if message.data == 'splash':
                    await bot.send_message(chat_id=message.message.chat.id, reply_markup=exception_kb(message), 
                                            text="Можешь выбрать другой сервис либо изменить <b>Запрос</b> 🔎, а также перейти в раздел <b>Информация</b> 📖")
            else:
                await bot.send_message(chat_id=message.message.chat.id, text=f"✔️ Available only <i>{rspl['total']}</i> photos from <b>Unsplash</b>",
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton(text="Перейти на Unsplash с данным запросом", 
                                                                          url=f"https://unsplash.com/s/photos/{redis_bot.get('req')}")]]))
                for photo in range(rspl['total']):
                    await sleep(1.1)
                    await bot.send_photo(chat_id=message.from_user.id, photo=rspl["results"][photo]["urls"]["small"], 
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton(text="❌", callback_data="delete_photo"), 
                                                     InlineKeyboardButton(text="Подробнее ⇑", url=rspl["results"][photo]["links"]["html"])]]))
                if message.data == 'splash':
                    await bot.send_message(chat_id=message.message.chat.id, reply_markup=exception_kb(message), 
                                            text="Можешь выбрать другой сервис либо изменить <b>Запрос</b> 🔎, а также перейти в раздел <b>Информация</b> 📖")
    else:
        if message.data == 'splash': 
            await bot.send_message(chat_id=message.message.chat.id, reply_markup=istart_kb(),
                            text=f"❗ Во время поиска на <b>Unsplash</b> возникла ошибка: <i>{r.status_code}</i>\n\nСообщи об этом техподдержке!")
        else: return False


@parse_router.callback_query(F.data == "all")
async def parsall(message: types.CallbackQuery):
    await message.answer() 
    await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)  
    if await parspix(message) == False:
        if await parspex(message) == False:
            if await parsunspl(message) == False:
                await bot.send_message(chat_id=message.message.chat.id, 
                                       text=f"❗ К сожалению, ни один из сервисов не смог найти что-либо по запросу: {redis_bot.get('req')}")
                await sleep(2)
                for i in range(1,5):
                    try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+i)
                    except: pass
        else:
            if await parsunspl(message) == False:
                pass
            pass
    else:
        if await parspex(message) == False:
            if await parsunspl(message) == False:
                pass
            pass
        else:
            if await parsunspl(message) == False:
                pass
    await bot.send_message(chat_id=message.message.chat.id, reply_markup=istart_kb(),
                            text="Можешь изменить запрос либо ознакомиться с информацией")

@parse_router.callback_query(F.data == 'DEMO')
async def demo_mode(call: types.CallbackQuery):
    await call.answer()
    demo: int = coll.find_one({'_id': call.from_user.id})['demo']
    await parspex(call, demo = demo)
    coll.update_one({'_id': call.from_user.id}, {"$set": {'demo': demo-1}})
