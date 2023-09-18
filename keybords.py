from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from DataBase import redis




searchbut = InlineKeyboardButton(text="Поиск медиа", callback_data="search")
infobut = InlineKeyboardButton(text="Информация", callback_data="info")
istartkb = InlineKeyboardMarkup(inline_keyboard=[[searchbut], [infobut]])

cancelkb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]])



async def exception_kb(message: CallbackQuery):
    restartbut = InlineKeyboardButton(text="Изменить запрос", callback_data="search")
    pixbut = InlineKeyboardButton(text="PixaBay", callback_data="pixabay")
    pexelbut = InlineKeyboardButton(text="Pexels", callback_data="pexel")
    splashbut = InlineKeyboardButton(text="Unsplash", callback_data="splash")
    allbut = InlineKeyboardButton(text="Со всех сразу", callback_data="all")
    async def get_reg() -> list:
        return [i for i in ['pix','pex','spl'] if await redis.get(f'token{i}') != 'Unregistered']
    list_reg: list = await get_reg()#type:ignore
    amount = len(list_reg)
    def get_markup(list_reg) -> list:
        markup = [[b] for t in list_reg for b in [pixbut, pexelbut, splashbut] if b.callback_data.startswith(t)]
        if amount < 3:
            markup.extend([[InlineKeyboardButton(text='Регистрация', callback_data='registration')]])
        if message.data == 'typeall':
            markup.extend([[allbut]])
        markup.extend([[restartbut], [infobut]])
        return markup
    match message.data:
        case "pixabay": 
            try: list_reg.remove('pix')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(2 if amount >= 2 else 1,1).as_markup() # type: ignore
        case "pexel": 
            try: list_reg.remove('pex')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(2 if amount >= 2 else 1,1).as_markup() # type: ignore
        case "splash":
            try: list_reg.remove('spl')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(2 if amount >= 2 else 1,1).as_markup() # type: ignore
        case "illustration":
            try: list_reg.remove('pix')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(1).as_markup() # type: ignore
        case "vector": 
            try: list_reg.remove('pix')
            except: pass
            finally: return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(1).as_markup() # type: ignore
        case "all": return None
        case "typeall": return InlineKeyboardBuilder(markup=get_markup(list_reg)).adjust(amount,1,amount).as_markup() # type: ignore

def mainInfo(message: CallbackQuery):
    Infoservicebut = InlineKeyboardButton(text="О сервисах", callback_data="services")
    Inforequestbut = InlineKeyboardButton(text="О запросах", callback_data="requests")
    Inforegisterbut = InlineKeyboardButton(text="О регистрации", callback_data="register")
    Infocommandbut = InlineKeyboardButton(text="О командах", callback_data="commands")
    Infoaboutbut = InlineKeyboardButton(text="О возможностях бота", callback_data="aboutbot")
    searchbt = InlineKeyboardButton(text="Начать поиск медиа", callback_data="search")
    if message == "info" or message.data == "info": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Inforequestbut], [Infocommandbut], [Inforegisterbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
    match message.data:
        case "services": return InlineKeyboardBuilder(markup=[[Inforequestbut], [Infocommandbut], [Inforegisterbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
        case "commands": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Inforequestbut], [Inforegisterbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
        case "requests": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Infocommandbut], [Inforegisterbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
        case "register": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Inforequestbut], [Infocommandbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()
        case "aboutbot": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Inforequestbut], [Infocommandbut], [Inforegisterbut], [searchbt]]).adjust(2,2).as_markup()
        #case "info": return InlineKeyboardBuilder(markup=[[Infoservicebut], [Inforequestbut], [Infocommandbut], [Inforegisterbut], [Infoaboutbut], [searchbt]]).adjust(2,2).as_markup()

async def typeskb():
    typeallbut = InlineKeyboardButton(text="все вместе", callback_data="typeall")
    typephotobut = InlineKeyboardButton(text="Фото", callback_data="typeall")
    typeIllustbut = InlineKeyboardButton(text="Иллюстрации", callback_data="illustration")
    typevectorbut = InlineKeyboardButton(text="Вектор", callback_data="vector")
    if await redis.get('tokenpix') == "Unregistered":
        return InlineKeyboardBuilder(markup=[[typephotobut]]).adjust(3).as_markup()
    else:
        return InlineKeyboardBuilder(markup=[[typephotobut], [typeIllustbut], [typevectorbut], [typeallbut]]).adjust(3).as_markup()

#webtokenkb = InlineKeyboardMarkup()
    
tokenpixurl =  InlineKeyboardButton(text="PixaBay", url="https://pixabay.com/api/docs/")
tokenpexurl =  InlineKeyboardButton(text="Pexels", url="https://www.pexels.com/api/")
tokensplurl =  InlineKeyboardButton(text="Unsplash", url="https://unsplash.com/developers")




def amount_unreg_kb(List_unreg: list, amount: int):
    tokenpixreg =  InlineKeyboardButton(text="PixaBay", callback_data="pix_reg")
    tokenpexreg =  InlineKeyboardButton(text="Pexels", callback_data="pex_reg")
    tokensplreg =  InlineKeyboardButton(text="Unsplash", callback_data="spl_reg")
    continue_without = InlineKeyboardButton(text = "Search without...")
    returnBut = InlineKeyboardButton(text="Exit", callback_data="start")
    markup = None
    match amount:
        case 1: 
            match List_unreg:
                case ['tokenpix']: markup=[[tokenpixreg],[InlineKeyboardButton(text="Search without <i>PixBay</i>")], [returnBut]]
                case ['tokenpex']: markup=[[tokenpexreg],[InlineKeyboardButton(text="Search without <i>Pexels</i>")], [returnBut]]
                case ['tokenspl']: markup=[[tokensplreg],[InlineKeyboardButton(text="Search without <i>Unsplash</i>")], [returnBut]]
        case 2:
            if 'tokenpix' not in List_unreg: markup=[[tokenpexreg], [tokensplreg],[InlineKeyboardButton(text="Search only with PixaBay")], [returnBut]] 
            if 'tokenpex' not in List_unreg: markup=[[tokenpixreg], [tokensplreg],[InlineKeyboardButton(text="Search only with Pexels")], [returnBut]] 
            if 'tokenspl' not in List_unreg: markup=[[tokenpixreg], [tokenpexreg],[InlineKeyboardButton(text="Search only with Unsplash")], [returnBut]]
        case 3: markup=[[tokenpixreg], [tokenpexreg], [tokensplreg], [returnBut]]
     
    return InlineKeyboardBuilder(markup=markup).adjust(amount, 1).as_markup()
