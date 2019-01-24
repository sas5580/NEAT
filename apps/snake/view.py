import pygame as pg
from pygame.locals import *

from apps.snake.config import BLOCK_SIZE, GRID_SIZE, BACKGROUND_COLOUR, SNAKE_COLOUR, HEAD_COLOUR, FOOD_COLOUR
from apps.snake.game import Snake
from apps.snake.actions import Action


class SnakeView:
    def __init__(self, game=None):
        pg.init()

        self.game = game or Snake()

        self.size = (BLOCK_SIZE * GRID_SIZE, BLOCK_SIZE * GRID_SIZE)
        self.surface = pg.Surface(self.size)

    def window_size(self):
        return self.size

    def draw_board(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                rect = (c*BLOCK_SIZE, r*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if (c, r) == self.game.food:
                    pg.draw.rect(self.surface, FOOD_COLOUR, rect, 0)
                elif (c, r) == self.game.positions[-1]:
                    pg.draw.rect(self.surface, HEAD_COLOUR, rect, 0)
                elif (c, r) in self.game.positions:
                    pg.draw.rect(self.surface, SNAKE_COLOUR, rect, 0)
                else:
                    pg.draw.rect(self.surface, BACKGROUND_COLOUR, rect, 0)
                pg.draw.rect(self.surface, BACKGROUND_COLOUR, rect, 1)

    def draw(self):
        self.draw_board()
        return self.surface

    def init(self):
        self.game.start()

    def on_event(self, ev):
        action = None
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_UP:
                action = Action.UP
            elif ev.key == pg.K_RIGHT:
                action = Action.RIGHT
            elif ev.key == pg.K_DOWN:
                action = Action.DOWN
            elif ev.key == pg.K_LEFT:
                action = Action.LEFT

        if action:
            self.game.action(action)

    def loop(self):
        self.game.step()
        return not self.game.game_over
