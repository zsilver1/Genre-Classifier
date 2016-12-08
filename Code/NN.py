from dataTypes import FeatureVector, ClassificationLabel
import math


class NeuralNetwork:
    def __init__(self, data, numOutputNodes=10, numHiddenLayers=0):

        # list of (FeatureVector, ClassificationLabel)
        self.data = data
        self.numExamples = len(self.data)
        self.numHiddenLayers = numHiddenLayers
        self.numOutputNodes = numOutputNodes
        self.numHiddenNodes = int(self.numExamples / 2)
        # list of w[l][i] where l is layer, i is output node
        # (returns FeatureVector)
        self.weights = []
        self.populateWeights()
        # list of d[l][i] where l is layer, i is ith node in layer
        self.deltas = []
        self.populateDeltas()
        # this is the delta from which all other deltas are calculated
        self.finalDelta = 0.0

    # def populateWeights(self):
    #     # by default, we will calculate the number of nodes in the hidden layer
    #     # as the length of the input nodes divided by 2
    #     for l in xrange(self.numHiddenLayers+1):
    #         self.weights.append([])
    #     if self.numHiddenLayers == 0:
    #         for i in xrange(self.numExamples):
    #             self.weights[0].append([0.0 for y in
    #                                     xrange(self.numOutputNodes)])
    #     elif self.numHiddenLayers == 1:
    #         for i in xrange(self.numExamples):
    #             self.weights[0].append([0.0 for y in
    #                                     xrange(self.numHiddenNodes)])
    #         for i in xrange(self.numHiddenNodes):
    #             self.weights[1].append([0.0 for y in
    #                                     xrange(self.numOutputNodes)])
    #     else:
    #         for i in xrange(self.numExamples):
    #             self.weights[0].append([0.0 for y in
    #                                     xrange(self.numHiddenNodes)])
    #         for i in xrange(self.numHiddenNodes):
    #             self.weights[1].append([0.0 for y in
    #                                     xrange(self.numHiddenNodes)])
    #         for i in xrange(self.numHiddenNodes):
    #             self.weights[2].append([0.0 for y in
    #                                     xrange(self.numOutputNodes)])

    def populateWeights(self):
        if self.numHiddenLayers == 0:
            self.weights.append([FeatureVector() for i in
                                 xrange(self.numOutputNodes)])
        elif self.numHiddenLayers == 1:
            self.weights.append([FeatureVector() for i in
                                 xrange(self.numHiddenNodes)])
            self.weights.append([FeatureVector() for i in
                                 xrange(self.numOutputNodes)])
        else:
            self.weights.append([FeatureVector() for i in
                                 xrange(self.numHiddenNodes)])
            self.weights.append([FeatureVector() for i in
                                 xrange(self.numHiddenNodes)])
            self.weights.append([FeatureVector() for i in
                                 xrange(self.numOutputNodes)])

    def populateDeltas(self):
        for l in xrange(self.numHiddenLayers):
            self.deltas.append([0.0 for i in xrange(self.numHiddenNodes)])

    def sigmoid(self, x, derivative=False):
        if derivative:
            return x * (1 - x)
        return 1 / (1 + math.exp(-x))

    def finalActivation(self, x):
        # CHANGE THIS MAYBE
        return self.sigmoid(x)

    def costDeriv(self, real, calculated):
        # this is a quadratic cost function
        return (calculated - real) * (1 - real)

    def forwardPropagate(self, instance):
        # instance is tuple, see above
        x = instance[0]
        print x.dataDict
        for layer in xrange(self.numHiddenLayers):
            l = FeatureVector()
            for node in xrange(self.numHiddenNodes):
                a = self.sigmoid(self.weights[layer][node].dot(x))
                l.add(node, a)
            # output becomes new input
            x = l
        prediction = []
        for i in xrange(self.numOutputNodes):
            w = self.weights[self.numHiddenLayers][i]
            prediction.append(self.finalActivation(x.dot(w)))
        return prediction
