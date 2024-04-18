from aiogram.fsm.state import State, StatesGroup


class MainWindow(StatesGroup):
    gender = State()
    age = State()
    activities = State()
    name = State()
    all_child_settings = State()
    wait_task = State()

    channel_subscription = State()
    tail = State()
    episode = State()


class Subscription(StatesGroup):
    plans = State()
    subscription = State()
