from random import shuffle
from collections import deque
from copy import deepcopy
from time import time
from pygame.time import Clock

from config.tetris import HORIZONTAL_BLOCKS, VERTICAL_BLOCKS, SPAWN_POS, GRAVITY, MAX_DELAY, DELAY_LEEWAY, DEFAULT_DELAY, STEP_RATE
from game.piece import Piece
from game.piece_data import PieceType, RotationType
from game.actions import Action


class Tetris:
    def __init__(self):
        self.clock = Clock()
        self.board = [[None for _ in range(HORIZONTAL_BLOCKS)] for _ in  range(VERTICAL_BLOCKS)]
        self.piece_queue = deque()
        self.cur_piece = None
        self.held_piece = None
        self.swapped = False
        self.piece_done = False
        self.game_over = False
        self.last_step = 0 # time passed since alst grav
        self.done_delay = DEFAULT_DELAY # amount to delay before next piece
        self.last_ev = 0 # last time piece was moved
    
    def check_queue(self):
        if len(self.piece_queue) <= PieceType.NUM_TYPES.value:
            types = list(PieceType)[:-2]
            shuffle(types)
            self.piece_queue.extend(types)
    
    def spawn_piece(self):
        piece_type = self.piece_queue.popleft()
        self.cur_piece = Piece(piece_type, SPAWN_POS)

        if not self.cur_piece.check_rotation_pos_fits(self.board):
            self.game_over = True
            self.cur_piece = None
            print('GAME OVER')

    def lower_piece(self):
        try:
            self.cur_piece.translate(self.board, 0, 1)
        except:
            pass
    
    def swap_help_cur_piece(self):
        if not self.swapped:
            if not self.held_piece:
                self.held_piece = self.cur_piece
                self.spawn_piece()
            else:
                tmp = self.cur_piece
                self.cur_piece = self.held_piece
                self.held_piece = tmp
                self.cur_piece.pos = SPAWN_POS

            self.swapped = True

    def check_piece_done(self):
        return self.cur_piece.check_at_bottom(self.board)

    def move_piece_left(self):
        try:
            self.cur_piece.translate(self.board, -1, 0)
            return True
        except:
            return False
    
    def move_piece_right(self):
        try:
            self.cur_piece.translate(self.board, 1, 0)
            return True
        except:
            return False
    
    def rotate_piece_clockwise(self):
        return self.cur_piece.rotate(self.board, RotationType.CLOCKWISE)
    
    def rotate_piece_counterclockwise(self):
        return self.cur_piece.rotate(self.board, RotationType.COUNTER_CLOCKWISE)

    def settle_piece(self):
        if not self.check_piece_done():
            raise Exception('Attempting to settle piece that is not at bottom')

        self.board = self.cur_piece.add_to_board(self.board)
        self.clear_lines()
        self.check_queue()
        self.spawn_piece()
        self.swapped = False
    
    def hard_drop(self):
        while not self.check_piece_done():
            self.lower_piece()
        self.settle_piece()
    
    def clear_lines(self):
        rows_to_clear = []
        for row_ind in reversed(range(VERTICAL_BLOCKS)):
            cleared = True
            for block in self.board[row_ind]:
                if block is None: cleared = False
            if cleared:
                self.board[row_ind] = [None for _ in range(HORIZONTAL_BLOCKS)]
                rows_to_clear.append(row_ind)
        
        if not rows_to_clear:
            return

        rows_to_clear.append(-1)
        last_row = rows_to_clear[0]
        for shift_amt in range(len(rows_to_clear)):
            if shift_amt == 0: continue
            row_ind = rows_to_clear[shift_amt]
            for shift_row in range(last_row - 1, row_ind, -1):
                self.board[shift_row + shift_amt] = deepcopy(self.board[shift_row])
            last_row = row_ind
    
    def start(self):
        self.check_queue()
        self.spawn_piece()

    def action(self, action):
        if self.game_over: return

        action_complete = False

        if action == Action.MOVE_LEFT:
            action = self.move_piece_left()
        elif action == Action.MOVE_RIGHT:
            action = self.move_piece_right()
        elif action == Action.HARD_DROP:
            self.hard_drop()
        elif action == Action.MOVE_DOWN:
            self.lower_piece()
        elif action == Action.ROTATE:
            action = self.rotate_piece_clockwise()
        elif action == Action.SWAP_HELD:
            self.swap_help_cur_piece()
        
        if action_complete:
            self.last_ev = time()*1000

    def check_time_to_step(self):
        if self.game_over:
            return False

        if self.piece_done:
            if self.last_ev < DELAY_LEEWAY:
                self.done_delay += DELAY_LEEWAY
                if self.done_delay < MAX_DELAY:
                    return False
            if not self.check_piece_done():
                self.piece_done = False

        elif self.last_step < GRAVITY:
            self.done_delay = 0
            self.last_step += self.clock.get_time()
            return False
        
        self.done_delay = DEFAULT_DELAY
        self.last_step = 0

        return True

    def step(self):
        if self.check_time_to_step():
            if self.piece_done:
                self.settle_piece()
                self.piece_done = False

            elif self.check_piece_done():
                self.piece_done = True

            else:
                self.lower_piece()

        self.clock.tick(STEP_RATE)

    def get_projection(self):
        if not self.cur_piece: return
        ghost = Piece(self.cur_piece.type, self.cur_piece.pos, self.cur_piece.rotation)
        while not ghost.check_at_bottom(self.board):
            ghost.translate(self.board, 0, 1)
        return ghost

    def get_board(self):
        board = deepcopy(self.board)
        if self.cur_piece:
            board = self.cur_piece.add_to_board(board)
            board = self.get_projection().add_to_board(board, True)
        return board

    def __str__(self):
        s = ''
        for r in self.get_board():
            for block in r:
                if block is None:
                    s += '*'
                else:
                    s += block.name
            s += '\n'
        return s
    
