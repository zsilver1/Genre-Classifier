from dataTypes import FeatureVector, Predictor, ClassificationLabel


class NeuralNetwork:
    def __init__(self, data, genre, numHiddenNodes, learningRate):
        self.data = data
        self.genre = genre
        self.numHiddenNodes = numHiddenNodes

    def forwardPropagate(self):
        pass

    def backPropaagate(self):
        pass

    def train(self, instances):
        pass

    def predict(self, instance):
        pass
