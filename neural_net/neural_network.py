
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class NeuralNetwork:
    def __init__(self, input_size: int, hidden_layers: list, output_size: int):
        self.weights = []
        self.biases = []
        prev_layer_nodes = input_size
        for layer_nodes in tuple(hidden_layers) + (output_size,):
            self.weights.append(np.random.rand(prev_layer_nodes, layer_nodes))
            self.biases.append(np.random.rand(prev_layer_nodes, 1))
            prev_layer_nodes = layer_nodes

        self.output = None
    
    def feed_forward(self, input_values):
        layer = sigmoid(np.dot(input_values, self.weights[0]) + self.biases[0])
        for weights, biases in zip(self.weights[1:], self.biases[1:]):
            layer = sigmoid(np.dot(layer, weights) + biases)
        self.output = layer
        return self.output

