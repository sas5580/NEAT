import random
from collections import deque
from time import time
from pygame.time import Clock

from apps.snake.config import GRID_SIZE, STEP_RATE, MOVE_RATE
from apps.snake.actions import Action


class Snake:
    DIR_MAP = {
        Action.LEFT: (-1, 0),
        Action.UP: (0, -1),
        Action.RIGHT: (1, 0),
        Action.DOWN: (0, 1)
    }

    def __init__(self, speed_multiplier=1.0):
        self.STEP_RATE = STEP_RATE * speed_multiplier
        self.MOVE_RATE = MOVE_RATE / speed_multiplier

        self.clock = Clock()
        self.last_step = 0

        self.direction = Action.RIGHT
        self.prestep_direction = self.direction
        self.positions = deque(((3, 3), (3, 4), (3, 5)))
        self.food = None
        self.game_over = False

        self.score = 0
        self.steps = 0

    def start(self):
        self.spawn_food()

    def spawn_food(self):
        pos = {(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)} - set(self.positions)
        self.food = random.sample(pos, 1)[0]

    def move(self):
        diff = Snake.DIR_MAP[self.direction]
        nxt = (self.positions[-1][0] + diff[0], self.positions[-1][1] + diff[1])

        if nxt[0] < 0 or nxt[0] >= GRID_SIZE or nxt[1] < 0 or nxt[1] >= GRID_SIZE or nxt in self.positions:
            self.game_over = True
            return

        self.positions.append(nxt)

        if nxt == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.positions.popleft()

    def action(self, action):
        if self.game_over: return
        if Action.can_move(self.direction, action):
            self.prestep_direction = action

    def check_time_to_step(self):
        return (time() - self.last_step) * 1000 >= self.MOVE_RATE

    def step(self):
        if not self.game_over and self.check_time_to_step():
            self.direction = self.prestep_direction
            self.move()

            self.last_step = time()
            self.steps += 1

        self.clock.tick(self.STEP_RATE)

    def __str__(self):
        s = ''
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (c, r) in self.positions:
                    s += 'X'
                elif (c, r) == self.food:
                    s += 'O'
                else:
                    s += ' '
            s += '\n'
        return s
