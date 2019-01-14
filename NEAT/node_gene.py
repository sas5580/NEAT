from enum import Enum


class NodeGene:
    class Type:
        INPUT = 0
        OUTPUT = 1
        HIDDEN = 2
        BIAS = INPUT

    @classmethod
    def orientNodes(cls, node1, node2):
        if node2.type == cls.Type.INPUT or node1.type == cls.Type.OUTPUT:
            return node2, node1
        elif node1.depth > node2.depth:
            return node2, node1
        return node1, node2

    ID_COUNT = 0
    NODE_MAP = {}
    def __init__(self, type_, depth):
        NodeGene.ID_COUNT += 1
        self.id = NodeGene.ID_COUNT
        self.type = type_
        self.depth = depth

        NodeGene.NODE_MAP[self.id] = self

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return f'Node {self.id} ({self.depth})'