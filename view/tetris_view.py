import pygame as pg
from pygame.locals import *

from config.tetris import *
from game.tetris import Tetris
from game.piece_data import PieceType

VERTICAL_BLOCKS -= 1

PIECE_COLORS = {
    PieceType.I: (80, 248, 253),
    PieceType.J: (47, 2, 251), 
    PieceType.L: (248, 168, 6),
    PieceType.O: (252, 252, 1),
    PieceType.S: (67, 255, 0),
    PieceType.T: (153, 0, 249),
    PieceType.Z: (245, 11, 3),
    PieceType.G: (150, 150, 150)
}

EMPTY_BLOCK_COLORS = ((30, 30, 30), (70, 70, 70))

GRID_LINE_COLOR = (20, 20, 20)

class TetrisView:
    def __init__(self):
        pg.init()

        self.game = Tetris()

        width = BLOCK_SIZE*HORIZONTAL_BLOCKS + 2*BORDER_DEPTH + LINES_SENT_SIZE[0] + NEXT_BOX_SIZE[0]
        height = BLOCK_SIZE*VERTICAL_BLOCKS + 2*BORDER_DEPTH + LINES_SENT_SIZE[1] + NEXT_BOX_SIZE[1]
        self.size = (width, height)
        self.surface = pg.Surface(self.size)
    
    def draw_board(self):
        
        board_surf = pg.Surface((BLOCK_SIZE*HORIZONTAL_BLOCKS, BLOCK_SIZE*VERTICAL_BLOCKS))

        for y, row in enumerate(self.game.get_board()[1:]):
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
        self.game.event(ev)

    def loop(self, clock):
        self.game.step(clock)
