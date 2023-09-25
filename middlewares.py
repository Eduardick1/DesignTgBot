from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from DataBase import coll, redis_reg as redis
from createBot import bot
from typing import Callable, Awaitable, Dict, Any

class RedisterCheckMiddleWare(BaseMiddleware):

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
                             event: Message, data: Dict[str, Any]) -> Any:
        if redis.get('_id') and int(redis.get('_id')) == event.from_user.id:
            pass
        else:
            print(f"_id not in Redis")
            user_id: int = event.from_user.id 
            if coll.find_one({'_id': user_id}):
                redis.set('_id', user_id)
                redis.set('tokenpix', coll.find_one({'_id': user_id})['tokenpix']) # 36810750-674fa7182bd4b3e51c4cef4bf
                redis.set('tokenpex', coll.find_one({'_id': user_id})['tokenpex']) # goOlL7n8WOVRn1HyZzeQyduxlmlg3erSDk9PNkZVEuLOYCkA25MUwthN
                redis.set('tokenspl', coll.find_one({'_id': user_id})['tokenspl']) # TAlJzkst0mlj8NzMOuOvtbd5uZY9YPKzxKKKci6uV-A
            else:
                coll.insert_one({'_id': user_id, 
                                'name': event.from_user.full_name, 
                                'tokenpix': "Unregistered",
                                'tokenpex': "Unregistered",
                                'tokenspl': "Unregistered",
                                'demo': 3})
                
        return await handler(event, data)
    


class Command_manager(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
                             event: Message, data: Dict[str, Any]) -> Any:
        if event.entities:
            if getattr(event.entities[0], 'type') == 'bot_command':
                try: await bot.delete_message(chat_id=event.chat.id, message_id=event.message_id)
                except Exception as e:
                    print(f"Варя не нашла команду для удаления: {e}")
                    pass
                try: await bot.delete_message(chat_id=event.chat.id, message_id=event.message_id-1)
                except Exception as e:
                    print(f"Варя не нашла предыдущую команду для удаления: {e}")
                    pass
        return await handler(event, data)
     