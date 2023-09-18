from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import types
from DataBase import coll, redis
from typing import Callable, Awaitable, Dict, Any

class DataBaseMiddleWare(BaseMiddleware):
    def __init__ (self):
        super().__init__()

    async def __call__(self, handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]], event: types.Update, data: Dict[str, Any]) -> Any:
        #print(f"Handler: {handler}")
        #print(f"Event: {event}")
        #print(f"Data: {data}")
        #await redis.flushall()
        if await redis.get('_id'):
        #if coll.find_one({'_id': event.callback_query.from_user.id if event.callback_query else event.message.from_user.id}):
            #print(f"_id: {await redis.get('_id')}")
            #print(f"tokenpix: {await redis.get('tokenpix')}")
            #print(f"tokenpex: {await redis.get('tokenpex')}")
            #print(f"tokenspl: {await redis.get('tokenspl')}")
            pass
        else:
            print(f"_id not in Redis")
            user_id: int = event.callback_query.from_user.id if event.callback_query else event.message.from_user.id #type:ignore
            if coll.find_one({'_id': user_id}):
                await redis.set('_id', user_id)
                await redis.set('tokenpix', coll.find_one({'_id': user_id})['tokenpix']) #type:ignore 36810750-674fa7182bd4b3e51c4cef4bf
                await redis.set('tokenpex', coll.find_one({'_id': user_id})['tokenpex']) #type:ignore goOlL7n8WOVRn1HyZzeQyduxlmlg3erSDk9PNkZVEuLOYCkA25MUwthN
                await redis.set('tokenspl', coll.find_one({'_id': user_id})['tokenspl']) #type:ignore TAlJzkst0mlj8NzMOuOvtbd5uZY9YPKzxKKKci6uV-A
            else:
                coll.insert_one({'_id': user_id, 
                                'name': event.callback_query.from_user.full_name if event.callback_query else event.message.from_user.full_name, #type:ignore
                                'tokenpix': "Unregistered",
                                'tokenpex': "Unregistered",
                                'tokenspl': "Unregistered"})
                
        return await handler(event, data)