from enum import IntEnum


class Level(IntEnum):
    IMPORTANT_URGENT = 3
    IMPORTANT_NOT_URGENT = 2
    UNIMPORTANT_URGENT = 1
    UNIMPORTANT_NOT_URGENT = 0
