from aiogram.dispatcher.filters.state import State, StatesGroup


class AddTask(StatesGroup):
    waiting_for_task = State()
    waiting_for_date = State()
    waiting_for_priority = State()


class ManageTasks(StatesGroup):
    waiting_for_task_choice = State()
    waiting_for_action_choice = State()
    on_delete = State()
    on_update = State()
    on_update_date = State()
    on_update_text = State()
    on_update_priority = State()