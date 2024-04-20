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

    # @property
    # def hour(self):
    #     return self.value[0]
    #
    # @property
    # def text(self):
    #     return self.value[1]
