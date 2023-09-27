from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
load_dotenv()

class FSM_(StatesGroup):
    req = State() 
    hits = State()

class tokenfsm(StatesGroup):
    tokenpix = State()
    tokenpex = State()
    tokenspl = State()

storage = MemoryStorage() #

bot = Bot(token=os.getenv('bot_token'), parse_mode="HTML")
dp = Dispatcher(storage=storage)