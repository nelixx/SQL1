import logging
from aiogram.types import KeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from parse import *
import os
from database import *

from dotenv import load_dotenv

from utlis import check_query
# from parse2 import contemporary_prose
from database import Database

load_dotenv()


TOKEN = os.getenv('6541815968:AAEfV3dipxQ3sCgQNJsid7fKt7JzQiJBvdU')


logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())
db = Database()

@dp.message_handler(commands='start')
async def start_process(message: types.Message):
    user = await db.check_user(message.from_id)
    if not user:
        await db.register_user(
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            message.from_id
        )
        await message.answer('Дякую за реєстрацію!')
        await message.answer('Привіт!🌟\nЯ спробую допомогти тобі з шуканням девайсів для ігор')
    
        topic = '/topic'
        search = '/search'
                                

        await message.answer(f'Щоб зробити пошуковий запит, \nскористуйся командою {search}.🔍\nЯкщо не знаєш що шукати, команда {topic} допоможе тобі щось знайти.')
    else:
        await message.answer('Ви вже зареєстровані')


@dp.message_handler(commands='topic')
async def start(message: types.Message, state:FSMContext):
    kb = [

        [types.KeyboardButton("XBOX")],
        [types.KeyboardButton("PC Gaming")],
        [types.KeyboardButton("PlayStation")],

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, selective=True)
    await message.answer('Яка категорія тобі більш подобається?', reply_markup=keyboard)


@dp.message_handler(text="XBOX")
async def start(message: types.Message):
    await message.answer("ОСь що я можу підсказати ")
    kb_1 = [

        [KeyboardButton(text=" Microsoft Xbox Series S 512 GB + доп. джойстик (Гарантія 18 місяців) (13999 грн)")],
        [KeyboardButton(text="Xbox One S 1ТБ All Digital Edition Б.В. + дод. джойстик (Гарантія 6 місяців) (7699 грн)")],
        [KeyboardButton(text="Xbox 360 Slim 250 GB LT +3.0 Б.В. (3599 грн)")],
        [KeyboardButton(text="Xbox Original 80 GB Black Модифікована Вживана (2499 грн)")],
        
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_1, resize_keyboard=True, selective=True)
    await message.answer('Це і все інше ви можете купити на сайтіn https://game-shop.com.ua/ua', reply_markup=keyboard)


@dp.message_handler(text="PC Gaming")
async def start(message: types.Message):
    await message.answer("ОСь що я можу підсказати")
    kb_1 = [

        [KeyboardButton(text="Ноутбук Acer Predator Helios 300 Gaming Laptop, 17.3 Full HD IPS 144Hz (42999 грн)")],
        [KeyboardButton(text="Клавіатура Razer Cynosa Lite RGB Chroma (RZ03-02741500-R3R1) (1199 грн)")],
        [KeyboardButton(text="Mionix Naos QG 12000 DPI (2220 грн)")],
        [KeyboardButton(text="Гарнітура RAZER Kraken Black (RZ04-02830100-R3U1) (1999 грн)")],
        [KeyboardButton(text="Крісло для геймерів Hator Sport Essential Black / Red (HTC-906) (999грн)")],
        
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_1, resize_keyboard=True, selective=True)
    await message.answer('Це і все інше ви можете купити на сайтіn https://game-shop.com.ua/ua', reply_markup=keyboard)


@dp.message_handler(text="PlayStation")
async def start(message: types.Message):
    await message.answer("ОСь що я можу підсказати )")
    kb_1 = [

        [KeyboardButton(text="Sony PlayStation 5 White Digital Edition Б.У. (18999 грн)")],
        [KeyboardButton(text="Sony PlayStation 4 SLIM 500gb (Гарантія 18 місяців) (12999 грн)")],
        [KeyboardButton(text="Sony Playstation 3 SUPER SLIM 500 GB Модифікована Б.В. (Гарантія 3 місяця) (3999 грн)")],
        [KeyboardButton(text="Окуляри віртуальної реальності PlayStation VR2 (23999 грн)")],
        

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_1, resize_keyboard=True, selective=True)
    await message.answer('Це і все інше ви можете купити на сайтіn https://game-shop.com.ua/ua', reply_markup=keyboard)




@dp.message_handler(commands='search')
async def get_games(message:types.Message):
    await message.answer('Тепер введи свій пошуковий запит!')
    await Search.state_on.set()



@dp.message_handler(state=Search.state_on, content_types='text')
async def get_games(message:types.Message, state: FSMContext):
    if not check_query(message.text):
        await message.answer('Будь ласка, введи пошукий запит через пробіли.')
    else:
        query = message.text.lower().strip()
        games = get_games(query)
        for game in games:
            title = games['title']
            price = games['price']
            availability = games['availability']
            url = games['url']
            banner = games['banner']

            msg = (f'<b>Назва: </b>{title}\n<b>Ціна: </b>{price}\n\n<b>{availability}</b>\n\n<b>Посилання: </b>{url}')

            await bot.send_photo(message.chat.id, banner)
            await message.answer(text=msg, parse_mode='html', disable_web_page_preview=True)
            await state.finish()
            await message.answer(f'Якщо бажаєш ввести інший пошуковий запит, скористайся коммандою /search знову!🔍')



    

executor.start_polling(dp)