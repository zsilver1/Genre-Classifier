from dataTypes import FeatureVector
import math


class Perceptron:
    def __init__(self, input_data):
        self.weights = FeatureVector()
        self.input_data = input_data
        # add bias to output
        self.bias = 0
        self.outputError = 0

    def computeOutput(self):
        return self.input_data.dot(self.weights) + self.bias

    def sigmoid(self, x, derivative=False):
        if derivative:
            return x * (1 - x)
        return 1 / (1 + math.exp(-x))

    def softmax(self):
        # we could use this for multiple classes instead of multiple networks
        pass

    def crossEntropy(self, real, predicted):
        pass
