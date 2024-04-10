from aiogram import Bot, Dispatcher, types, executor
from config import token
from bs4 import BeautifulSoup
import requests, logging

bot = Bot(token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer(f"Здравствуйте {message.from_user.first_name}, нажмите /courses чтобы узнать курсы валют")

@dp.message_handler(commands='courses')
async def send_currency_rates(message):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    currencies = soup.find_all('td', class_='exrate')
    await message.answer(f"Зраствуйте! Я бот, который поможет вам узнать текущие курсы валют.\n"
                                                  f"Курс USD: {currencies[0].text}\n"
                                                  f"Курс EUR: {currencies[2].text}\n"
                                                  f"Курс RUB: {currencies[4].text}\n"
                                                  f"Курс KZT: {currencies[6].text}")            

executor.start_polling(dp, skip_updates=True)