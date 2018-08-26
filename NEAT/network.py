from operator import attrgetter
from math import exp


def sigmoid(x):
    return 1/(1 + exp(-4.9*x))

class Network:
    def __init__(self, nodes, bias, connections):
        # First node in depth 0 is always bias
        self.node_depths = [[bias]]
        self.graph = {bias: []}
        self.activations = {bias: 1.0}

        for node in nodes:
            while node.depth >= len(self.node_depths):
                self.node_depths.append([])
            self.node_depths[node.depth].append(node)

            self.graph[node] = []

            self.activations[node] = None

        self.node_depths[0].sort(key=attrgetter('id'))
        self.node_depths[-1].sort(key=attrgetter('id'))

        for connection in connections.values():
            if connection.enabled:
                self.graph[connection.out].append((connection.in_, connection.weight))

    def activate(self, inputs):
        assert(len(inputs) == len(self.node_depths[0]) - 1)

        for i, val in enumerate(inputs):
            self.activations[self.node_depths[0][i+1]] = val

        for nodes in self.node_depths[1:]:
            for node in nodes:
                activation = 0
                for inode, weight in self.graph[node]:
                    activation += self.activations[inode]*weight
                self.activations[node] = sigmoid(activation)

        for node in self.node_depths[-1]:
            yield self.activations[node]
