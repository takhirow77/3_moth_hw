from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
import logging, time, random

from config import token

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('kino_tokens.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        age INT, 
        city VARCHAR(200),
        balance REAL DEFAULT 0
    )
''')
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS seats (
        id INTEGER PRIMARY KEY,
        row_number INTEGER,
        seat_number INTEGER,
        status TEXT DEFAULT 'available', 
        user VARCHAR(200) DEFAULT NULL
    )
''')
conn.commit()

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/register')).add(KeyboardButton('/balance')).add(KeyboardButton('/shop_tokens'))

# def add_seats():
#     rows = 4  
#     seats_per_row = 10  

#     for row_number in range(1, rows + 1):
#         for seat_number in range(1, seats_per_row + 1):
#             cursor.execute('INSERT INTO seats (row_number, seat_number) VALUES (?, ?)', (row_number, seat_number))
#     conn.commit()


# add_seats()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}, я бот для покупки билетов, на кино', reply_markup=start_keyboard)

class UserState(StatesGroup):
    name = State()
    age = State()
    city = State()
    
    
@dp.message_handler(commands=['register'])
async def cmd_register(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        await message.answer("Вы уже зарегистрированы.")
    else:
        await message.answer("Введите ваше имя:")
        await UserState.name.set()
        
@dp.message_handler(state=UserState.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Введите ваш возраст:")
    await UserState.next()

@dp.message_handler(state=UserState.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer("Введите ваш город:")
    await UserState.next()

@dp.message_handler(state=UserState.city)
async def process_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
        cursor.execute('INSERT INTO users (user_id, username, age, city) VALUES (?, ?, ?, ?)',
                       (message.from_user.id, data['name'], data['age'], data['city']))
        conn.commit()
    await state.finish()
    await message.answer("Регистрация завершена. Спасибо!")

class DepositState(StatesGroup):
    amount = State()

@dp.message_handler(commands='balance')
async def cmd_deposit(message: types.Message):
    await message.answer("Введите сумму для пополнения баланса:")
    await DepositState.amount.set()

@dp.message_handler(state=DepositState.amount)
async def deposit_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()[0]

    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")

        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()


        await message.answer(f"Баланс успешно пополнен на {amount}")
        
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")
        await state.finish()

class TicketPurchase(StatesGroup):
    Row = State()
    Seat = State()

@dp.message_handler(commands=['shop_tokens'])
async def buy_ticket_start(message: types.Message):
    await message.answer("Выберите ряд:")
    await TicketPurchase.Row.set()

@dp.message_handler(state=TicketPurchase.Row)
async def process_row(message: types.Message, state: FSMContext):
    row = message.text
    await state.update_data(row=row)
    await message.answer("Выберите место:")
    await TicketPurchase.Seat.set()

def get_name_from_id(user_id):
    cursor.execute('SELECT username FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

@dp.message_handler(state=TicketPurchase.Seat)
async def process_seat(message: types.Message, state: FSMContext):
    seat = message.text
    data = await state.get_data()
    row = data.get('row')
    user_id = message.from_user.id
    username = get_name_from_id(user_id)
    cursor.execute('SELECT status FROM seats WHERE row_number = ? AND seat_number = ?', (row, seat))
    seat_status = cursor.fetchone()
    if seat_status and seat_status[0] == 'available':
        await message.answer(f"Вы выбрали место: Ряд {row}, Место {seat}")
        cursor.execute('UPDATE seats SET status = "occupied", user = ? WHERE row_number = ? AND seat_number = ?', (username, row, seat))
        conn.commit()

        cursor.execute('UPDATE users SET balance = balance - 200 WHERE user_id = ?', (user_id,))
        conn.commit()
        
        await message.answer("Билет успешно куплен!")
        await state.finish()
    else:
        await message.answer(f"Извините, место {seat} в ряду {row} уже занято. Выберите другое место.") 
        
 
@dp.message_handler(commands=['seating_chart'])
async def cmd_seating_chart(message: types.Message):
    cursor.execute('SELECT row_number, seat_number, status FROM seats')
    all_seats = cursor.fetchall()
    seating_chart = ""
    for row in range(1, 5):  
        row_seats = ""
        for seat in range(1, 11):
            seat_status = next((status for (r, s, status) in all_seats if r == row and s == seat), "unavailable")
            if seat_status == "available":
                row_seats += "◯"  
            else:
                row_seats += "⬤" 
        seating_chart += f"Ряд {row}: {row_seats}\n"

    await message.answer(f"График мест:\n{seating_chart}")


executor.start_polling(dp, skip_updates=True)
