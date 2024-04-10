from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from config import token 
import sqlite3, requests, time, logging

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('codes.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS code(
    code INT,
    title_film VARCHAR(255)
);
""")

start_inline_buttons = [
    types.InlineKeyboardButton('Фильм', callback_data='get_film'),
    types.InlineKeyboardButton('Загрузить', callback_data='add_film'),
    types.InlineKeyboardButton('TikTok', url='https://tiktok.com/@codex_kg/')
]
start_inline_keyboard = types.InlineKeyboardMarkup().add(*start_inline_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.reply("Привет отправь мне код, а я тебе название фильма", reply_markup=start_inline_keyboard)

class AddFilmState(StatesGroup):
    code = State()
    title_film = State()

@dp.callback_query_handler(lambda call: call.data == 'add_film')
async def start_add_film(callback:types.CallbackQuery):
    await callback.answer("Кнопка работает")
    await callback.message.answer("Отправьте код для фильма")
    await AddFilmState.code.set()

@dp.message_handler(state=AddFilmState.code)
async def get_title_film(message:types.Message, state:FSMContext):
    if message.text.isdigit():
        await state.update_data(code=message.text)
        await message.answer("Введите название фильма")
        await AddFilmState.title_film.set()
    else:
        await message.answer("Введите цифры")

@dp.message_handler(state=AddFilmState.title_film)
async def get_code_title_and_to_db(message:types.Message, state:FSMContext):
    await state.update_data(title_film=message.text)
    result = await storage.get_data(user=message.from_user.id)
    await message.answer("Загружаю в Базу Данных...")
    await message.answer(f"{result}")
    cursor.execute("INSERT INTO code VALUES (?, ?);",
                   (result['code'], result['title_film']))
    cursor.connection.commit()
    await state.finish()

class SendFilmState(StatesGroup): #Создаем функцию State для получения данных полей в будущем
    code = State() #Создаем поле code для получения кода фильма

@dp.callback_query_handler(lambda call: call.data == "get_film") #Проверяем нажал ли пользователь на кнопку Фильм, то есть вызвал ли пользователь
async def start_get_film(callback:types.CallbackQuery): #Создаем асинхронную функцию
    await callback.message.answer("Введите код фильма") #Просим пользователя ввести код фильма
    await SendFilmState.code.set() #Ожидаем от пользователя код от фильма


@dp.message_handler(state=SendFilmState.code) #После того как пользователь ввел код от фильма начинаем его обрабатывать
async def find_film_send(message:types.Message, state:FSMContext): #Создаем асинхронную функцию find_film_send
    await message.answer(f"Ищу фильм по коду {message.text}") #Выводим сообщение что ищем фильм
    cursor.execute(f"SELECT title_film FROM code WHERE code = {message.text};") #Делаем запрос в базу данных где выводим колонну title_film, и сравниваем есть ли данный код в базе данных
    result = cursor.fetchall() #Выводим результат с базы данных через метод fetchall
    if result != []: #Делаем условие если результат не пустой список, то есть есть код есть в базе то он не будет пустой
        await message.answer(f"Фильм найден {result[0][0]}") #Выводим результат поиска и название фильма, также обращаемся в переменной result и выводим сперва котеж который он выводит, так как там сперва выходит список внутри которого кортеж, и внутри котежа через индекс ноль получаем первое значение
    else:
        await message.answer("Мы не нашли фильм") #Если фильма нету в базе, то есть переменная result пустой список. Выводим о том что мы не нашли фильм
    await state.finish() #В конце не ожидаем от пользователя данных

executor.start_polling(dp)
