from enum import Enum

class Action(Enum):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    ROTATE = 3
    HARD_DROP = 4
    SWAP_HELD = 5