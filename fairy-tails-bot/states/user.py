from aiogram.fsm.state import State, StatesGroup


class MainWindow(StatesGroup):
    start = State() # just useless state to start either left dialog or right dialog


class AllUsersTails(StatesGroup):
    main = State() # gives all users tails


class Profile(StatesGroup):
    my_profile = State() 
    subscription = State() # main window with all types of "subscription"


class Tail(StatesGroup):
    # set child settings
    all_child_settings = State()
    gender = State()
    name = State()
    age = State()
    activities = State()
    send_data = State() # switch to state Tail.main with setted data (data locates in manager.dialog_data)
    
    # tail
    tail = State() # window for tail's plot(1 season) with photo
    
    episode = State() # every click gets new data
    
    episode_ended = State() # user see this window only when he've just bought this tail and if he has scrolled all episodes.
                            # he can't scroll episodes back. He can do it only in his profile

    # single window says that user dont have subscription 
    user_dont_have_subscription = State()
