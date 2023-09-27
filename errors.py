from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError, TelegramNotFound, TelegramServerError, DetailedAiogramError,CallbackAnswerException

error_router = Router()

@error_router.errors()
async def errors_handlers(exception: types.ErrorEvent):

    if isinstance(exception.exception, TelegramNetworkError):
        print(f"Network error: {exception.exception}")

    elif isinstance(exception.exception, TelegramServerError):
        print(f"Server Error: {exception.exception}")
    
    elif isinstance(exception.exception, TelegramNotFound):
        print(f"Message or Chat or User not found: {exception.exception}")
    
    elif isinstance(exception.exception, TelegramBadRequest):
        print(f"BadRequest: {exception.exception}")
    
    elif isinstance(exception.exception, CallbackAnswerException):
        print(f"CallBack error: {exception.exception}")

    elif isinstance(exception.exception, DetailedAiogramError):
        print(f"Some error: {exception.exception}")
    else:
        print(f"Other error: {exception.exception}")
    pass