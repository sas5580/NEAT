import pickle
import datetime
import multiprocessing as mp
import multiprocessing.dummy as threading

from config.tetris import HORIZONTAL_BLOCKS, VERTICAL_BLOCKS, STEP_RATE
from config.training import NUM_GAMES_PER_GENOME, SPEED_MULTIPLIER_TRAINING
from game.actions import Action
from game.tetris import Tetris
from view.view import GameView
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
    game = Tetris(speed_multiplier=1000.0)
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
    p = threading.Pool()
    scores = p.map(play_tetris, [network] * NUM_GAMES_PER_GENOME)
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

    view = GameView(game=game, ai_controller=make_move, ai_state={'force_drop_count': 0})
    view.run()

org = run_neat(HORIZONTAL_BLOCKS*VERTICAL_BLOCKS, len(ACTION_MAP), tetris_fitness, population=100, generations=100)

with open(f'genomes/{datetime.date.today()}_{org.fitness:.2f}.pickle', 'wb') as f:
    pickle.dump(org, f)

#play_tetris_with_view(Network(org.genome.nodes, org.genome.bias_node, org.genome.connections))

