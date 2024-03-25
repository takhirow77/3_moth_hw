from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging
import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('bmw_test_drives.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS test_drives (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username INTEGER NOT NULL,
                    model TEXT NOT NULL,
                    date_time TEXT NOT NULL
                    );''')
conn.commit()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет, я тг бот от компании BMW", reply_markup=start_keyboard)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    print(message)
    await message.answer(f"Привет, {message.from_user.full_name}! Чем могу вам помочь?")

start_buttons = [
    types.KeyboardButton("Модели автомобилей"),
    types.KeyboardButton("Цены"),
    types.KeyboardButton("Характеристики"),
    types.KeyboardButton("Специальные предложения")
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

model_button = [
    types.KeyboardButton('BMW i7 M70 xDRIVE'),
    types.KeyboardButton('BMW M440i xDrive Cabrio'),
    types.KeyboardButton('BMW X7 M60i'),
    types.KeyboardButton("Назад")
]

model_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*model_button)

@dp.message_handler(text="Модели автомобилей")
async def num_3(message: types.Message):
    await message.answer("Вот модели машин, которые у нас есть", reply_markup=model_keyboard)

@dp.message_handler(text="BMW i7 M70 xDRIVE")
async def num_5(message: types.Message):
    await message.answer_photo('https://www.topgear.com/sites/default/files/2023/04/P90500803_highRes_the-bmw-i7-m70-xdriv.jpg')
    await message.answer("Это модель i7 M70 xDRIVE BMW ")

@dp.message_handler(text="BMW M440i xDrive Cabrio")
async def num_6(message: types.Message):
    await message.answer_photo('https://static.carbuyer.com.sg/wp-content/uploads/2021/06/2021-bmw-4-series-convertible-price-singapore-review-25062021-1.jpg')
    await message.answer('Это модель M440i xDrive cabrio BMW')

@dp.message_handler(text="BMW X7 M60i")
async def num_7(message: types.Message):
    await message.answer_photo('https://www.completecar.ie/img/galleries/11845/bmw_x7_m60i_mineral_white_lci_2022_020.jpg')
    await message.answer('Это модель BMW X7 M60i')

num1_button = [
    types.KeyboardButton('Цена BMW i7 M70 xDRIVE'),
    types.KeyboardButton('Цена BMW  M440i xDrive Cabrio '),
    types.KeyboardButton('Цена BMW X7 M60i '),
    types.KeyboardButton("Назад")
]

num00_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*num1_button)

@dp.message_handler(text="Цены")
async def num_9(message: types.Message):
    await message.answer("Вот модели машин и их цены", reply_markup=num00_keyboard)

@dp.message_handler(text="Цена BMW i7 M70 xDRIVE")
async def num_01(message: types.Message):
    await message.answer("Эта машинка BMW i7 M70 xDRIVE 27 925 000 сомов.")

@dp.message_handler(text="Цена BMW  M440i xDrive Cabrio")
async def num_02(message: types.Message):
    await message.answer("Эта машинка BMW M440i xDrive Cabrio 8 650 000 сомов стоит")

@dp.message_handler(text="Цена BMW X7 M60i")
async def num_03(message: types.Message):
    await message.answer("Эта машинка BMW X7 M60i 15 300 000 сомов стоит")

@dp.message_handler(text='Назад')
async def rollback(message: types.Message):
    await start(message)

num01_button = [
    types.KeyboardButton('Характеристики BMW i7 M70 xDRIVE'),
    types.KeyboardButton('Характеристики BMW M440i xDrive Cabrio'),
    types.KeyboardButton('Характеристики BMW X7 M60i'),
    types.KeyboardButton("Назад")
]


num2_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*num01_button)

@dp.message_handler(text="Характеристики")
async def num_9(message: types.Message):
    await message.answer("Характеристики машин", reply_markup=num2_keyboard)

@dp.message_handler(text='Назад')
async def rollback(message: types.Message):
    await start(message)


@dp.message_handler(text='Характеристики BMW i7 M70 xDRIVE')
async def num_01(message: types.Message):
    await message.answer("""Годы производства
2023 -
Страна производства
Germany (i7)
Разгон 0-100 км/ч
3.7 с
47 из 575
Запас хода
560 км
95 из 575 
Батарея
105.7 кВт⋅ч
49 из 575 
Разгон 0-100 км/ч
3.7 с
Емкость батареи
105.7 кВт⋅ч
Запас хода
560 км
Разгон 0-100 км/ч
3.7 с
Макс. скорость
250 км/ч (155 миль/ч)
Мощность двигателя
659 л.с. (491 кВт)
Крутящий момент
1100 Нм (811 lb-ft)
Эффективность
19 кВт⋅ч/100 км
Привод
AWD
Тип двигателя
Permanent-magnet""")
    
@dp.message_handler(text="Характеристики BMW M440i xDrive Cabrio")
async def num_02(message: types.Message):
    await message.answer("""
 Модельный год: 2020
 КПП: автомат
 Привод: полный
 Кузов: кабриолет
 Л.с.: 387
 Объем: 2998
 Топливо: бензин
 Страна бренда: Германия
 Уровень оснащения: M Sport Edition 21
 Год начала производства модели: 2020
 Комплектация: M440i xDrive M Sport Edition 21
 Класс модели: D-средний класс
 Модель: 4 серия Cabrio
 Диски: легкосплавные
 Защита автомобиля снизу: есть
 Количество дверей: 2
 Тип кузова: кабриолет
 Размер дисков: R19""")

@dp.message_handler(text='Характеристики BMW X7 M60i')
async def num_03(message: types.Message):
    await message.answer("""Мощность, л.с.:
530
Разгон 0-100 км/ч, с:
4,7
Расход топлива (смешанный цикл), л/100 км:
12,2
Выбросы CO₂, (смешанный цикл), г/км:
277""")

@dp.message_handler(text='Назад')
async def rollback(message: types.Message):
    await start(message)

num_button = [
    types.KeyboardButton('Гарантия 1+1'),
    types.KeyboardButton('Тест драйв'),  
    types.KeyboardButton("Назад")
]

num_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*num_button)

@dp.message_handler(text="Специальные предложения")
async def num(message: types.Message):
    await message.answer("Вот какие есть специальные предложения", reply_markup=num_keyboard)

@dp.message_handler(text="Гарантия 1+1")
async def num(message: types.Message):
    await message.answer("Мы дадим гарантию на 3 года")

test_buttons = [
    types.KeyboardButton('взять на тест BMW i7 M70 xDRIVE'),
    types.KeyboardButton('взять на тест BMW M440i xDrive Cabrio'),
    types.KeyboardButton('взять на тест BMW X7 M60i'),
    types.KeyboardButton("Назад")
]
test_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*test_buttons)

@dp.message_handler(text='Тест драйв')
async def test_drive(message: types.Message):
    await message.answer("Выберите модель для тест-драйва:", reply_markup=test_keyboard)

@dp.message_handler(text='взять на тест BMW i7 M70 xDRIVE')
async def test_car1(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    car_model = 'BMW i7 M70 xDRIVE'
    date_time = message.date.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO test_drives (username, model, date_time) VALUES (?, ?, ?)",
                   (username, car_model, date_time))
    conn.commit()

    await message.answer('Вы записались на тест-драйв BMW i7 M70 xDRIVE. Приходите к нам в офис в указанное время.')

@dp.message_handler(text='взять на тест BMW M440i xDrive Cabrio')
async def test_car1(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    car_model = 'BMW M440i xDrive Cabrio'
    date_time = message.date.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO test_drives (username, model, date_time) VALUES (?, ?, ?)",
                   (username, car_model, date_time))
    conn.commit()

    await message.answer('Вы записались на тест-драйв BMW M440i xDrive Cabrio  . Приходите к нам в офис в указанное время.')

@dp.message_handler(text='взять на тест BMW X7 M60i')
async def test_car1(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    car_model = 'BMW X7 M60i'
    date_time = message.date.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO test_drives (username, model, date_time) VALUES (?, ?, ?)",
                   (username, car_model, date_time))
    conn.commit()

    await message.answer('Вы записались на тест-драйв BMW X7 M60i . Приходите к нам в офис в указанное время.')
    

executor.start_polling(dp, skip_updates=True)