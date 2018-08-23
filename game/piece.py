from copy import deepcopy

from game.piece_data import PieceType, Rotation, RotationType, PIECE_SHAPE, get_roation_checks

class Piece:
    def __init__(self, type_ : PieceType, topleft : tuple, rotation: Rotation = Rotation.ZERO):
        self.pos = topleft
        self.type = type_
        self.rotation = rotation
    
    def check_rotation_pos_fits(self, board: list, rotation: Rotation = None, pos: tuple = None):
        if rotation is None: rotation = self.rotation
        if pos is None: pos = self.pos

        for (dx, dy) in PIECE_SHAPE[self.type][rotation]:
            x, y = pos[0] + dx, pos[1] + dy
            if x < 0 or x >= len(board[0]) or y >= len(board):
                return False
            if board[y][x] != None:
                return False
        return True

    def add_to_board(self, board: list, ghost: bool = False):
        for (dx, dy) in PIECE_SHAPE[self.type][self.rotation]:
            x, y = self.pos[0] + dx, self.pos[1] + dy
            if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
                continue

            if not ghost:
                board[y][x] = self.type
            elif board[y][x] is None:
                board[y][x] = PieceType.G

        return board

    def rotate(self, board: list, rotation_type: RotationType):
        desired_rotation = Rotation.clockwise(self.rotation) if rotation_type == RotationType.CLOCKWISE else Rotation.counter_clockwise(self.rotation)
        for (dx, dy) in get_roation_checks(self.type, self.rotation, desired_rotation):
            x, y = self.pos[0] + dx, self.pos[1] + dy
            if self.check_rotation_pos_fits(board, rotation = desired_rotation, pos = (x, y)):
                self.pos = (x, y)
                self.rotation = desired_rotation
                return True
        return False

    def translate(self, board: list, dx: int, dy: int):
        if not self.check_rotation_pos_fits(board, pos = (self.pos[0] + dx, self.pos[1] + dy)):
            raise Exception('Invalid translation')
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
    
    def check_at_bottom(self, board: list):
        if not self.check_rotation_pos_fits(board):
            raise Exception('Invalid state at start of check_at_bottom')
        return not self.check_rotation_pos_fits(board, pos = (self.pos[0], self.pos[1] + 1))
