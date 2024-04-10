from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from config import token 
import sqlite3,time, logging

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect("kino_reservation.db")
cur = conn.cursor()
cur.execute( """CREATE TABLE IF NOT EXISTS kino_reservation(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username INTEGER NOT NULL,
                    kino TEXT NOT NULL,
                    date_time TEXT NOT NULL
);""")
conn.commit()

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer(f"Здравствуйте нажмите на /kino чтобы узнать о ближайших сеансов", reply_markup=start_keyboard)

@dp.message_handler(commands=['kino'])
async def start(message:types.Message):
    await message.answer(f"Здравствуйте {message.from_user.first_name}, сейчас покажу ближайший сеансы")

start_buttons = [
    types.KeyboardButton("Фильмы")
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

model_button = [
    types.KeyboardButton('БЕЙИШ'),
    types.KeyboardButton('КУНФУ ПАНДА 4'),
]

model_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*model_button)

@dp.message_handler(text="Фильмы")
async def num_3(message: types.Message):
    await message.answer("Вот наший ближайший сеансы, которые у нас есть", reply_markup=model_keyboard)

@dp.message_handler(text='БЕЙИШ')
async def num5_(message: types.Message):
    await message.answer("Вы выбрали фильм 'БЕЙИШ'. Теперь укажите дату и время сеанса в формате 'ГГГГ-ММ-ДД ЧЧ:ММ'. Например, '2024-04-07 18:00'")
    await KinoReservation.waiting_for_date_time.set()

@dp.message_handler(text='КУНФУ ПАНДА 4')
async def num5_(message: types.Message):
    await message.answer("Вы выбрали фильм 'КУНФУ ПАНДА 4'. Теперь укажите дату и время сеанса в формате 'ГГГГ-ММ-ДД ЧЧ:ММ'. Например, '2024-04-07 18:00'")
    await KinoReservation.waiting_for_date_time.set()

class KinoReservation(StatesGroup):
    waiting_for_date_time = State()
    waiting_for_name = State()

@dp.message_handler(state=KinoReservation.waiting_for_date_time)
async def process_date_time(message: types.Message, state: FSMContext):
    date_time = message.text
    async with state.proxy() as data:
        data['date_time'] = date_time
    await message.answer(f"Вы выбрали дату и время: {date_time}. Теперь укажите свое имя.")
    await KinoReservation.next()

@dp.message_handler(state=KinoReservation.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        data['name'] = name
        username = message.from_user
        username = message.from_user.username
        kino = 'БЕЙИШ'
        date_time = data['date_time']
        cur.execute("INSERT INTO kino_reservation (username, kino, date_time) VALUES (?, ?, ?)", (username, kino, date_time))
        conn.commit()
    await message.answer(f"Благодарим вас, {name}! Ваша бронь на фильм 'БЕЙИШ' на {date_time} успешно оформлена.")
    await state.finish()

executor.start_polling(dp, skip_updates=True)
