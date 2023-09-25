from aiogram import F, Router
from aiogram.types import Update, ErrorEvent
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError, TelegramNotFound, TelegramServerError, DetailedAiogramError
from typing import Union

error_router = Router()

@error_router.errors()
async def errors_handlers(update: Update, exception: Union[ErrorEvent, Exception]):

    if isinstance(exception, TelegramNetworkError):
        print(f"Network error: {exception}; Update {update}")
        return True

    if isinstance(exception, TelegramServerError):
        print(f"Server Error: {exception}; Update {update}")
        return True
    
    if isinstance(exception, TelegramNotFound):
        print(f"Message or Chat or User not found: {exception}; Update {update}")
        return True
    
    if isinstance(exception, TelegramBadRequest):
        print(f"BadRequest: {exception}; Update {update}")
        return True
    
    if isinstance(exception, DetailedAiogramError):
        print(f"Other error: {exception}; Update {update}")
        return True

    print(f"Update: {update}; Exception: {exception}")
