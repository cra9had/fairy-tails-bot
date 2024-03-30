from aiogram.fsm.state import State, StatesGroup


class MainWindow(StatesGroup):
    my_profile = State()


class AllUsersTails(StatesGroup):
    main = State() # gives all users tails


class ChildSettings(StatesGroup):
    main = State()
    gender = State()
    name = State()
    age = State()
    activities = State()
    send_data = State() # switch to state Tail.main with setted data (data locates in manager.dialog_data)


class Tail(StatesGroup):
    main = State() # window for tail's plot(1 season) with photo
    current_episode = State() # for example 1 / 10 episode
    episode_ended = State() # user see this window only when he've just bought this tail and if he has scrolled all episodes.
                            # he can't scroll episodes back. He can do it only in his profile


class Episode(StatesGroup):
    main = State() # every click gets new data


class UserDontHaveSubcription(StatesGroup):
    main = State()


class Subscription(StatesGroup):
    main = State() # main window with all types of "subscription"