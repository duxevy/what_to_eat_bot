import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TG_API_KEY")
dp = Dispatcher()

# Списки блюд
garnishes = ["рис", "картошка пюре"]
meats = ["курица терияки", "печень куриная"]

# Текущее блюдо
current_garnish = None
current_meat = None


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Собрать блюдо 🎲")],
        [
            types.KeyboardButton(text="Добавить гарнир 🍚"),
            types.KeyboardButton(text="Добавить мясо 🥩"),
        ],

    ]
    main_menu = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer("Привет! Я помогу тебе составить блюдо. Выбери действие:", reply_markup=main_menu)


async def main() -> None:
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
