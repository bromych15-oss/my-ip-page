import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "-5025289260"))

bot = Bot(token=TOKEN)
dp = Dispatcher()


class Application(StatesGroup):
    name = State()
    details = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Чтобы оставить заявку, напиши своё имя:"
    )
    await state.set_state(Application.name)


@dp.message(Application.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📝 Теперь напиши текст своей заявки:")
    await state.set_state(Application.details)


@dp.message(Application.details)
async def get_details(message: Message, state: FSMContext):
    data = await state.get_data()

    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "нет username"
    )

    application = (
        "📝 НОВАЯ ЗАЯВКА!\n\n"
        f"Имя: {data['name']}\n"
        f"Пользователь: {username}\n"
        f"Заявка: {message.text}"
    )

    await bot.send_message(GROUP_ID, application)
    await message.answer("✅ Заявка отправлена!")
    await state.clear()


async def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN")
    await dp.start_polling(bot)


if name == "main":
    asyncio.run(main())
