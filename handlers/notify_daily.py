import asyncio
from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, Chat
import dateparser
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from utils import dp, auth, bot
from config import *
from orm import engine, Task
from states import ManageTasks
import logging
import os

VOICE = os.environ.get("VOICE_TOKEN")
if VOICE is None:
    raise ValueError("Environment variable \"VOICE_TOKEN\" \
is not set, with no default")

MY_ID = int(os.environ.get("MY_ID", default=0))
if MY_ID == 0:
        raise ValueError("Environment variable \"MY_ID\" \
is not set, with no default")
async def match_time(time: tuple):
    while True:
         ts = datetime.now()
         if ts.hour == time[0] and ts.minute == time[1] and ts.second == 0:
            return
         else:
            await asyncio.sleep(0)


async def notify_at(hours, minuites):
    while True:
        await match_time((hours, minuites))
        today = datetime.date(datetime.now())
        Session = sessionmaker(bind=engine)
        session = Session()
        raw_tasks = session.query(Task).filter(Task.date==today).all()
        
        state = dp.current_state(user=MY_ID)
        
        for id_ in {MY_ID}:
            if len(raw_tasks) == 0:
                bot.send_message(id_, "Нет задач на сегодня")
            else:

                keyboard = types.InlineKeyboardMarkup()
            
                for index, t_ in enumerate(raw_tasks):
                    button = types.InlineKeyboardButton(f"({t_.id_}). {str(t_.date)}, {t_.task}", callback_data = t_.id_)
                    keyboard.add(button)
            
                await bot.send_message(id_,"Доброго времени суток!\nНажмите на текст задачи, чтобы ее изменить", reply_markup=keyboard)
                await bot.send_voice(id_, VOICE)
                await state.set_state( ManageTasks.waiting_for_task_choice)
        await match_time((0, 0))