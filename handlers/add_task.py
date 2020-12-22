from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.types import ReplyKeyboardRemove
import dateparser
import datetime
from utils import dp, auth
from orm import engine, Task
from sqlalchemy.orm import sessionmaker
from states import AddTask



@dp.message_handler(commands="new", state="*")
@auth
async def add_task_text(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Cancel")
    await message.answer("Выберите задачу:",reply_markup=keyboard )
    await AddTask.waiting_for_task.set()



@dp.message_handler(state=AddTask.waiting_for_task, content_types=types.ContentTypes.TEXT)
async def add_task_time(message: types.Message, state: FSMContext):
    #print(message.text)
    if message.text == "Cancel":
        await message.answer("Выхожу из интерфейса.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return



    await state.update_data(task=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Cancel")
    keyboard.add("Default")
    await AddTask.next()
    await message.answer("Выберите дату/время или нажмите на Cancel,\nесли хотите прекратить выполнение задачи;\nНажмите на Default, чтобы добавить задачу без времени.", reply_markup=keyboard)


@dp.message_handler(state=AddTask.waiting_for_date, content_types=types.ContentTypes.TEXT)
async def add_task_text(message: types.Message, state: FSMContext):
    try:
        response = message.text
        print(response)
        if response == "Cancel":
            await message.answer("Выхожу из интерфейса.", reply_markup=ReplyKeyboardRemove())
            await state.finish()
            return
        elif response == "Default":
            date =  datetime.datetime.date(datetime.datetime.now())
            date = date.replace(day = date.day + 1)
        else:  
            date = datetime.datetime.date(dateparser.parse(message.text))
    except:
        await message.reply("Что-то пошло не так, попробуйте ввести дату заново")
        return

    await state.update_data(date=date)
    await AddTask.next()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Зеленый")
    keyboard.add("Желтый")
    keyboard.add("Красный")
    keyboard.add("Cancel")
    await message.answer("Выберите приоритет задачи с помощью клавиатуры ниже, или нажмите Cancel для прекращения выполнения задачи:", reply_markup=keyboard)
   

   


@dp.message_handler(state=AddTask.waiting_for_priority, content_types=types.ContentTypes.TEXT)
async def add_task_final(message: types.Message, state: FSMContext):
    print(message.text)
    if message.text == "Cancel":
        await message.answer("Выхожу из интерфейса добавления задачи.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    elif message.text == "Зеленый":
        priority = 0
    elif message.text == "Желтый":
        priority = 1
    elif message.text == "Красный":
        priority = 2
    else:
        await message.answer("Что-то пошло не так, попробуйте еще раз.")





    #await message.answer("Выберите дату/время или нажмите на Cancel,\nесли хотите прекратить выполнение задачи;\nНажмите на Default, чтобы добавить задачу без времени.", reply_markup=keyboard)
    user_data = await state.get_data()
    new_task = Task(task=user_data["task"], date=user_data["date"], priority=priority)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(new_task)
    session.commit()

    await message.answer(new_task, reply_markup=ReplyKeyboardRemove())
    await state.finish()









