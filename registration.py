from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from DataBase import coll, redis_reg, redis_bot
from keybords import unreg_kb, get_reg
from createBot import bot, tokenfsm

from asyncio import sleep


register_router = Router()


#====================🢃🢃🢃===FSM_REGISTERING_PIXABAY_token===🢃🢃🢃=====================================================================================================================

@register_router.callback_query(F.data == 'pix_reg')
async def start_reg_pix(callback: CallbackQuery, state: FSMContext):
    callback.answer()
    d=await bot.edit_message_text(message_id=callback.message.message_id, chat_id=callback.message.chat.id, 
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="PixaBay", url="https://pixabay.com/api/docs/")]]), 
                                text=f"<i>PixaBay</i>\
                                    \n\nПо кнопке ниже ты можешь перейти на сайт <i>Pixabay</i>\
                                    \n<b>Пожайлуста, внимательно следуй каждому пункту инструкции:</b>↴\
                                    \n\n<i>1</i>) Нажав на кнопку ниже, ты попадаешь на документацию по API\
                                    \n<i>2</i>) Переходим по главам '<i>Search Images</i>' --> '<i>Parameters</i>' --> '<i>key(required)</i>'\
                                    \n<i>3</i>) Твой API выделен зелёным (если ты вошёл на сайт), либо в том же месте будет возможность войти в аккаунт\
                                    \n<i>4</i>) <b>Скопируй максимально аккуратно, каждый символ</b>\
                                    \n<i>5</i>) Отправь скопированный API следующим сообщением") #ОРФОГРАФИЯ
    redis_bot.sadd('todelete', d.message_id)
    await state.set_state(tokenfsm.tokenpix)

@register_router.message(tokenfsm.tokenpix, F.text)
async def reg_pix(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        if message.text[0] == "/" or len(message.text) != 34: #Отредактировать тексты
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            d=await message.answer(text="<b>Токен не похож сам на себя</b>, попробуй ещё раз")
            await sleep(2)
            await bot.delete_message(chat_id=message.chat.id, message_id=d.message_id)
        else:
            redis_reg.set('tokenpix', message.text)  
            coll.update_one({'_id': message.from_user.id}, {"$set": {'tokenpix': message.text}})
            await bot.delete_message(chat_id=message.chat.id, message_id=int(redis_bot.spop('todelete')))
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await state.clear()
            await message.answer(reply_markup=unreg_kb(), 
                                text=f"<b>Токен успешно зарегестрирован</b>\
                                    \n\nТеперь можешь свободно пользоваться сервисом <i>Pixabay</i>\
                                    \n\nПо кнопке <b>Exit</b> выйдешь в главное меню\
                                    \n\n{'Либо можешь продолжить регистрацию токенов, выбрав сервис ниже' if len(get_reg()) < 3 else ''}")    

#====================🢃🢃🢃===FSM_REGISTERING_PEXELS_token===🢃🢃🢃=====================================================================================================================

@register_router.callback_query(F.data == 'pex_reg')
async def start_reg_pex(callback: CallbackQuery, state: FSMContext):
    callback.answer()
    d=await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Pexels", url="https://www.pexels.com/api/")]]),
                                text = "<i>Pexels</i>\
                                    \n\nПо кнопке ниже ты можешь перейти на сайт <i>Pexels</i>\
                                    \n\n<b>Пожайлуста, внимательно следуй каждому пункту инструкции:</b>↴\
                                    \n<i>1</i>) Нажав на кнопку ниже, ты попадаешь на стартовую страницу API\
                                    \n<i>2</i>) Необходимо нажать на кнопку '<i>Get started</i>' и войти в аккаунт\
                                    \n<i>3</i>) Далее нужно будет заполнить форму(анкету), думаю ты разберёшься как именно, <b>но желательно</b>, чтобы смысл был в 'учебных целях'\
                                    \n<i>4</i>) После заполнения тебя перекинет на страницу с твоим API-ключом\
                                    \n<i>5</i>) <b>Скопируй максимально аккуратно, каждый символ</b>\
                                    \n<i>6</i>) Отправь скопированный API следующим сообщением") #ОРФОГРАФИЯ
    redis_bot.sadd('todelete', d.message_id)
    await state.set_state(tokenfsm.tokenpex)    

@register_router.message(tokenfsm.tokenpex, F.text)
async def reg_pex(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        if message.text[0] == "/" or len(message.text) != 56:  #Отредактировать тексты
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            d=await bot.send_message(chat_id=message.chat.id,
                                text="<b>Токен не похож сам на себя</b>, попробуй ещё раз!\
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
                                text=f"<b>Токен успешно зарегестрирован</b>\
                                    \n\nТеперь можешь свободно пользоваться сервисом <i>Pexels</i>\
                                    \n\nПо кнопке <b>Exit</b> выйдешь в главное меню\
                                    \n\n{'Либо можешь продолжить регистрацию токенов, выбрав сервис ниже' if len(get_reg()) < 3 else ''}") 
          
#====================🢃🢃🢃===FSM_REGISTERING_UNSPLASH_token===🢃🢃🢃=====================================================================================================================

@register_router.callback_query(F.data == 'spl_reg')
async def start_reg_spl(callback: CallbackQuery, state: FSMContext):
    callback.answer()
    d=await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, 
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Unsplash", url="https://unsplash.com/developers")]]),
                                text="<i>Unsplash</i>\
                                    \n\nПо кнопке ниже ты можешь перейти на сайт <i>Unsplash</i>\
                                    \n\n<b>Пожайлуста, внимательно следуй каждому пункту инструкции:</b>↴\
                                    \n<i>1</i>) Нажав на кнопку ниже, ты попадаешь на стартовую страницу API\
                                    \n<i>2</i>) Необходимо нажать на кнопку '<i>Register as a Developer</i>' или '<i>Your apps</i>', если ты вошёл в аккаунт предварительно\
                                    \n<i>3</i>) Далее нужно будет нажать <i>New Application</i>\
                                    \n<i>4</i>) Ставим галочки и читаем соглашение (по возможности)\
                                    \n<i>5</i>) Следующим шагом будет заполнить форму(анкету), думаю ты разберёшься как именно, <b>но желательно</b>, чтобы смысл был в 'учебных целях'\
                                    \n<i>6</i>) После заполнения тебя перекинет на страницу, созданного <i>Application</i>\
                                    \n<i>7</i>) Теперь скролишь вниз, находишь раздел '<i>Keys</i>', в котором копируешь '<i>Access-Key</i>', это и есть необходимый API\
                                    \n<i>8</i>) <b>Скопируй максимально аккуратно, каждый символ</b>\
                                    \n<i>9</i>) Отправь скопированный API следующим сообщением") #ОРФОГРАФИЯ
    redis_bot.sadd('todelete', d.message_id)
    await state.set_state(tokenfsm.tokenspl)    

@register_router.message(tokenfsm.tokenspl, F.text)
async def reg_spl(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        if message.text[0] == "/" or len(message.text) != 43:  #Отредактировать тексты
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            d=await bot.send_message(chat_id=message.chat.id,
                                text="<b>Токен не похож сам на себя</b>, попробуй ещё раз!\
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
                                text=f"<b>Токен успешно зарегестрирован</b>\
                                    \n\nТеперь можешь свободно пользоваться сервисом <i>Unsplash</i>\
                                    \n\nПо кнопке <b>Exit</b> выйдешь в главное меню\
                                    \n\n{'Либо можешь продолжить регистрацию токенов, выбрав сервис ниже' if len(get_reg()) < 3 else ''}")