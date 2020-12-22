from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import dateparser
import datetime
from utils import dp, auth, logging
from orm import engine, Task
from sqlalchemy.orm import sessionmaker
from utils import bot
from states import ManageTasks
from aiogram.utils.emoji import emojize
import logging


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False




map_priority_to_unicode = {
    0: ":green_apple:",
    1: ":banana:",
    2: ":apple:"
}


@dp.message_handler(commands=["all"], state="*")
@auth
async def query_database(message: types.Message):
    argument = message.get_args()
    Session = sessionmaker(bind=engine)
    session = Session()
    if len(argument) > 0:
        
        date = datetime.datetime.date(dateparser.parse(argument))
        #logging.info("Requesting tasks for date", date)
        response = session.query(Task).filter(Task.date == date).order_by(Task.id_).all()
    else:

        response = session.query(Task).order_by(Task.id_).all()
    #print("RESPONSE", response)
    if len(response) == 0:
        await message.answer("Нет добавленных задач")
    else:
        keyboard = types.InlineKeyboardMarkup()
        
        #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for index, t_ in enumerate(response):
            button = types.InlineKeyboardButton(f"({t_.id_}). {str(t_.date)}, {t_.task} {emojize(map_priority_to_unicode[t_.priority])}", callback_data = t_.id_)
            keyboard.add(button)
        
        await message.answer("Нажмите на текст задачи, чтобы ее изменить", reply_markup=keyboard)
        await ManageTasks.waiting_for_task_choice.set()



@dp.message_handler(commands=["today"], state="*")
@auth
async def query_database(message: types.Message):
    Session = sessionmaker(bind=engine)
    session = Session()
    response = session.query(Task).filter(Task.date ==datetime.datetime.date(datetime.datetime.now())).order_by(Task.id_).all()
    #print("RESPONSE", response)
    if len(response) == 0:
        await message.answer("Нет добавленных задач")
    else:
        keyboard = types.InlineKeyboardMarkup()
        
        #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for index, t_ in enumerate(response):
            button = types.InlineKeyboardButton(f"({t_.id_}). {str(t_.date)}, {t_.task} {emojize(map_priority_to_unicode[t_.priority])}", callback_data = t_.id_)
            keyboard.add(button)
        
        await message.answer("Нажмите на текст задачи, чтобы ее изменить", reply_markup=keyboard)
        await ManageTasks.waiting_for_task_choice.set()



@dp.callback_query_handler(lambda t: True,  state=ManageTasks.waiting_for_task_choice)
async def choose_tasks_action(query: types.CallbackQuery, state: FSMContext):
    #print("TEXT", query.data)
    try:
        
        id_ = int(query.data)
        Session = sessionmaker(bind=engine)
        session = Session()
        response = session.query(Task).filter(Task.id_ == id_).all()
        if len(response) > 0:

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.row("Delete", "Update")
            keyboard.add("Cancel")
            
            await state.update_data(id_=id_)
            await bot.send_message(query["from"]["id"], f"Выбрана задача ({id_}). Выберите действие", reply_markup=keyboard)
            await ManageTasks.waiting_for_action_choice.set()
        else:
            await bot.send_message(query["from"]["id"], "Неправильно выбрано действие, выхожу из интерфейса", reply_markup=ReplyKeyboardRemove())
            await state.finish()
            return 



    except Exception as e:
        logging.warning("SNAFU")
        logging.warning(str(e))
        return 


@dp.message_handler(state=ManageTasks.waiting_for_action_choice, content_types=types.ContentTypes.TEXT)
async def handle_action_choise(message: types.Message, state: FSMContext):
    logging.info("Handling action choice...")
    if message.text == "Delete":
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            id_ = await state.get_data()
            id_ = id_["id_"]
            task_to_delete = session.query(Task).filter(Task.id_ == id_).one()
            session.delete(task_to_delete)
            session.commit()
            if session.query(Task).filter(Task.id_ == id_).count() == 0:
                await message.answer("Задача успешно удалена!", reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            await message.answer(str(e))
            return   

    elif message.text == "Update":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row("Date", "Text", "Priority")
        await message.answer("Выберите, что вы хотите обновить:", reply_markup=keyboard)
        await ManageTasks.on_update.set()

        
    elif message.text == "Cancel":
        await message.answer("Выхожу из интерфейса.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return


    else:
        await message.answer("Пожалуйста, выберите действие из списка ниже")




@dp.message_handler(state=ManageTasks.on_update, content_types=types.ContentTypes.TEXT)
async def process_update(message: types.Message, state: FSMContext):
    logging.info("Processing update value choice...")
    if message.text == "Date":
        await ManageTasks.on_update_date.set()
        await message.answer("Введите новое значение, ", reply_markup=ReplyKeyboardRemove())

    elif message.text == "Text":
        await ManageTasks.on_update_text.set()
        await message.answer("Введите новое значение", reply_markup=ReplyKeyboardRemove())

    elif message.text == "Priority":
        await ManageTasks.on_update_priority.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Зеленый")
        keyboard.add("Желтый")
        keyboard.add("Красный")
        keyboard.add("Cancel")
        await message.answer("Выберите новое значение", reply_markup=keyboard)
    elif message.text == "Cancel":
        await message.answer("Выхожу из интерфейса.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return




@dp.message_handler(state=ManageTasks.on_update_date, content_types=types.ContentTypes.TEXT)
async def process_update_date(message: types.Message, state: FSMContext):
    logging.info("Processing date update...")
    try:
        if message.text != "Cancel":
            Session = sessionmaker(bind=engine)
            session = Session()
            date = message.text
            date = datetime.datetime.date(dateparser.parse(date))
            id_ = await state.get_data()
            id_ = id_["id_"]
            session.query(Task).filter(Task.id_ == id_).update({Task.date:date}, synchronize_session=False)
            session.commit()
            state.finish()
        else:
            await message.answer("Выхожу из интерфейса.", reply_markup=ReplyKeyboardRemove())
            await state.finish()
            return

    except Exception as e:
        await message.answer(str(e))




@dp.message_handler(state=ManageTasks.on_update_text, content_types=types.ContentTypes.TEXT)
async def process_update_text(message: types.Message, state: FSMContext):
    logging.info("Processing task text update...")
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        text = message.text
        id_ = await state.get_data()
        id_ = id_["id_"]
        session.query(Task).filter(Task.id_ == id_).update({Task.task:text}, synchronize_session=False)
        session.commit()
        
    except Exception as e:
        await message.answer(str(e))




@dp.message_handler(state=ManageTasks.on_update_priority, content_types=types.ContentTypes.TEXT)
async def process_update_priority(message: types.Message, state: FSMContext):
    logging.info("Processing task priority update...")
    if message.text == "Зеленый":
        Session = sessionmaker(bind=engine)
        session = Session()
        id_ = await state.get_data()
        id_ = id_["id_"]
        session.query(Task).filter(Task.id_ == id_).update({Task.priority:0}, synchronize_session=False)
        session.commit()
    elif message.text == "Желтый":
        Session = sessionmaker(bind=engine)
        session = Session()
        id_ = await state.get_data()
        id_ = id_["id_"]
        session.query(Task).filter(Task.id_ == id_).update({Task.priority:1}, synchronize_session=False)
    elif message.text == "Красный":
        Session = sessionmaker(bind=engine)
        session = Session()
        id_ = await state.get_data()
        id_ = id_["id_"]
        session.query(Task).filter(Task.id_ == id_).update({Task.priority:2},synchronize_session=False)
        session.commit()
    elif message.text == "Cancel":
        await message.answer("Выхожу из интерфейса.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return





