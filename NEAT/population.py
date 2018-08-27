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
                Organism(1, genome)
            )

        self.species = []
        self.speciate(self.organisms)
        self.evaluator_func = evaluator_func
        self.best_org = None
        self.calculate_fitness()

    def calculate_fitness(self):
        best_fitness = -1e9
        best_org = None
        for org in self.organisms:
            network = Network(org.genome.nodes, org.genome.bias, org.genome.connections)
            org.fitness = self.evaluator_func(network)
            if best_fitness > org.fitness:
                best_org = org

        if self.best_org is None or best_fitness > self.best_org.fitness:
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

        # Adjust fitness based on species size and stagnance
        # Kill off bottom of species (param for amount)
        # Calculate average fitnesses of each species
        # Kill stagnant species
        # Kill crappy species
        # give children to species based on how much they contribute to the entire sum of average fitnesses
        # If not enough children, create more from best species
        # Speciate based on old organsisms
        # delete old organisms from population and species
        population_size = len(self.organisms)
        average_fitness_sum = 0.0

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

        expected_orgs = len(self.organisms)
        children = []
        for sp in self.species:
            children.append(Organism(self.generation, sp.organisms[0].genome))

            num_children = (sp.average_adjusted_fitness / average_fitness_sum * expected_orgs) - 1
            for _ in range(num_children):
                children.append(sp.reproduce(self.generation))

        self.speciate(children)
        for sp in self.species:
            sp.wipe_older_generations()

        self.organisms = children

        self.calculate_fitness()

    def get_best(self):
        return max(self.organisms, key=attrgetter('fitnesss'))