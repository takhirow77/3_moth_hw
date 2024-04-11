from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from config import token 
import sqlite3, requests, time, logging,re

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
 
conn = sqlite3.connect('codex.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                    id INT,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    phone VARCHAR(100),
                    directions VARCHAR(150)
 );''')

conn.commit()

start_inline_buttons = [
    types.InlineKeyboardButton('Регистрация', callback_data='add_info')
]
start_inline_keyboard = types.InlineKeyboardMarkup().add(*start_inline_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.reply("Здраствуйте я бот codex_club-ба пройдите регистрацию ", reply_markup=start_inline_keyboard)

class AddInfoState(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    directions = State()

@dp.callback_query_handler(lambda call: call.data == 'add_info')
async def start_add_film(callback:types.CallbackQuery):
    await callback.answer("Кнопка работает")
    await callback.message.answer("Введите имя")
    await AddInfoState.first_name.set()

@dp.message_handler(state=AddInfoState.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await message.answer("Введите вашу Фамилию:")
    await AddInfoState.last_name.set()

@dp.message_handler(state=AddInfoState.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
    await message.answer("Введите номер:")
    await AddInfoState.phone.set()

@dp.message_handler(state=AddInfoState.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await message.answer("Введите вашу направление:")
    await AddInfoState.directions.set()

@dp.message_handler(state=AddInfoState.directions)
async def process_directions(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['directions'] = message.text
    cursor.execute("INSERT INTO users (id, first_name, last_name, phone, directions) VALUES (?, ?, ?, ?, ?)",
                   (message.from_user.id,  data['first_name'], data['last_name'],data['phone'],data['directions']))
    conn.commit()
    await message.answer("Спасибо за регистрацию!")
    await state.finish()
    await bot.send_message(-4134523818,    'Успешно прошло')

executor.start_polling(dp, skip_updates=True)
    
