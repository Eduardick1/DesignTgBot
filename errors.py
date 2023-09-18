from aiogram.utils.exceptions import InvalidQueryID, MessageCantBeDeleted, MessageCantBeEdited, BadRequest
from aiogram import Dispatcher
from createBot import dp

async def errors_handlers(update, exception):

    if isinstance(exception, InvalidQueryID):
        print(f"InvalidQueryID: {exception}; Update {update}")
        return True

    if isinstance(exception, MessageCantBeDeleted):
        print(f"MessageCantBeDeleted: {exception}; Update {update}")
        return True
    
    if isinstance(exception, MessageCantBeEdited):
        print(f"MessageCantBeEdited: {exception}; Update {update}")
        return True
    
    if isinstance(exception, BadRequest):
        print(f"BadRequest: {exception}; Update {update}")
        return True
    
    print(f"Update: {update}; Exception: {exception}")

def register_errors(dp: Dispatcher):

    dp.register_errors_handler(errors_handlers)