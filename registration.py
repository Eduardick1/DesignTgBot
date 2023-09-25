from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from keybords import unreg_kb, get_reg
from DataBase import coll, redis_reg, redis_bot
from createBot import bot, tokenfsm
from asyncio import sleep


register_router = Router()


def get_registerText() -> str:
    
    if len(get_reg()) == 0:
        return "Привет, {}\n\nВозможно ты первый раз работаешь с этим ботом\
                \n\nТебе следует настроить API каждого сервиса, тоесть подключить твои аккаунты для корректной работы и для возможности пользоваться всем функционалом бота, :\
                \n <i>PixaBay</i>, <i>Pexels</i>, <i>Unsplash</i>\
                \n\nЭта первоначальная настройка займёт от 5 до 10 минут, в дальнейшем тебе не нужно будет этим заниматься, так как бот тебя запомнит\
                \n\nВыбери сервис, с которого хочешь начать" 
    else:
        return "Привет, {}\n\nУ тебя ещё есть незарегестрированные токены\
                \n\nДля корректной работы и для возможности пользоваться всем функционалом бота, тебе следует настроить оставшиеся сервисы"


@register_router.callback_query(F.data == 'registration')
async def register(call: CallbackQuery):
    call.answer()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                    text=get_registerText().format(call.from_user.first_name),
                                    reply_markup=unreg_kb())


@register_router.callback_query(F.data == 'pix_reg')
async def start_reg_pix(call: CallbackQuery, state: FSMContext):
    call.answer()
    d=await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, 
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="PixaBay", url="https://pixabay.com/api/docs/")]]), 
                                text=f"<i>PixaBay</i>\
                                    \n\nПо кнопке ниже ты можешь перейти на сайт <i>Pixabay</i>\
                                    \nПожайлуста, внимательно следуй каждому пункту инструкции:\
                                    \n\n1) Нажав на кнопку ниже, ты переходишь по ссылке и попадаешь на документацию по API\
                                    \n2) Переходим по главам 'Search Images' -> 'Parameters' -> 'key(required)'\
                                    \n3) Твой API выделен зелёным (если ты вошёл на сайт), либо в том же месте будет возможность войти в аккаунт\
                                    \n4) Скопируй максимально аккуратно, каждый символ\
                                    \n5) Отправь скопированный API следующим сообщением")
    redis_bot.sadd('todelete', d.message_id)
    await state.set_state(tokenfsm.tokenpix)

@register_router.message(tokenfsm.tokenpix, F.content_type == 'text')
async def reg_pix(message: Message, state: FSMContext):
    if message.text[0] == "/" or len(message.text) != 34: #Отредактировать тексты
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        d=await message.answer(text="Токен не похож сам на себя, попробуй ещё раз!\
                                \n\nПосле ввода токена ты сможешь воспользоваться полным функционалом бота")
        await sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=d.message_id)
    else:
        redis_reg.set('tokenpix', message.text)  
        coll.update_one({'_id': message.from_user.id}, {"$set": {'tokenpix': message.text}})
        await bot.delete_message(chat_id=message.chat.id, message_id=int(redis_bot.spop('todelete')))
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await state.clear()
        await message.answer(reply_markup=unreg_kb(), 
                            text=f"Токен успешно зарегестрирован!\
                                \n\nТеперь можешь свободно пользоваться сервисом Pixabay\
                                \n\nПо кнопке 'Exit' выйдешь в главное меню\
                                \n\n{'Либо можешь продолжить регистрацию токенов, выбрав сервис ниже' if len(get_reg()) < 3 else ''}")    


@register_router.callback_query(F.data == 'pex_reg')
async def start_reg_pex(call: CallbackQuery, state: FSMContext):
    call.answer()
    d=await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Pexels", url="https://www.pexels.com/api/")]]),
                                text = "<i>Pexels</i>\
                                    \n\nПо кнопке ниже ты можешь перейти на сайт <i>Pexels</i>\
                                    \n\nПожайлуста, внимательно следуй каждому пункту инструкции:\
                                    \n1) Нажав на кнопку ниже, ты переходишь по ссылке и попадаешь на стартовую страницу API\
                                    \n2) Необходимо нажать на кнопку 'Get started' и войти в аккаунт\
                                    \n3) Далее нужно будет заполнить форму(анкету), думаю ты разберёшься как именно, но желательно, чтобы смысл был в учебных целях\
                                    \n4) После заполнения тебя перекинет на страницу с твоим API-ключом\
                                    \n5) Скопируй максимально аккуратно, каждый символ\
                                    \n6) Отправь скопированный API следующим сообщением")
    redis_bot.sadd('todelete', d.message_id)
    await state.set_state(tokenfsm.tokenpex)    

@register_router.message(tokenfsm.tokenpex, F.content_type == 'text')
async def reg_pex(message: Message, state: FSMContext):
    
    if message.text[0] == "/" or len(message.text) != 56:  #Отредактировать тексты
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        d=await bot.send_message(chat_id=message.chat.id,
                               text="Токен не похож сам на себя, попробуй ещё раз!\
                                \n\nПосле ввода токена ты сможешь воспользоваться полным функционалом бота")
        await sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=d.message_id)
    else:
        redis_reg.set('tokenpex', message.text)  
        coll.update_one({'_id': message.from_user.id}, {"$set": {'tokenpex': message.text}})
        await bot.delete_message(chat_id=message.chat.id, message_id=int(redis_bot.spop('todelete')))
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await state.clear()
        await message.answer(reply_markup=unreg_kb(), 
                            text=f"Токен успешно зарегестрирован!\
                                \n\nТеперь можешь свободно пользоваться сервисом Pexels\
                                \n\nПо кнопке 'Exit' выйдешь в главное меню\
                                \n\n{'Либо можешь продолжить регистрацию токенов, выбрав сервис ниже' if len(get_reg()) < 3 else ''}") 
          

@register_router.callback_query(F.data == 'spl_reg')
async def start_reg_spl(call: CallbackQuery, state: FSMContext):
    call.answer()
    d=await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Unsplash", url="https://unsplash.com/developers")]]),
                                text="<i>Unsplash</i>\
                                    \n\nПожайлуста, внимательно следуй каждому пункту инструкции:\
                                    \n\nПо кнопке ниже ты можешь перейти на сайт <i>Unsplash</i>\
                                    \n1) Нажав на кнопку ниже, ты переходишь по ссылке и попадаешь на стартовую страницу API\
                                    \n2) Необходимо нажать на кнопку 'Register as a Developer' или 'Your apps', если ты уже вошёл в аккаунт предварительно\
                                    \n3) Далее нужно будет нажать New Application\
                                    \n4) Ставим галочки и читаем соглашение (по возможности)\
                                    \n5) Следующим шагом будет заполение анкеты как и на предыдущем сайте\
                                    \n6) После заполнения тебя перекинет на страницу, созданного Application\
                                    \n7) Теперь скролишь вниз, находишь раздел 'Keys', в котором копируешь '<i>Access-Key</i>', это и есть необходимый API\
                                    \n8) Скопируй максимально аккуратно, каждый символ\
                                    \n9) Отправь скопированный API следующим сообщением")
    redis_bot.sadd('todelete', d.message_id)
    await state.set_state(tokenfsm.tokenspl)    

@register_router.message(tokenfsm.tokenspl, F.content_type == 'text')
async def reg_spl(message: Message, state: FSMContext):
    if message.text[0] == "/" or len(message.text) != 43:  #Отредактировать тексты
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        d=await bot.send_message(chat_id=message.chat.id,
                               text="Токен не похож сам на себя, попробуй ещё раз!\
                                \n\nПосле ввода токена ты сможешь воспользоваться полным функционалом бота")
        await sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=d.message_id)
    else:
        redis_reg.set('tokenspl', message.text)  
        coll.update_one({'_id': message.from_user.id}, {"$set": {'tokenspl': message.text}})
        await bot.delete_message(chat_id=message.chat.id, message_id=int(redis_bot.spop('todelete')))
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await state.clear()
        await message.answer(reply_markup=unreg_kb(),
                             text=f"Токен успешно зарегестрирован!\
                                \n\nТеперь можешь свободно пользоваться сервисом Unsplash\
                                \n\nПо кнопке 'Exit' выйдешь в главное меню\
                                \n\n{'Либо можешь продолжить регистрацию токенов, выбрав сервис ниже' if len(get_reg()) < 3 else ''}")