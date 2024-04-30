from enum import Enum, auto


class ChainType(Enum):
    START = auto()
    SUBSCRIBE = auto()
    SECOND_CHAPTER = auto()


class ChainStage(Enum):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()
