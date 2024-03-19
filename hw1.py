from aiogram import types,executor,Dispatcher,Bot
from config import token
import random

bot = Bot(token=token)
dp = Dispatcher(bot)


a = [1,2,3]
b = random.choice(a)

@dp.message_handler(commands='start')
async def start(message:types.Message):
   await message.answer('Я загадал число от 1 до 3')

@dp.message_handler(text='1')
async def one(message: types.Message):
   if b == 1:
      await message.answer('вы угадали')
      await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
   else:
        await message.answer('не угадали')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')


@dp.message_handler(text='2')
async def one(message: types.Message):
   if b == 2:
      await message.answer('вы угадали')
      await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
   else:
        await message.answer('не угадали')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')


@dp.message_handler(text='3')
async def one(message: types.Message):
   if b == 3:
      await message.answer('вы угадали')
      await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
   else:
        await message.answer('не угадали')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')

executor.start_polling(dp)