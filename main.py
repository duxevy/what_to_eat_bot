import asyncio
import logging
import os
import sys
import random

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TG_API_KEY")
dp = Dispatcher()

# Текущее блюдо
current_garnish = None
current_meat = None

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


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    garnish = State()  # Состояние ожидания ввода гарнира
    meat = State()  # Состояние ожидания ввода мяса


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я помогу тебе составить блюдо. Выбери действие:", reply_markup=main_menu)


@dp.message(F.text == "Собрать блюдо 🎲")
async def assemble_dish(message: types.Message):
    global current_garnish, current_meat
    # Списки блюд
    try:
        with open("garnishes.txt", "r", encoding="utf-8") as f:
            garnishes = [str(line) for line in f.readlines()]
        with open("meats.txt", "r", encoding="utf-8") as f:
            meats = [str(line) for line in f.readlines()]
        current_garnish = random.choice(garnishes)
        current_meat = random.choice(meats)
        await message.answer(f"Вот твоё блюдо: {current_garnish.strip()} + {current_meat.strip()}",
                             reply_markup=main_menu)
    except IndexError:
        await message.answer(f"Пока списки гарниров и мяса пусты, нечего составить! 🙂")


@dp.message(F.text == "Добавить гарнир 🍚", StateFilter(default_state))
async def add_garnish_prompt(message: types.Message, state: FSMContext):
    await message.answer("Отправь мне название гарнира, который ты хочешь добавить.")
    await state.set_state(FSMFillForm.garnish)


@dp.message(StateFilter(FSMFillForm.garnish))
async def add_garnish(message: types.Message, state: FSMContext):
    new_garnish = message.text
    with open("garnishes.txt", "a", encoding="utf-8") as f:
        f.write(f"{new_garnish}\n")
    await message.reply(f"Гарнир '{new_garnish}' добавлен!", reply_markup=main_menu)
    await state.clear()


@dp.message(F.text == "Добавить мясо 🥩", StateFilter(default_state))
async def add_meat_prompt(message: types.Message, state: FSMContext):
    await message.reply("Отправь мне название мяса, которое ты хочешь добавить.")
    await state.set_state(FSMFillForm.meat)


@dp.message(StateFilter(FSMFillForm.meat))
async def add_meat(message: types.Message, state: FSMContext):
    new_meat = message.text
    with open("meats.txt", "a", encoding="utf-8") as f:
        f.write(f"{new_meat}\n")
    await message.reply(f"Мясо '{new_meat}' добавлено!", reply_markup=main_menu)
    await state.clear()


async def main() -> None:
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
