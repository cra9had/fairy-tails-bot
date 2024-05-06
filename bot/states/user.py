from aiogram.fsm.state import State, StatesGroup


class MainWindow(StatesGroup):
    gender = State()
    age = State()
    activities = State()
    name = State()
    all_child_settings = State()
    wait_tail = State()

    channel_subscription = State()
    wait_episode = State()
    episode = State()

    bad_balance = State()

class Subscription(StatesGroup):
    discount = State()
    plans = State()
    subscription = State()
