import os
import asyncio
from aiogram import Bot, Dispatcher, executor, types



from config import *
from utils import ioloop, dp, auth


import logging
from datetime import datetime
from handlers import *

"""
engine = create_engine('sqlite:///:{DB_FILENAME}:', echo=True)
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id=Column(Integer)
    time = Column(DateTime)
    task = Column(String)

    def __repr__(self):
        return f"<Task(time={self.time}, task={self.task})>"

"""

"""




@dp.message_handler(commands=["help"])
@auth
async def process_help_command(message: types.Message):
    await message.reply(
        "Привет!\n\
Я могу: \n\
1. Добавить задачу: /new\n\
2. Посмотреть на список всех задач: /all")

@dp.message_handler()
@auth
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)

@dp.message_handler()
@auth
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)




async def match_time(time: tuple):
    while True:
         ts = datetime.now()
         if ts.hour == time[0] and ts.minute == time[1] and ts.second == 0:
            return
         else:
            await asyncio.sleep(0)



async def periodic(sleep_for):
    while True:
        await match_time((13, 47))
        now = datetime.utcnow()
        for id in {251538773}:
            await bot.send_message(id, f"{now}",
                                   disable_notification=True)

"""
if __name__ == '__main__':
    ioloop.create_task(notify_at(NOTIFY_HOURS, NOTIFY_MINUITES))
    executor.start_polling(dp)
