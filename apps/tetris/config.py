from apps.tetris.game.piece_data import PieceType

# Game
HORIZONTAL_BLOCKS = 10
VERTICAL_BLOCKS = 20
DROP_SPEED = 1 # second
SPAWN_POS = (3, 0)

GRAVITY = 1000 # milliseconds between each move down
DEFAULT_DELAY = 500
MAX_DELAY = 2200 # milliseconds
DELAY_LEEWAY = 300 # milliseconds
STEP_RATE = 24 # per second


# Display
WINDOW_HEIGHT = 600 # px
WINDOW_WIDTH = 450 # px
BLOCK_SIZE = 30 # px
LINES_SENT_SIZE = (50, 50)
NEXT_BOX_SIZE = (100, 300)
BORDER_DEPTH = 20

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

# Training
NUM_GAMES_PER_GENOME = 5
SPEED_MULTIPLIER_TRAINING = 100