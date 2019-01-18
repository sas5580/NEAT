from apps.view_lib.view import GameView
from apps.snake.view import SnakeView
from apps.snake.game import Snake

if __name__ == '__main__':
    app = GameView(controller=SnakeView(Snake(speed_multiplier=1.0)))
    app.run()
