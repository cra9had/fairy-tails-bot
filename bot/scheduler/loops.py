import enum

from bot.texts.task_texts import *


class Loop1(enum.Enum):
    def __init__(self, hour: int, text: str):
        self.hour = hour
        self.text = text

    task_1 = (1, LOOP1_1)
    task_2 = (24, LOOP1_2)
    task_3 = (48, LOOP1_3)
    done = (0, 'finished')


class Loop2(enum.Enum):
    def __init__(self, hour: int, text: str):
        self.hour = hour
        self.text = text

    task_1 = (1, LOOP2_1)
    task_2 = (24, LOOP2_2)
    task_3 = (24, LOOP2_3)
    done = (0, 'finished')


class Loop3(enum.Enum):
    def __init__(self, hour: int, text: str):
        self.hour = hour
        self.text = text

    task_1 = (24, LOOP3_1)
    task_2 = (48, LOOP3_2)
    task_3 = (72, LOOP3_3)
    done = (0, 'finished')


class Loop4(enum.Enum):
    def __init__(self, hour: int, text: str):
        self.hour = hour
        self.text = text

    task_1 = (24, LOOP4_1)
    task_2 = (48, LOOP4_2)
    task_3 = (72, LOOP4_3)
    done = (0, 'finished')
