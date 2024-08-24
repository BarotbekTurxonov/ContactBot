from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ADMINS
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer("Assalom alaykum boss!")
        return
    await message.answer(f"Salom {message.from_user.full_name}!")
