from NEAT.random import random

from NEAT.config import WEIGHT_MUTATION_POWER, WEIGHT_CAP, PERTRUBE_WEIGHT_PROB, RANDOM_WEIGHT_PROB

class ConnectionGene:
    INNOVATION_COUNT = 0
    INNOVATION_MAP = {}

    @classmethod
    def getInnovation(cls, in_node, out_node):
        return cls.INNOVATION_MAP.get((in_node, out_node))

    @classmethod
    def addInnovation(cls, in_node, out_node):
        if cls.getInnovation(in_node, out_node) is not None:
            raise Exception(f'Cannot add existing innovation {in_node}, {out_node}')
        cls.INNOVATION_COUNT += 1
        cls.INNOVATION_MAP[in_node, out_node] = cls.INNOVATION_COUNT
        return cls.INNOVATION_COUNT

    def __init__(self, in_node, out_node, weight = None, disable_chance = 0.0):
        assert in_node.depth < out_node.depth, f'in {in_node} has depth {in_node.depth}, out {out_node} has depth {out_node.depth}'

        self.innovation = self.getInnovation(in_node, out_node)
        if self.innovation is None:
            self.innovation = self.addInnovation(in_node, out_node)

        self.in_ = in_node
        self.out = out_node
        self.weight = random.uniform(-1, 1) if weight is None else weight
        self.enabled = random.uniform(0, 1) >= disable_chance

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def clone(self):
        return ConnectionGene(self.in_, self.out, self.weight, 0 if self.enabled else 1)

    def mutateWeight(self):
        rand = random.uniform(0, 1)
        if rand < RANDOM_WEIGHT_PROB:
            self.weight = random.uniform(-1, 1)
        elif rand < PERTRUBE_WEIGHT_PROB:
            self.weight += random.gauss(0, 1)*WEIGHT_MUTATION_POWER
            self.weight = max(min(self.weight, WEIGHT_CAP), -WEIGHT_CAP)

    def __repr__(self):
        return f'({self.innovation}) {self.in_} -> {self.out}: {self.weight} {"E" if self.enabled else "D"}'