from NEAT.neat import run_neat

XOR_IO = (((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0))
MAX_FITNESS = 4

def xor_fitness(network):
    fitness = 0
    for inp, out in XOR_IO:
        fitness += (out - next(network.activate(inp))) ** 2
    return MAX_FITNESS - fitness

def xor_test():
    return run_neat(2, 1, xor_fitness)