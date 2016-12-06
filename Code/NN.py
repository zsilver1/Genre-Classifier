from dataTypes import FeatureVector, Predictor, ClassificationLabel
import math


class NeuralNetwork(Predictor):
    def __init__(self, data, genre, numHiddenLayers):
        self.data = data
        self.genre = genre
        self.numHiddenLayers = numHiddenLayers

    def logistic(self, x):
        # we will only use this in the LAST LAYER, because we are doing
        # binary regression
        return 1 / (1 + math.exp(-x))

    def softmax(self):
        # we could use this for multiple classes instead of multiple networks
        pass

    def crossEntropy(self, real, predicted):
        pass

    def train(self, instances):
        pass

    def predict(self, instance):
        pass
