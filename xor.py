import pickle

from NEAT.test import xor_test
from NEAT.drawing import draw_genome
from NEAT.network import Network

best = xor_test()
draw_genome(best.genome, f'best {round(best.fitness, 2)}')

for i in (0, 0), (0, 1), (1, 0), (1, 1):
    net = Network(best.genome.nodes, best.genome.bias_node, best.genome.connections)
    print(f'{i}: {next(net.activate(i))}')

with open('best_genome.pickle', 'wb') as f:
        pickle.dump(best, f)