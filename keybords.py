from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from DataBase import coll, redis_reg as redis


cancelkb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🚮 Отмена", callback_data="cancel")]]) #

def istart_kb():
    searchbut = InlineKeyboardButton(text="🔎 Поиск медиа", callback_data="search")
    infobut = InlineKeyboardButton(text="📖 Инфо", callback_data="info")
    return InlineKeyboardBuilder(markup=[[infobut], [searchbut]]).adjust(2).as_markup()

def get_reg() -> list:
    return [i for i in ['spl','pex','pix'] if redis.get(f'token{i}') != 'Unregistered']

def get_demo_button(id: int) -> InlineKeyboardButton:
    if coll.find_one({'_id': id})['demo'] > 0:
        return [[InlineKeyboardButton(text="Демо-режим", callback_data="DEMO")]]
    return []

def exception_kb(message: CallbackQuery):
    pixbut = InlineKeyboardButton(text="PixaBay", callback_data="pixabay")
    pexelbut = InlineKeyboardButton(text="Pexels", callback_data="pexel")
    splashbut = InlineKeyboardButton(text="Unsplash", callback_data="splash")
    allbut = InlineKeyboardButton(text="Со всех сразу", callback_data="all")
    searchbut = InlineKeyboardButton(text="🔎 Поиск медиа", callback_data="search")
    infobut = InlineKeyboardButton(text="📖 Инфо", callback_data="info")
    
    list_reg: list = get_reg()
    amount = len(list_reg)
    
    def get_markup(list_reg) -> list:
        markup = [[b] for t in list_reg for b in [splashbut, pexelbut, pixbut] if b.callback_data.startswith(t)]
        if amount > 1:
            markup.extend([[allbut]])
        if amount == 0:
            markup.extend(get_demo_button(message.from_user.id))
        if amount < 3:
            markup.extend([[InlineKeyboardButton(text='✏️ Регистрация', callback_data='registration')]])
        if message.data != 'typeall':
            markup.extend([[infobut], [searchbut]])
        return markup
    
    match message.data:
        case "pixabay": 
            try: list_reg.remove('pix')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(2 if amount >= 2 else 1, 1, 2).as_markup() 
        case "pexel": 
            try: list_reg.remove('pex')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(2 if amount >= 2 else 1, 1, 2).as_markup() 
        case "splash":
            try: list_reg.remove('spl')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(2 if amount >= 2 else 1, 1, 2).as_markup() 
        case "illustration":
            try: list_reg.remove('pix')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(2 if amount >= 2 else 1, 1, 2).as_markup() 
        case "vector": 
            try: list_reg.remove('pix')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(2 if amount >= 2 else 1, 1, 2).as_markup() 
        case "all": return None
        case "typeall": return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(amount if amount > 0 else 1,1,amount).as_markup() 


def mainInfo(message: CallbackQuery):
    Infoservicebut = InlineKeyboardButton(text="О сервисах 📚", callback_data="services")
    Inforequestbut = InlineKeyboardButton(text="О запросах 🔎", callback_data="requests")
    Inforegisterbut = InlineKeyboardButton(text="О регистрации ✏️", callback_data="register")
    Infocommandbut = InlineKeyboardButton(text="О командах 💬", callback_data="commands")
    Infoaboutbut = InlineKeyboardButton(text="О возможностях бота 🤖", callback_data="aboutbot")
    searchbt = InlineKeyboardButton(text="🔎 Поиск медиа", callback_data="search")
    
    if message == "info" or message.data == "info": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Inforequestbut], [Infocommandbut], [Inforegisterbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
    match message.data:
        case "services": return InlineKeyboardBuilder(markup=[[Inforequestbut], [Infocommandbut], [Inforegisterbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
        case "commands": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Inforequestbut], [Inforegisterbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
        case "requests": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Infocommandbut], [Inforegisterbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
        case "register": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Inforequestbut], [Infocommandbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
        case "aboutbot": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Inforequestbut], [Infocommandbut], [Inforegisterbut], [searchbt]]).adjust(2,2).as_markup()


def typeskb():
    typeallbut = InlineKeyboardButton(text="Все вместе", callback_data="typeall")
    typephotobut = InlineKeyboardButton(text="Фото", callback_data="typeall")
    typeIllustbut = InlineKeyboardButton(text="Иллюстрации", callback_data="illustration")
    typevectorbut = InlineKeyboardButton(text="Вектор", callback_data="vector")
    if redis.get('tokenpix') == "Unregistered":
        return InlineKeyboardBuilder(markup=[[typephotobut]]).as_markup()
    else:
        return InlineKeyboardBuilder(markup=[[typeIllustbut], [typevectorbut], [typephotobut], [typeallbut]]).adjust(3).as_markup()


def unreg_kb() -> InlineKeyboardMarkup:
    tokenpixreg =  InlineKeyboardButton(text="PixaBay", callback_data="pix_reg")
    tokenpexreg =  InlineKeyboardButton(text="Pexels", callback_data="pex_reg")
    tokensplreg =  InlineKeyboardButton(text="Unsplash", callback_data="spl_reg")
    returnBut = InlineKeyboardButton(text="🚪 Exit", callback_data="start")
    
    List_reg: list = get_reg()
    amount: int = len(List_reg)
    
    def get_markup() -> list:
        match amount:
            case 0: return [[tokenpixreg],[tokenpexreg],[tokensplreg]]
            case 1: 
                match List_reg:
                    case ['pix']: return [[tokenpexreg], [tokensplreg], [InlineKeyboardButton(text="🔎 Search only with PixaBay", callback_data='pixabay')], [returnBut]]
                    case ['pex']: return [[tokenpixreg], [tokensplreg], [InlineKeyboardButton(text="🔎 Search only with Pexels", callback_data='pexel')], [returnBut]]
                    case ['spl']: return [[tokenpixreg], [tokenpexreg], [InlineKeyboardButton(text="🔎 Search only with Unsplash", callback_data='splash')], [returnBut]]
            case 2:
                if 'pix' not in List_reg: return [[tokenpixreg], [InlineKeyboardButton(text="🔎 Search without PixBay", callback_data='all')], [returnBut]] 
                if 'pex' not in List_reg: return [[tokenpexreg], [InlineKeyboardButton(text="🔎 Search without Pexels", callback_data='all')], [returnBut]] 
                if 'spl' not in List_reg: return [[tokensplreg], [InlineKeyboardButton(text="🔎 Search without Unsplash", callback_data='all')], [returnBut]]
            case 3: return [[returnBut]]
    
    return InlineKeyboardBuilder(markup=get_markup()).adjust((3-amount)if amount < 3 else 1, 1).as_markup()