import multiprocessing as mp
from operator import attrgetter

from NEAT.config import STAGNANT_SPECIES_AGE_DIFF
from NEAT.network import Network
from NEAT.species import Species
from NEAT.organism import Organism


class Population:
    def __init__(self, seed_genomes, evaluator_func):
        self.generation = 0
        self.max_fitness = 0
        self.organisms = []
        for genome in seed_genomes:
            self.organisms.append(
                Organism(0, genome)
            )

        self.species = []
        self.speciate(self.organisms)
        self.evaluator_func = evaluator_func
        self.best_org = None
        self.calculate_fitness()

    def calculate_fitness(self):
        pool = mp.Pool(mp.cpu_count())

        nets = (Network(org.genome.nodes, org.genome.bias_node, org.genome.connections) for org in self.organisms)

        best_org = None
        for org, fitness in zip(self.organisms, pool.map(self.evaluator_func, nets)):
            org.fitness = fitness
            if not best_org or org.fitness > best_org.fitness:
                best_org = org
        print(f'Best fitness this geneartion: {best_org.fitness}')
        if self.best_org is None or best_org.fitness > self.best_org.fitness:
            self.best_org = best_org

    def speciate(self, organisms):
        for org in organisms:
            specie = None
            for sp in self.species:
                if sp.compatible(org):
                    specie = sp
                    sp.add(org)
                    break

            if specie is None:
                specie = Species(org)
                self.species.append(specie)


    def next_generation(self):
        self.generation += 1
        print(f'Beginning Generation {self.generation}')

        population_size = len(self.organisms)
        average_fitness_sum = 0.0

        print(f'Num Species: {len(self.species)}')
        for sp in self.species:
            sp.new_gen()
            sp.compute_adjusted_fitness()
            sp.sort_and_cull()
            average_fitness_sum += sp.average_adjusted_fitness

        sp_index = len(self.species)
        ave_fit_sum_copy = average_fitness_sum
        while sp_index > 0:
            sp_index -= 1
            sp = self.species[sp_index]
            if sp.age - sp.last_improved_age >= STAGNANT_SPECIES_AGE_DIFF:
                average_fitness_sum -= sp.average_adjusted_fitness
                del self.species[sp_index]
            elif sp.average_adjusted_fitness/ave_fit_sum_copy*population_size < 1:
                average_fitness_sum -= sp.average_adjusted_fitness
                del self.species[sp_index]

        print(f'Num Species after cull: {len(self.species)}')

        expected_orgs = len(self.organisms)
        children = []
        best_species = None
        for sp in self.species:
            if not best_species or sp.average_adjusted_fitness > best_species.average_adjusted_fitness:
                best_species = sp

            children.append(Organism(self.generation, sp.organisms[0].genome))
            num_children = (sp.average_adjusted_fitness / average_fitness_sum * expected_orgs) - 1

            for _ in range(int(num_children)):
                children.append(sp.reproduce(self.generation))

        num_childs = len(children)
        while num_childs < expected_orgs:
            children.append(best_species.reproduce(self.generation))
            num_childs += 1

        self.speciate(children)

        sp_index = len(self.species)
        ave_fit_sum_copy = average_fitness_sum
        while sp_index > 0:
            sp_index -= 1
            self.species[sp_index].wipe_older_generations(self.generation)
            if not self.species[sp_index].organisms:
                del self.species[sp_index]

        self.organisms = children

        self.calculate_fitness()

    def get_best(self):
        return max(self.organisms, key=attrgetter('fitnesss'))

    def verify(self):
        for org in self.organisms: org.verify()