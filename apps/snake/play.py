import sys
import pickle

from apps.view_lib.view import GameView
from apps.snake.view import SnakeView
from apps.snake.game import Snake
from apps.snake.train import play_snake_with_view


if __name__ == '__main__':
    if len(sys.argv) > 1:
        genome_path = sys.argv[1]
        with open(genome_path, 'rb') as f:
            org = pickle.load(f)
        play_snake_with_view(org)

    else:
        app = GameView(controller=SnakeView(Snake(speed_multiplier=1.0)))
        app.run()
