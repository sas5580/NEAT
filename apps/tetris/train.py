import pickle
import datetime
import multiprocessing as mp
import multiprocessing.dummy as threading

from apps.tetris.config import HORIZONTAL_BLOCKS, VERTICAL_BLOCKS, STEP_RATE, NUM_GAMES_PER_GENOME, SPEED_MULTIPLIER_TRAINING
from apps.tetris.game.actions import Action
from apps.tetris.game.tetris import Tetris
from apps.tetris.view.tetris_view import TetrisView
from apps.view_lib.view import GameView
from NEAT.network import Network
from NEAT.neat import run_neat

ACTION_MAP = {
    0: Action.MOVE_LEFT,
    1: Action.MOVE_RIGHT,
    2: Action.ROTATE,
}


def calculate_fitness(game):
    return game.score * 10 + game.steps / 1000


def play_tetris(network):
    game = Tetris(speed_multiplier=SPEED_MULTIPLIER_TRAINING)
    game.start()
    force_drop_count = 0
    while not game.game_over:
        if force_drop_count > STEP_RATE:
            game.action(Action.HARD_DROP)
            force_drop_count = 0

        inp = []
        for row in game.get_board():
            for piece in row:
                inp.append(True if piece is not None else False)
        out = list(network.activate(inp))
        action = ACTION_MAP[out.index(max(out))]
        game.action(action)

        game.step()
        force_drop_count += 1
    fitness = calculate_fitness(game)

    return fitness

def tetris_fitness(network):
    scores = map(play_tetris, [network] * NUM_GAMES_PER_GENOME)
    return sum(scores) / NUM_GAMES_PER_GENOME

def play_tetris_with_view(network):
    game = Tetris()

    def make_move(state):
        if state['force_drop_count'] > STEP_RATE:
            game.action(Action.HARD_DROP)
            state['force_drop_count'] = 0

        inp = []
        for row in game.get_board():
            for piece in row:
                inp.append(True if piece is not None else False)
        out = list(network.activate(inp))
        action = ACTION_MAP[out.index(max(out))]
        game.action(action)

        state['force_drop_count'] += 1

    view = GameView(controller=TetrisView(game), ai_controller=make_move, ai_state={'force_drop_count': 0})
    view.run()

org = run_neat(HORIZONTAL_BLOCKS*VERTICAL_BLOCKS, len(ACTION_MAP), tetris_fitness)

with open(f'apps/tetris/genomes/{datetime.date.today()}_{org.fitness:.2f}.pickle', 'wb') as f:
    pickle.dump(org, f)

play_tetris_with_view(Network(org.genome.nodes, org.genome.bias_node, org.genome.connections))
