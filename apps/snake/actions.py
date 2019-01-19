from enum import Enum

class Action(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    SIZE = 4

    @classmethod
    def can_move(cls, cur, to):
        return cur.value not in (to.value, (to.value + 2) % 4)
