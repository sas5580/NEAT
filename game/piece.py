from copy import deepcopy

from game.piece_data import PieceType, Rotation, RotationType, PIECE_SHAPE, get_roation_checks

def print_board(b):
    s = ''
    for r in b:
        for block in r:
            if block is None:
                s += '*'
            else:
                s += block.name
        s += '\n'
    print(s)

class Piece:
    def __init__(self, type_ : PieceType, topleft : tuple, rotation: Rotation = Rotation.ZERO):
        self.pos = topleft
        self.type = type_
        self.rotation = rotation
    
    def check_rotation_pos_fits(self, board: list, rotation: Rotation, pos: tuple):
        for (dx, dy) in PIECE_SHAPE[self.type][rotation]:
            x, y = pos[0] + dx, pos[1] + dy
            if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
                return False
            if board[y][x] != None:
                return False
        return True

    def add_to_board(self, board: list, ghost: bool = False):
        if not self.check_rotation_pos_fits(board, self.rotation, self.pos):
            raise Exception(f'Cannot add ({self.type}, {self.rotation}, {self.pos}) to board')
        for (dx, dy) in PIECE_SHAPE[self.type][self.rotation]:
            board[self.pos[1] + dy][self.pos[0] + dx] = self.type if not ghost else PieceType.G
        return board

    def rotate(self, board: list, rotation_type: RotationType):
        desired_rotation = Rotation.clockwise(self.rotation) if rotation_type == RotationType.CLOCKWISE else Rotation.counter_clockwise(self.rotation)
        for (dx, dy) in get_roation_checks(self.type, self.rotation, desired_rotation):
            x, y = self.pos[0] + dx, self.pos[1] + dy
            if self.check_rotation_pos_fits(board, desired_rotation, (x, y)):
                self.pos = (x, y)
                self.rotation = desired_rotation
                return True
        return False

    def translate(self, board: list, dx: int, dy: int):
        if not self.check_rotation_pos_fits(board, self.rotation, (self.pos[0] + dx, self.pos[1] + dy)):
            raise Exception('Invalid translation')
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
    
    def check_at_bottom(self, board: list):
        if not self.check_rotation_pos_fits(board, self.rotation, self.pos):
            raise Exception('Invalid state at start of check_at_bottom')
        return not self.check_rotation_pos_fits(board, self.rotation, (self.pos[0], self.pos[1] + 1))
