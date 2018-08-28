from NEAT.config import MAX_GENERATIONS, POPULATION_SIZE
from NEAT.genome import Genome
from NEAT.population import Population

def run_neat(inp_nodes, out_nodes, evaluator_func):
    Genome.init_io_nodes(inp_nodes, out_nodes)
    seed_orgs = []
    for _ in range(POPULATION_SIZE):
        genome = Genome()
        genome.basic_init()
        seed_orgs.append(genome)

    population = Population(seed_orgs, evaluator_func)

    while population.generation < MAX_GENERATIONS:
        population.next_generation()

    return population.best_org