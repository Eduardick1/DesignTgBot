from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
# from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from asyncio import sleep
from createBot import bot
from keybords import istartkb, tokenpixurl, tokenpexurl, tokensplurl, amount_unreg_kb
from DataBase import coll, redis
from typing import AnyStr, List

register_router = Router()

class tokenfsm(StatesGroup):
    tokenpix = State()
    tokenpex = State()
    tokenspl = State()


attemptpix: int = 0
attemptpex: int = 0
attemptspl: int = 0

async def get_list_unreg() -> list:
    tokens = ['tokenpix', 'tokenpex', 'tokenspl']
    unreg_tokens = []
    for t in tokens:
        if await redis.get(t) == 'Unregistered':
            unreg_tokens.append(t)
    return unreg_tokens

def get_amount_of_unreg(list: list) -> int:
    return len(list)

async def get_registerText() -> str:
    
    quantity = get_amount_of_unreg(await get_list_unreg())
    if quantity == 3:
        return "<b>Привет, {}</b>\n\nВозможно ты первый раз работаешь с этим ботом\n\nПоэтому для корректной работы и для возможности пользоваться всем функционалом бота, тебе следует настроить <b>API</b> каждого сервиса, тоесть подключить твои аккаунты:\n<i>PixaBay</i>, <i>Pexels</i>, <i>Unsplash</i>\n\nЭта первоначальная настройка займёт от 5 до 10 минут, в дальнейшем тебе не нужно будет этим заниматься, так как бот тебя запомнит\n\nВыбери сервис, с которого хочешь начать" 
    else:
        return "<b>Привет, {}</b>\n\nУ тебя ещё {} незарегестрированных токенов\n\nДля корректной работы и для возможности пользоваться всем функционалом бота, тебе следует настроить оставшиеся <b>API</b>"

async def registerM(message: CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=message.message.chat.id, #type: ignore
                                    message_id=message.message.message_id, #type: ignore
                                    text=str(await get_registerText()).format(message.from_user.first_name, get_amount_of_unreg(await get_list_unreg())),
                                    reply_markup=amount_unreg_kb(await get_list_unreg(), get_amount_of_unreg(await get_list_unreg())))
    except Exception as e:
        print(f"45: {e}")
        await bot.send_message(chat_id=message.message.chat.id, #type: ignore
                            #message_id=message.message.message_id, #type: ignore
                            text=str(await get_registerText()).format(message.from_user.first_name, get_amount_of_unreg(await get_list_unreg())),
                            reply_markup=amount_unreg_kb(await get_list_unreg(), get_amount_of_unreg(await get_list_unreg())))


'''async def registerM(message: Message, state: FSMContext):
    await message.edit_text(text=f"<b>Привет, {}</b>\n\nВозможно ты первый раз работаешь с этим ботом\n\nПоэтому для корректной работы и для возможности пользоваться всем функционалом бота, тебе следует настроить <b>API</b> каждого сервиса, тоесть подключить твои аккаунты:\n<i>PixaBay</i>, <i>Pexels</i>, <i>Unsplash</i>\n\nЭта первоначальная настройка займёт от 5 до 10 минут, в дальнейшем тебе не нужно будет этим заниматься, так как бот тебя запомнит\n\nДавай начнём с <b><i>PixaBay</i></b>\nПо кнопке ниже ты можешь перейти на сайт <b><i>Pixabay</i></b>\n\nПожайлуста, внимательно следуй каждому пункту инструкции:\n<b>1)</b> Нажав на кнопку ниже, ты переходишь по ссылке и попадаешь на документацию по API\n<b>2)</b> В главе <b>'Search Images' -> 'Parameters' -> 'key(required)'</b> твой API выделен зелёным (если ты вошёл на сайт), либо в том же месте будет возможность войти в аккаунт\n<b>3)Скопируй максимально аккуратно, каждый символ\n4)</b> Отправь скопированный API следующим сообщением", # type: ignore
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[tokenpixurl]]))
    await state.set_state(tokenfsm.tokenpix)

@register_router.message(tokenfsm.tokenpix)
async def registerpix(message: Message, state: FSMContext):
    global attemptpix
    if message.text[0] == "/":  # type: ignore
        attemptpix += 2
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text="<b>Токен не может начинаться с символа '<i>/</i>'</b>\n\nВ данный момент ты не можешь воспользоваться командой\nПосле ввода токена ты сможешь воспользоваться полным функционалом бота")
        await sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    elif len(message.text) < 30:  # type: ignore # type: ignore
        attemptpix += 2
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id, text="<b>Токен не похож сам на себя</b>, попробуй ещё раз!")
        await sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    else:
        await state.update_data(tokenpix = str(message.text))
        await bot.send_message(chat_id=message.chat.id,
                                text="Теперь продолжим с <i>Pexels</i>\n\nПо кнопке ниже ты можешь перейти на сайт <i>Pexels</i>\n\nПожайлуста, внимательно следуй каждому пункту инструкции:\n<b>1)</b> Нажав на кнопку ниже, ты переходишь по ссылке и попадаешь на стартовую страницу API\n<b>2)</b> Необходимо нажать на кнопку '<b>Get started</b>' и войти в аккаунт\n<b>3)</b> Далее нужно будет заполнить форму(анкету), думаю ты разберёшься как именно, но желательно, чтобы смысл был в учебных целях\n<b>4)</b> После заполнения тебя перекинет на страницу с твоим API-ключом\n<b>5)</b> Скопируй максимально аккуратно, каждый символ\n6) Отправь скопированный API следующим сообщением",
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[tokenpexurl]]))
        await state.set_state(tokenfsm.tokenpex)

@register_router.message(tokenfsm.tokenpex)
async def registerpex(message: Message, state: FSMContext):
    global attemptpex
    if message.text[0] == "/":  # type: ignore
        attemptpex += 2
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text="<b>Токен не может начинаться с символа '<i>/</i>'</b>\n\nВ данный момент ты не можешь воспользоваться командой\nПосле ввода токена ты сможешь воспользоваться полным функционалом бота")
        await sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    elif len(message.text) < 50:  # type: ignore
        attemptpex += 2
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id, text="<b>Токен не похож сам на себя</b>, попробуй ещё раз!")
        await sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    else:
        await state.update_data(tokenpex = str(message.text))  # register as developer if no acc
        await bot.send_message(chat_id=message.chat.id,
                                text="И наконец <i>Unsplash</i>\n\nПо кнопке ниже ты можешь перейти на сайт <i>Unsplash</i>\n\nПожайлуста, внимательно следуй каждому пункту инструкции:\n<b>1)</b> Нажав на кнопку ниже, ты переходишь по ссылке и попадаешь на стартовую страницу API\n<b>2)</b> Необходимо нажать на кнопку '<b>Register as a Developer</b>' или '<b>Your apps</b>', если ты уже вошёл в аккаунт предварительно\n<b>3)</b> Далее нужно будет нажать <b>New Application</b>\n<b>4)</b> Ставим галочки и читаем соглашение (по возможности)\n<b>5)</b> Следующим шагом будет заполение анкеты как и на предыдущем сайте\n<b>6)</b> После заполнения тебя перекинет на страницу, созданного Application\n<b>7)</b> Теперь скролишь вниз, находишь раздел '<b>Keys</b>', в котором копируешь '<b><i>Access-Key</i></b>', это и есть необходимый API\n<b>5)</b> Скопируй максимально аккуратно, каждый символ\n<b>6)</b> Отправь скопированный API следующим сообщением",
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[tokensplurl]]))
        await state.set_state(tokenfsm.tokenspl)

@register_router.message(tokenfsm.tokenspl)
async def registersplall(message: Message, state: FSMContext):
    global attemptspl, attemptpix, attemptpex
    if message.text[0] == "/":  # type: ignore
        attemptspl += 2
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text="<b>Токен не может начинаться с символа '<i>/</i>'</b>\n\nВ данный момент ты не можешь воспользоваться командой\nПосле ввода токена ты сможешь воспользоваться полным функционалом бота")
        await sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    elif len(message.text) < 40:  # type: ignore
        attemptspl += 2
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id, text="<b>Токен не похож сам на себя</b>, попробуй ещё раз!")
        await sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    else:
        await state.update_data(tokenspl = str(message.text))
        data = await state.get_data()
        coll.update_one({'_id': message.from_user.id}, {"$set": {'tokenpix': data['tokenpix'], #type:ignore
                                                                'tokenpex': data['tokenpex'],
                                                                'tokenspl': data['tokenspl']}})
        await bot.send_message(chat_id=message.chat.id,
                                text="Думаю всё прошло успешно\n\nТеперь перед тобой открыт весь функционал бота!\n\nЕсли в дальнейшем возникнут трудности или ошибки, можешь обратиться к техподдержке для проверки корректности ваших API", 
                                reply_markup=istartkb)
        # print(f"attempts pix :{attemptpix}")
        # print(f"attempts pex :{attemptpex}")
        # print(f"attempts spl :{attemptspl}")
        # print(f"Message to delete {message.message_id-(attemptpix+attemptpex+attemptspl)-5} = {message.message_id} - ({attemptpix}+{attemptpex}+{attemptspl}) - 5)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - (
                attemptpix + attemptpex + attemptspl) - 5)  # инфа о пикс
        # print(f"Message to delete {message.message_id-(attemptpex+attemptspl)-4}")
        await bot.delete_message(chat_id=message.chat.id,
                                    message_id=message.message_id - (attemptpex + attemptspl) - 4)  # api pix
        # print(f"Message to delete {message.message_id-(attemptpex+attemptspl)-3}")
        await bot.delete_message(chat_id=message.chat.id,
                                    message_id=message.message_id - (attemptpex + attemptspl) - 3)  # info pex
        # print(f"Message to delete {message.message_id-(attemptspl)-2}")
        await bot.delete_message(chat_id=message.chat.id,
                                    message_id=message.message_id - (attemptspl) - 2)  # api pex
        # print(f"Message to delete {message.message_id-(attemptspl)-1}")
        await bot.delete_message(chat_id=message.chat.id,
                                    message_id=message.message_id - (attemptspl) - 1)  # info spl
        # print(f"Message to delete {message.message_id}")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # api spl
        attemptspl = 0
        attemptpix = 0
        attemptpex = 0'''