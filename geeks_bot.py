from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

start_buttons =[
    types.KeyboardButton('Помощь'),
    types.KeyboardButton('Курсы'),
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Пробные уроки'),
    types.KeyboardButton('Меропрятия'),
    types.KeyboardButton('Адрес')
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)


@dp.message_handler(commands='start')
async def star(message:types.Message):
    await message.answer(f"Привет {message.from_user.first_name},на связи Geeks! Чем могу помочь?",
                         reply_markup=start_keyboard)


@dp.message_handler(text="Помощь")
async def help(message:types.Message):
    await message.reply(f"{message.from_user.full_name} напишите о  своей проблеме")

@dp.message_handler(text="О нас")
async def about_us(message:types.Message):
    await message.answer("Geeks - это айти курсы в Бишкеке, Кара-Балте, Оше и Ташкенте с 2018 года")

@dp.message_handler(text="Адрес")
async def   address(message:types.Message):
    await message.answer("Ош,Мыразылы Аматова 1Б")
    await message.answer_location(40.5194,72.803)


courses_buttons = [
    types.KeyboardButton('Backend'),
    types.KeyboardButton('Frontend'),
    types.KeyboardButton('Android'),
    types.KeyboardButton('UX/UI'),
    types.KeyboardButton('Назад')
]
courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_buttons)


@dp.message_handler(text="Курсы")
async def all_courses(message:types.Message):
    await message.answer("Вот все наши курсы:",reply_markup=courses_keyboard)

@dp.message_handler(text="Назад")
async def back(message:types.Message):
    await star(message)

@dp.message_handler(text="Backend")
async def backend(message:types.Message):
    await message.answer("Backend - это серверная сторона сайта или приложения\nМесяц обучения: 5 месяцев\nСтоимость 10000")

@dp.message_handler(text="Frontend")
async def backend(message:types.Message):
    await message.answer("Frontend -  создает интерфейсы веб-сайтов и приложений\nМесяц обучения: 5 месяцев\nСтоимость 10000")

@dp.message_handler(text="Android")
async def backend(message:types.Message):
    await message.answer("Android -  создает приложений на андроид \nМесяц обучения: 7 месяцев\nСтоимость 10000")

@dp.message_handler(text="UX/UI")
async def backend(message:types.Message):
    await message.answer("Ux/UI -  проектирует и рисует интерфейсы цифровых продуктов: мобильных и веб-приложений, сайтов\nМесяц обучения: 3 месяцев\nСтоимость 10000")

@dp.message_handler(text="Пробные уроки")
async def all_courses(message:types.Message):
    await message.answer("На пробным уроке будете писать код")

@dp.message_handler(text="Меропрятия")
async def all_courses(message:types.Message):
    await message.answer("В эту суботе будет дент кода 16:00")

                         
@dp.message_handler()
async def   not_found(message:types.Message):
    await message.reply("Я вас не понял")


executor.start_polling(dp)