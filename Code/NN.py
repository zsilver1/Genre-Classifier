from dataTypes import FeatureVector, Predictor, ClassificationLabel


class NeuralNetwork(Predictor):
    def __init__(self, data, genre, numHiddenLayers):
        self.data = data
        self.genre = genre
        self.numHiddenLayers = numHiddenLayers

    def logistic(self, num):
        pass

    def train(self, instances):
        pass

    def predict(self, instance):
        pass
