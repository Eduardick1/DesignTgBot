from createBot import bot
from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
#from googletrans import Translator
from keybords import cancelkb, istartkb, exception_kb, typeskb
from commands import startC, startM
from registration import registerM
from asyncio import sleep
import httpx #requests
from fake_useragent import UserAgent
from DataBase import redis
#import logging

parse_router = Router()
Headers = {"User-Agent": f"{UserAgent().random}"}

class FSM_(StatesGroup):
    req = State() 
    hits = State()

attemptreq: int = 0
attempthit: int = 0



@parse_router.callback_query(F.data == "cancel")
async def CcancelFSM(message: types.CallbackQuery, state: FSMContext):
    global attemptreq, attempthit
    await message.answer()
    try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)#type:ignore
    except Exception as e: 
        print(f"32: {e}")
        pass
    try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+1)#type:ignore
    except Exception as e: 
        print(f"36: {e}")
        pass
    curState = await state.get_state()
    if curState == None:
        return await startC(message)
    else:
        await bot.send_message(chat_id=message.message.chat.id, #type:ignore 
                                    text="Отменено!")
        await state.clear()
        if curState[-1] == "q":
            try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+attemptreq+2)#type:ignore 
            except Exception as e:
                print(f"Parser 42: {e}")
                pass
        elif curState[-1] == "s":   
            try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+attemptreq+3)#type:ignore 
            except Exception as e: 
                print(f"Parser 47: {e}")
                pass 
            try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+attemptreq+2)#type:ignore 
            except Exception as e: 
                print(f"Parser 51: {e}")
                pass 
            try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+1)#type:ignore 
            except Exception as e: 
                print(f"Parser 55: {e}")
                pass 
            try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)#type:ignore  
            except Exception as e: 
                print(f"Parser 59: {e}")
                pass 
            try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+attemptreq+attempthit+4)#type:ignore 
            except Exception as e: 
                print(f"Parser 63: {e}")
                pass 
        await startC(message)
    attemptreq = 0
    attempthit = 0
 

@parse_router.message(F.text.lower().contains("отмен") | F.text.lower().contains("cancel"))
async def McancelFSM(message: types.Message, state: FSMContext):
    global attemptreq, attempthit
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    curState = await state.get_state()
    if curState == None:
        return
    else:
        await state.clear()
        if curState[-1] == "q":
            try:await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attemptreq-2)
            except Exception as e:
                print(f"Parser 84: {e}")
                pass
            try:await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attemptreq-1)
            except Exception as e:
                print(f"Parser 88: {e}")
                pass
        elif curState[-1] == "s":   
            try:await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attemptreq-attempthit-4)
            except Exception as e:
                print(f"Parser 93: {e}")
                pass
            try:await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attemptreq-attempthit-3)
            except Exception as e:
                print(f"Parser 97: {e}")
                pass
            try:await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attempthit-2)
            except Exception as e:
                print(f"Parser 101: {e}")
                pass
            try:await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attempthit-1)
            except Exception as e:
                print(f"Parser 105: {e}")
                pass
        await bot.send_message(chat_id=message.chat.id, 
                               text="Отменено!")
        await sleep(1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)#type:ignore
        await startM(message) 
    attemptreq = 0
    attempthit = 0


@parse_router.message(F.text.lower().contains("поиск") | F.text.lower().contains("search"))
async def searchM(message: types.Message, state: FSMContext): 
    try: await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
    except Exception as e:
        print(f"Parser 124: {e}")
        pass
    try: await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print(f"Parser 128: {e}")
        pass
    await bot.send_message(chat_id=message.chat.id, 
                            text="В любой момент можешь воспользоваться командой <b>'Отмена'</b>",  reply_markup=cancelkb)
    await state.set_state(FSM_.req)
    await bot.send_message(chat_id=message.chat.id, 
                            text="Для поиска фото, придумай ключевые слова(теги):")


@parse_router.callback_query(F.data == "search")
async def searchC(message: types.CallbackQuery, state: FSMContext):
    await message.answer()
    try: await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)#type:ignore
    except Exception as e:
        print(f"Parser 142: {e}")
        pass
    await bot.send_message(chat_id=message.message.chat.id,#type:ignore 
                            text="В любой момент можешь воспользоваться командой <b>'Отмена'</b>", 
                            reply_markup=cancelkb)
    await state.set_state(FSM_.req)
    await bot.send_message(chat_id=message.message.chat.id, #type:ignore
                            text="Для поиска фото, придумай ключевые слова(теги):") 
    

#==================================================================================================================================================================

@parse_router.message(FSM_.req)
async def collect_request(message: types.Message, state: FSMContext):
    #translator = Translator()
    global attemptreq
    if message.text[0] == "/": #type:ignore
        attemptreq += 2
        await message.delete()
        await bot.send_message(chat_id=message.chat.id, 
                               text="Запрос не может начинаться с символа '<i>/</i>' Если хочешь воспользоваться командой, для начала нажми кнопку '<b>ОТМЕНА</b>'!")
        await sleep(1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)#type:ignore
    else:
        await state.update_data(req = str(message.text))
        await redis.set('req', str(message.text))
        await state.set_state(FSM_.hits)
        await bot.send_message(chat_id=message.chat.id, 
                               text="Введи количество необходимых медиа:")


@parse_router.message(FSM_.hits) #ПОДУМАТЬ НА РЕФАКТОРИНГОМ
async def collect_hits(message: types.Message, state: FSMContext):
    global attempthit, attemptreq
    try:
        if int(message.text) < 1: #type:ignore
            raise ValueError
        else:
            await redis.set('hits', int(message.text)) #type:ignore
            print(f"Hits: {await redis.get('hits')}")
            await state.clear()
            await bot.send_message(chat_id=message.chat.id, 
                                   text=f"Выбери тип медиа:", reply_markup=await typeskb())
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attemptreq-attempthit-4)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attemptreq-attempthit-3)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attempthit-2)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-attempthit-1)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            attempthit = 0
            attemptreq = 0
    except ValueError:
        attempthit += 2
        await message.delete()
        await bot.send_message(chat_id=message.chat.id, 
                               text="<b>Проверь вводимое число!</b>\n\nКак минимум оно должно быть целым и больше 0 !")
        await sleep(1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)#type:ignore
    except Exception as e:
        print(f"Parser 158-173(179): {e}")
        pass

@parse_router.callback_query(F.data == "typeall")
async def typeall(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, #type:ignore
                                text=f"<b>Твой запрос:</b>\n<i>{await redis.get('req')}</i>\n\n<b>Количество фото:</b> <i>{await redis.get('hits')}</i>\n\nВыбери сервис, с которого хочешь получить медиа:",
                                 reply_markup=await exception_kb(message)) #type:ignore


@parse_router.callback_query((F.data == "vector") | (F.data == "illustration"))
async def typeother(message: types.CallbackQuery):
    await message.answer()
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,  #type:ignore
                                    text=f"<b>Твой запрос:</b>\n<i>{await redis.get('req')}</i>\n\n<b>Количество фото:</b> <i>{await redis.get('hits')}</i>\n\n<b>Тип медиа:</b> <i>{message.data}</i>\n\nМедиа будут предоставлены сервисом PixaBay")
    await parspix(message, type = message.data)


@parse_router.callback_query(F.data == "pixabay")
async def parspix(message: types.CallbackQuery, type = "all"):
    if message.data == "pixabay":
        await message.answer()
    try:
        await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id) #type:ignore 
    except Exception as e:
        print(f"Parser 213: {e}")
        pass
    if await redis.get("tokenpix") == "Unregistered":
        await registerM(message)#type:ignore
    else: 
        url = f"https://pixabay.com/api/?key={await redis.get('tokenpix')}&q={str(await redis.get('req')).replace(',', '%2C')}&image_type = {type}&per_page = {int(await redis.get('hits')) if int(await redis.get('hits'))>2 else 3}" 
        r = httpx.get(url, headers = Headers, follow_redirects=True)
        print(r)
        print(f"Pix status: {r.status_code}")
        if r.status_code == 200:
            rpix = r.json()
            if rpix["total"] == 0:
                await bot.send_message(chat_id=message.message.chat.id, #type:ignore
                                    text=f"<i>{rpix['total']}</i> фото доступно из <b>PixaBay</b>.\n\n{'Попробуй другой сервис, либо измени запрос!' if message.data != 'all' else ''}",  
                                        reply_markup=await exception_kb(message))
                if message.data == "all":
                    return False
                #else:
                    #await sleep(15)
                    #try:
                    #    await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+1)#type:ignore 
                    #except Exception as e:
                    #    print(f"Parser 228: {e}")
                    #    pass
            else:
                if rpix['total'] >= int(await redis.get('hits')):
                    await bot.send_message(chat_id=message.message.chat.id,#type:ignore 
                                        text=f"Доступно <i>{rpix['total']}</i> фото из <b>PixaBay</b>",  
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти на PixaBay с данным запросом", 
                                                                                                                        url=f"https://pixabay.com/photos/search/{await redis.get('req')}/")]]))
                    for photo in range(int(await redis.get('hits'))):
                        await sleep(1.1)
                        await bot.send_photo(chat_id=message.from_user.id, 
                                            photo=rpix["hits"][photo]["webformatURL"],
                                            caption=f"{rpix['hits'][photo]['webformatWidth']}x{rpix['hits'][photo]['webformatHeight']}", 
                                            reply_markup= InlineKeyboardMarkup( 
                                            inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo"), 
                                                            InlineKeyboardButton(text="⬆ Подробнее о фото", 
                                                                                    url=rpix["hits"][photo]["pageURL"])]]))
                    if message.data != "all":
                        await bot.send_message(chat_id=message.message.chat.id, #type:ignore
                                            text="Можешь изменить запрос, а также перейти в раздел информации",  
                                                reply_markup=await exception_kb(message))
                else:
                    await bot.send_message(chat_id=message.message.chat.id, #type:ignore
                                        text=f"Доступно только <i>{rpix['total']}</i> фото из <b>PixaBay</b>", 
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти на PixaBay с данным запросом", 
                                                                                                                    url=f"https://pixabay.com/photos/search/{await redis.get('req')}/")]]))
                    for photo in range(rpix['total']):
                        await sleep(1.1)
                        await bot.send_photo(chat_id=message.from_user.id, 
                                            photo=rpix["hits"][photo]["webformatURL"],
                                            caption=f"{rpix['hits'][photo]['webformatWidth']}x{rpix['hits'][photo]['webformatHeight']}", 
                                            reply_markup= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo")], 
                                                                                                [InlineKeyboardButton(text="⬆ Подробнее о фото", 
                                                                                                                    url=rpix["hits"][photo]["pageURL"])]]))
                    if message.data != "all":
                        await bot.send_message(chat_id=message.message.chat.id, #type:ignore
                                            text="Можешь выбрать другой сервис либо изменить запрос, а также перейти в раздел информации",  
                                        reply_markup=await exception_kb(message))
        else:
            await bot.send_message(chat_id=message.message.chat.id, #type:ignore
                                text=f"Во время поиска на <b>PixaBay</b> возникла ошибка: <i>{r.status_code}</i>\n\nСообщи об этом техподдержке!",  
                                            
                                            reply_markup=istartkb)
            if message.data == "all":
                return False
            #else:
            #    await sleep(15)
            #    try:
            #        await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+1)#type:ignore  
            #    except Exception as e:
            #        print(f"Parser 279: {e}")
            #        pass


@parse_router.callback_query(F.data == "pexel")
async def parspex(message: types.CallbackQuery):
    if message.data == "pexel":
        await message.answer()
        try:
            await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)#type:ignore
        except Exception as e:
            print(f"Parser 295: {e}")
            pass
    if await redis.get("tokenpex") == "Unregistered":
        await registerM(message)#type:ignore
    else: 
        PexHeaders = Headers.copy()
        PexHeaders.update({"Authorization":await redis.get('tokenpex')}) 
        url = f"https://api.pexels.com/v1/search?query={str(await redis.get('req')).replace(',', '%2C')}&per_page = {await redis.get('hits')}"
        r = httpx.get(url, headers = PexHeaders, follow_redirects=True)
        print(r)
        print(f"Pex status: {r.status_code}")
        if r.status_code == 200:
            rpex = r.json()
            if rpex['total_results'] == 0:
                await bot.send_message(chat_id=message.message.chat.id,  #type:ignore
                                    text=f"<i>{rpex['total_results']}</i> доступных фото из <b>Pexels</b>.\n\n{'Попробуй другой сервис, либо измени запрос!' if message.data != 'all' else ''}", 
                                        
                                    reply_markup=await exception_kb(message))
                if message.data == "all":
                    return False
                #else:
                #    await sleep(15)
                #    try:
                #        await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+1)#type:ignore 
                #    except Exception as e:
                #        print(f": {e}")
                #        pass
            else:
                if rpex['total_results'] >= int(await redis.get('hits')):
                    await bot.send_message(chat_id=message.message.chat.id,  #type:ignore
                                        text=f"Доступно <i>{rpex['total_results']}</i> фото из <b>Pexels</b>",
                                        
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти на Pexels с данным запросом", 
                                                                                                                    url=f"https://www.pexels.com/search/{await redis.get('req')}/")]]))
                    for photo in range(int(await redis.get('hits'))):
                        await sleep(1.1)
                        await bot.send_photo(chat_id=message.from_user.id, 
                                            photo=rpex["photos"][photo]["src"]["large"],
                                            reply_markup= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo")], 
                                                                                                [InlineKeyboardButton(text="⬆ Подробнее о фото", 
                                                                                                                    url=rpex["photos"][photo]["url"])]]))
                    if message.data != 'all':
                        await bot.send_message(chat_id=message.message.chat.id,  #type:ignore
                                            text="Можешь выбрать другой сервис либо изменить запрос, а также перейти в раздел информации", 
                                            reply_markup=await exception_kb(message))
                else:
                    await bot.send_message(chat_id=message.message.chat.id, #type:ignore 
                                        text=f"Доступно только <i>{rpex['total_results']}</i> фото из <b>Pexels</b>",
                                        
                                        reply_markup=InlineKeyboardMarkup( 
                                        inline_keyboard=[[InlineKeyboardButton(text="Перейти на Pexels с данным запросом",
                                                                                url=f"https://www.pexels.com/search/{await redis.get('req')}/")]]))
                    for photo in range(rpex['total_results']):
                        await sleep(1.1)
                        await bot.send_photo(chat_id=message.from_user.id, 
                                            photo=rpex["photos"][photo]["src"]["large"],
                                            reply_markup= InlineKeyboardMarkup( 
                                            inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo"), 
                                                            InlineKeyboardButton(text="⬆ Подробнее о фото", 
                                                                                    url=rpex["photos"][photo]["url"])]]))
                    if message.data != 'all':
                        await bot.send_message(chat_id=message.message.chat.id,  #type:ignore
                                            text="Можешь выбрать другой сервис либо изменить запрос, а также перейти в раздел информации", 
                                            reply_markup=await exception_kb(message))
        else:
            await bot.send_message(chat_id=message.message.chat.id, #type:ignore
                                text=f"Во время поиска на <b>Pexels</b> возникла ошибка: <i>{r.status_code}</i>\n\nСообщи об этом техподдержке!", 
                                    reply_markup=istartkb)
            if message.data == "all":
                return False
            #else:
            #    await sleep(15)
            #    try:
            #        await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+1)#type:ignore  
            #    except Exception as e:
            #        print(f"Parser 367: {e}")
            #        pass


@parse_router.callback_query(F.data == "splash")
async def parsunspl(message: types.CallbackQuery, page = 1): #max hits is 30
    if message.data == "splash":
        await message.answer()
        try:
            await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)#type:ignore 
        except Exception as e:
            print(f"Parser 379: {e}")
            pass
    if await redis.get("tokenspl") == "Unregistered":
        await registerM(message)#type:ignore
    else: 
        url = f"https://api.unsplash.com/search/photos?query={str(await redis.get('req')).replace(' ', '-').replace(',', '%2C')}&page = {page}&per_page = {await redis.get('hits')}&client_id={await redis.get('tokenspl')}"
        r = httpx.get(url, headers=Headers, follow_redirects=True)
        print(r)
        print(f"Spl status: {r.status_code}")
        if r.status_code == 200:
            rspl = r.json()
            if rspl['total'] == 0:
                await bot.send_message(chat_id=message.message.chat.id, #type:ignore 
                                    text=f"<i>{rspl['total']}</i> доступных фото из <b>Unsplash</b>.\n\n{'Попробуй другой сервис, либо измени запрос!' if message.data != 'all' else ''}", 
                                        reply_markup=await exception_kb(message))
                if message.data == "all":
                    return False
                #else:
                #    await sleep(15)
                #    try:
                #        await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+1)#type:ignore 
                #    except Exception as e:
                #        print(f"Parser 401: {e}")
                #        pass
            else:
                if rspl['total'] >= int(await redis.get('hits')):
                    await bot.send_message(chat_id=message.message.chat.id,  #type:ignore
                                        text=f"Доступно <i>{rspl['total']}</i> фото из <b>Unsplash</b>",
                                                
                                                reply_markup=InlineKeyboardMarkup(
                                                inline_keyboard=[[InlineKeyboardButton(text="Перейти на Unsplash с данным запросом", 
                                                                                    url=f"https://unsplash.com/s/photos/{await redis.get('req')}")]]))
                    for photo in range(int(await redis.get('hits'))):
                        await sleep(1.1)
                        await bot.send_photo(chat_id=message.from_user.id,
                                            photo=rspl["results"][photo]["urls"]["small"], 
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo"), 
                                                                                                InlineKeyboardButton(text="⬆ Подробнее о фото", 
                                                                                    url=rspl["results"][photo]["links"]["html"])]]))
                    if message.data != "all":
                        await bot.send_message(chat_id=message.message.chat.id, #type:ignore 
                                            text="Можешь выбрать другой сервис либо изменить запрос, а также перейти в раздел информации", 
                                        reply_markup=await exception_kb(message))
                else:
                    await bot.send_message(chat_id=message.message.chat.id, #type:ignore 
                                        text=f"Available only <i>{rspl['total']}</i> photos from <b>Unsplash</b>",
                                                
                                                reply_markup=InlineKeyboardMarkup(
                                                inline_keyboard=[[InlineKeyboardButton(text="Перейти на Unsplash с данным запросом", 
                                                                                    url=f"https://unsplash.com/s/photos/{await redis.get('req')}")]]))
                    for photo in range(rspl['total']):
                        await sleep(1.1)
                        await bot.send_photo(chat_id=message.from_user.id,
                                            photo=rspl["results"][photo]["urls"]["small"], 
                                            reply_markup=InlineKeyboardMarkup(
                                            inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delete_photo"), 
                                                            InlineKeyboardButton(text="⬆ Подробнее о фото", 
                                                                                    url=rspl["results"][photo]["links"]["html"])]]))
                    if message.data != "all":
                        await bot.send_message(chat_id=message.message.chat.id,#type:ignore  
                                            text="Можешь выбрать другой сервис либо изменить запрос, а также перейти в раздел информации", 
                                        reply_markup=await exception_kb(message))
        else:
            await bot.send_message(chat_id=message.message.chat.id,#type:ignore
                               text=f"Во время поиска на <b>Unsplash</b> возникла ошибка: <i>{r.status_code}</i>\n\nСообщи об этом техподдержке!", 
                                         
                                        reply_markup=istartkb)
            if message.data == "all":
                return False
            #else:
            #    await sleep(15)
            #    try:
            #        await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+1)#type:ignore  
            #    except Exception as e:
            #        print(f"Parser 454: {e}")
            #        pass


@parse_router.callback_query(F.data == "all")
async def parsall(message: types.CallbackQuery): #кажется иногда криво работает с неточными! запросами
    await message.answer() 
    print(f"Req = {await redis.get('req')}")
    print(message.data)  
    if await parspix(message) == False:
        if await parspex(message) == False:
            if await parsunspl(message) == False:
                await bot.send_message(chat_id=message.message.chat.id, #type:ignore 
                                       text=f"К сожалению ни один из сервисов не смог найти что-либо по запросу: {await redis.get('req')}\n\nВведи новый запрос и повтори ещё раз!", 
                                        reply_markup=istartkb)
                await sleep(2)
                await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+1)#type:ignore 
                await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+2)#type:ignore 
                await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id+3)#type:ignore 
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
    await bot.send_message(chat_id=message.message.chat.id,#type:ignore 
                            text="Можешь изменить запрос либо ознакомиться с информацией", 
                            reply_markup=istartkb)

