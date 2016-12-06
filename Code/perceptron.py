from dataTypes import FeatureVector


class Perceptron:
    def __init__(self, input_data):
        self.weights = FeatureVector()
        self.input_data = input_data
        # add bias to output
        self.bias = 0

    def computeOutput(self):
        return self.input_data.dot(self.weights) + self.bias
