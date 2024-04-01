from aiogram import Bot, Dispatcher, types, executor,sts
from config import token 

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer("Привет я бот горрда ош")

start_buttons = [
    types.KeyboardButton("Места где можно поесть"),
    types.KeyboardButton("Достопримечательности"),
    types.KeyboardButton("Оставить отзыв"),
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

model_button = [
    types.KeyboardButton('Улук ата'),
    types.KeyboardButton('Алтын'),
    types.KeyboardButton('Нават'),
    types.KeyboardButton("Назад")
]

model_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*model_button)

@dp.message_handler(text="Кафе")
async def num_3(message: types.Message):
    await message.answer("Вот где можно перекусить", reply_markup=model_keyboard)

@dp.message_handler(text ='Улук ата')
async def num_6(message: types.Message):
    await message.photo('https://i4.photo.2gis.com/images/branch/0/30258560073783780_220f.jpg')
    await message.answer_location('https://g.co/kgs/Atxm7Hf')
    await message.answer("Это кафе Улук Ата")

@dp.message_handler(text ='Алтын')
async def num_6(message: types.Message):
    await message.photo('https://avatars.mds.yandex.net/get-altay/6550540/2a000001825daeb54d76a87badb204eacffb/orig')
    await message.answer_location('https://g.co/kgs/8SzwnCP')
    await message.answer("Это кафе Алтын")

@dp.message_handler(text ='Нават')
async def num_6(message: types.Message):
    await message.photo('https://cachizer3.2gis.com/reviews-photos/e247a2d1-67d3-4172-a3af-ee6e01a12352.jpg?w=1920')
    await message.answer_location('https://g.co/kgs/YmtvSDj')
    await message.answer("Это кафе Нават ")

num1_button = [
    types.KeyboardButton('Сулайман тоо'),
    types.KeyboardButton('Пик Ленина'),
    types.KeyboardButton("Назад")
]

num00_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*num1_button)

@dp.message_handler(text="Достопримечательности")
async def num_9(message: types.Message):
    await message.answer("Вот наший Достопримечательности", reply_markup=num00_keyboard)

@dp.message_handler(text="Сулайман тоо")
async def num_01(message: types.Message):
    await message.answer("Это Сулайман тоо")
    await message.answer_photo('https://www.discoverkyrgyzstan.org/sites/default/files/styles/hero/public/61467279254_big.jpg?itok=oSWxd6w3')
    await message.answer_location('https://maps.app.goo.gl/xGry3TbrAUnVq5aP7')

@dp.message_handler(text="")
async def num_01(message: types.Message):
    await message.answer("Пик Ленина")
    await message.answer_photo('https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0e/4c/46/09/tulpar-kul-lake-with.jpg?w=1200&h=-1&s=1')

num01_button = [
    types.KeyboardButton('Имя'),
    types.KeyboardButton('Номер'),
    types.KeyboardButton('Отзыв'),
    types.KeyboardButton("Назад")
]


num2_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*num01_button)

from aiogram.dispatcher.filters.state import State, StatesGroup

class RegisterState(StatesGroup):
    name = State()
    phone = State()
    text = State()








