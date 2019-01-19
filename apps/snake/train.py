import pickle
import datetime
import math
from enum import Enum
from functools import partial

from apps.snake.config import GRID_SIZE
from apps.snake.actions import Action
from apps.snake.game import Snake
from apps.snake.view import SnakeView
from apps.view_lib.view import GameView
from NEAT.network import Network
from NEAT.neat import run_neat
from NEAT.drawing import draw_genome


class Output(Enum):
    LEFT = -1
    FORWARD = 0
    RIGHT = 1

    @staticmethod
    def get_dir(out, cur):
        return Action((cur.value + out.value) % Action.SIZE.value)


def calculate_fitness(game):
    return game.score * 100 + game.steps / 100

def make_move(game, network, state=None):
    inp = []
    for out in Output:
        diff = Snake.DIR_MAP[Output.get_dir(out, game.direction)]
        x, y = (game.positions[-1][0] + diff[0], game.positions[-1][1] + diff[1])
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE or (x, y) in game.positions:
            inp.append(1)
        else:
            inp.append(0)

    head = game.positions[-1]
    food = game.food
    if game.direction == Action.UP:
        angle = math.atan2(food[0] - head[0], food[1] - head[1])
    elif game.direction == Action.DOWN:
        angle = math.atan2(head[0] - food[0], head[1] - food[1])
    elif game.direction == Action.LEFT:
        angle = -math.atan2(head[1] - food[1], head[0] - food[0])
    elif game.direction == Action.RIGHT:
        angle = -math.atan2(food[1] - head[1], food[0] - head[0])
    else:
        assert False

    inp.append(angle / math.pi)

    scores = []
    for out in Output:
        scores.append(next(network.activate(inp + [out.value])))

    action = [Output.LEFT, Output.FORWARD, Output.RIGHT][
        scores.index(max(scores))
    ]

    game.action(Output.get_dir(action, game.direction))

def play_snake(network):
    game = Snake(speed_multiplier=1e9)
    game.MOVE_RATE = 0
    game.start()

    no_score_change = 0
    while not game.game_over and no_score_change < 500:
        score = game.score
        make_move(game, network)
        game.step()

        if score != game.score:
            no_score_change = 0
        else:
            no_score_change += 1

    fitness = calculate_fitness(game)
    if no_score_change >= 500:
        fitness -= 4.99

    return fitness

def snake_fitness(network):
    scores = (play_snake(network) for _ in range(5))
    return sum(scores) / 5

def play_snake_with_view(network):
    game = Snake()

    move_fn = partial(make_move, game, network)

    view = GameView(controller=SnakeView(game), ai_controller=move_fn)
    view.run()

org = run_neat(5, 1, snake_fitness, population=200, generations=200)

draw_genome(org.genome, 'best_snake')
with open(f'apps/snake/genomes/{datetime.date.today()}_{org.fitness:.2f}.pickle', 'wb') as f:
    pickle.dump(org, f)

#play_snake_with_view(Network(org.genome.nodes, org.genome.bias_node, org.genome.connections))
