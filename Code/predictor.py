from collections import defaultdict

from dataTypes import Predictor,ClassificationLabel
class Predictor(Predictor):
    def __init__(self,weight):
        self.weight = weight
    def train(self, iterations, instances, algorithm):
        if algorithm == "perceptron":
            print "perceptron"
        else:
            print "Invalid option. Did you mean averaged_perceptron?"
            exit()
        return self.weight

    def predict(self, instance):
        print "find predictions"