from aiogram import Bot, Dispatcher, types, executor
from config import token 

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Hello World")

@dp.message_handler(commands='help')
async def help(message:types.Message):
    await message.answer("Help Geeks")

@dp.message_handler(text="Привет")
async def hello(message:types.Message):
    await message.answer("Привет, как дела?")

@dp.message_handler(commands='test')
async def test(message:types.Message):
    await message.reply("Тестирование бота")
    await message.answer_location(0, 0)
    await message.answer_venue(0, 0, "Geeks", "Amatova 1B", "Hello")
    await message.answer_dice("⚽️")

executor.start_polling(dp)
