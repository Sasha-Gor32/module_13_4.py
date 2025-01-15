import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter, CommandStart
import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import asyncio


api = ""
bot = Bot(token=api)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.')
    print('Привет! Я бот, помогающий твоему здоровью.')


# @dp.message()
# async def all_massages(message: types.Message):
#     text = message.text
#     if text in ['Привет', 'привет', 'hi', 'hello']:
#         await message.answer('Введите команду /start, чтобы начать общение.')
#         print('Введите команду /start, чтобы начать общение.')
#     else:
#         await message.answer(message.text)


class UserState(StatesGroup):
    age = State()  # Возраст
    growth = State()  # Рост
    weight = State()  # Вес


@dp.message(StateFilter(None), F.text == 'Calories')
async def set_age(message: types.Message, state: FSMContext):
    await message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)


@dp.message(UserState.age, F.text)
async def set_growth(message: types.Message, state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await message.answer('Вы ввели неправильно, введите возраст еще раз:')
        return

    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await state.set_state(UserState.growth)


@dp.message(UserState.growth, F.text)
async def set_weight(message: types.Message, state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await message.answer('Вы ввели данные неправильно, введите рост в см еще раз:')
        return

    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await state.set_state(UserState.weight)


@dp.message(UserState.weight, F.text)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    try:
        int(message.text)
    except ValueError:
        await message.answer('Вы ввели данные о весе неправильно, введите вес в кг еще раз:')
        return

    data = await state.get_data()
    print(data)

    norm_calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161

    print(norm_calories)
    await message.answer(str(f'Ваша норма калорий: {norm_calories}'))
    await state.clear()

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
