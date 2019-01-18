from apps.view_lib.view import GameView
from apps.tetris.view.tetris_view import TetrisView
from apps.tetris.config import WINDOW_HEIGHT, WINDOW_WIDTH

if __name__ == '__main__':
    app = GameView(controller=TetrisView())
    app.run()
