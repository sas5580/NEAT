import pickle
import argparse

from apps.view_lib.view import GameView
from apps.snake.view import SnakeView
from apps.snake.game import Snake
from apps.snake.train import play_snake_with_view


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play Snake')
    parser.add_argument('genome', nargs='?', default=None)
    parser.add_argument('--speed', required=False, type=float, default=3.0)
    args = parser.parse_args()
    print(args)

    if args.genome is not None:
        with open(args.genome, 'rb') as f:
            org = pickle.load(f)
        play_snake_with_view(org, args.speed)

    else:
        app = GameView(controller=SnakeView(Snake(speed_multiplier=args.speed)))
        app.run()
