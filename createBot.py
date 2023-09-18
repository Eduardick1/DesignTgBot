from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import DTOKEN


storage = MemoryStorage()

bot = Bot(token=DTOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)