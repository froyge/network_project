from aiogram import types
from utils import dp, auth

@dp.message_handler(commands=["start"], state="*")
@auth
async def process_start_command(message: types.Message):
    await message.reply(
        "Привет!\n\
Я - Бот для трекинга задач.\n\
Я могу: \n\
1. Добавить задачу: /new\n\
2. Посмотреть на список всех задач: /all")

@dp.message_handler(commands=["help"], state="*")
@auth
async def process_help_command(message: types.Message):
    await message.reply(
        "Привет!\n\
Я могу: \n\
1. Добавить задачу: /new\n\
2. Посмотреть на список всех задач: /all")