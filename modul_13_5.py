from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "***"
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
button = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
kb_list = (button, button2)
kb.add(button)
kb.add(button2)

@dp.message_handler(text='Привет')
async def start(message):
    await message.answer('Привет! Введите команду /Start, чтобы начать общение.')

@dp.message_handler(commands = ["start"])
async def start(message):
    await message.answer("Я бот, помогающий твоему здоровью", reply_markup=kb)


@dp.message_handler(text = 'Информация')
async def inform(message):
    await message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора \n'
                         'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; \n'
                         'для женщин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) -161')


@dp.message_handler(text = 'Рассчитать')
async def age(message):
    await message.answer("Введите свой возраст")
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def gender(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result1 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма калорий: {result1} ккал в сутки (для мужчин)')
    result2 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f'Ваша норма калорий: {result2} ккал в сутки (для женщин)')
    await UserState.weight.set()
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
