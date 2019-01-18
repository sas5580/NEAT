from NEAT.neat import run_neat
from NEAT.network import Network

XOR_IO = (((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0))
MAX_FITNESS = 4

def xor_fitness(network):
    fitness = 0
    for inp, out in XOR_IO:
        fitness += (out - next(network.activate(inp))) ** 2
    return MAX_FITNESS - fitness

best = run_neat(2, 1, xor_fitness, population=100, generations=100)
print(f'Best fitness: {best.fitness}')
net = Network(best.genome.nodes, best.genome.bias_node, best.genome.connections)
for inp, _ in XOR_IO:
    print(f'{inp}: {next(net.activate(inp))}')
