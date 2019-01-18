import pygame as pg
from pygame.locals import *

from apps.tetris.config import *
from apps.tetris.game.tetris import Tetris
from apps.tetris.game.piece_data import PieceType
from apps.tetris.game.actions import Action


class TetrisView:
    @staticmethod
    def window_size():
        return (WINDOW_WIDTH, WINDOW_HEIGHT)

    def __init__(self, game=None):
        pg.init()

        self.game = game or Tetris()

        width = BLOCK_SIZE*HORIZONTAL_BLOCKS + 2*BORDER_DEPTH + LINES_SENT_SIZE[0] + NEXT_BOX_SIZE[0]
        height = BLOCK_SIZE*VERTICAL_BLOCKS + 2*BORDER_DEPTH + LINES_SENT_SIZE[1] + NEXT_BOX_SIZE[1]
        self.size = (width, height)
        self.surface = pg.Surface(self.size)

    def draw_board(self):

        board_surf = pg.Surface((BLOCK_SIZE*HORIZONTAL_BLOCKS, BLOCK_SIZE*VERTICAL_BLOCKS))

        for y, row in enumerate(self.game.get_board()):
            for x, block in enumerate(row):
                rect = (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if block is None:
                    pg.draw.rect(board_surf, EMPTY_BLOCK_COLORS[(x + y) % 2], rect, 0)
                else:
                    pg.draw.rect(board_surf, PIECE_COLORS[block], rect, 0)
                pg.draw.rect(board_surf, GRID_LINE_COLOR, rect, 1)
        self.surface.blit(board_surf, (LINES_SENT_SIZE[0], 0))

    def init(self):
        self.game.start()

    def draw(self):
        self.draw_board()
        return self.surface

    def on_event(self, ev):
        action = None
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_UP:
                action = Action.ROTATE
            elif ev.key == pg.K_RIGHT:
                action = Action.MOVE_RIGHT
            elif ev.key == pg.K_DOWN:
                action = Action.MOVE_DOWN
            elif ev.key == pg.K_LEFT:
                action = Action.MOVE_LEFT
            elif ev.key == pg.K_SPACE:
                action = Action.HARD_DROP
            elif ev.key == pg.K_LSHIFT:
                action = Action.SWAP_HELD

        if action: self.game.action(action)

    def loop(self):
        self.game.step()
