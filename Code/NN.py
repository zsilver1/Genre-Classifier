import math


class NeuralNetwork:
    def __init__(self, data,  numInputNodes, numHiddenNodes, numOutputNodes=12,
                 learningRate=0.5, numHiddenLayers=0):

        # list of (np vectors, label (as tuple))
        self.data = data
        self.numInputNodes = numInputNodes
        self.numHiddenLayers = numHiddenLayers
        self.numOutputNodes = numOutputNodes
        self.learningRate = learningRate

        self.numHiddenNodes = numHiddenNodes

        # self.network[l][j] where l is layer and j is jth node of layer
        self.network = []
        self.populateNetwork()

    def populateNetwork(self):
        for l in xrange(self.numHiddenLayers+2):
            self.network.append([])
        # input nodes
        for i in xrange(self.numInputNodes):
            self.network[0].append(Node(0))
        # hidden layer nodes
        for j in xrange(1, self.numHiddenLayers+1):
            for i in xrange(self.numHiddenNodes):
                n = Node(j)
                n.inputs = self.network[j-1]
                n.weights = [0.0] * len(self.network[j-1])
                self.network[j].append(n)
        # output nodes
        for i in xrange(self.numOutputNodes):
            n = Node(self.numHiddenLayers+1)
            n.inputs = self.network[self.numHiddenLayers]
            n.weights = [0.0] * len(self.network[self.numHiddenLayers])
            self.network[self.numHiddenLayers+1].append(n)

    def setFirstLayerOutputs(self, instance):
        # instance is tuple, see above
        x = instance[0]
        for i, node in enumerate(self.network[0]):
            node.output = x[i]

    def forwardPropagate(self, instance):
        outputs = []
        y = instance[1]
        self.setFirstLayerOutputs(instance)
        for layer in xrange(1, self.numHiddenLayers+1):
            for neuron in self.network[layer]:
                neuron.getOutput()
        for neuron in self.network[self.numHiddenLayers+1]:
            neuron.getOutput()
            outputs.append(neuron.output)
        return outputs, y

    def setLastLayerDeltas(self, predictedLabels, trueLabels):
        for i, node in enumerate(self.network[self.numHiddenLayers+1]):
            node.delta = (node.output * (1 - node.output) *
                          (trueLabels[i] - predictedLabels[i]))

    def updateNeuronParams(self):
        for layer in xrange(1, self.numHiddenLayers+2):
            for node in self.network[layer]:
                node.updateParams(self.learningRate, self.network[layer - 1])

    def backPropagate(self, predictedLabels, trueLabels):
        self.setLastLayerDeltas(predictedLabels, trueLabels)
        for layer in reversed(xrange(1, self.numHiddenLayers+1)):
            for i, node in enumerate(self.network[layer]):
                error = 0
                for prevNode in self.network[layer+1]:
                    error += prevNode.delta * prevNode.weights[i]
                node.getDelta(error)
        self.updateNeuronParams()


class Node:
    def __init__(self, layer):
        self.inputs = []
        self.weights = []
        self.bias = 0
        self.net = 0
        self.output = 0
        self.delta = 0
        self.layer = layer

    def sigmoid(self, x):
        return 1.0 / (1 + math.exp(-1 * x))

    def getOutput(self):
        self.net = 0
        for weight, node in enumerate(self.inputs):
            self.net += self.weights[weight] * node.output
        self.net += self.bias

        self.output = self.sigmoid(self.net)

    def getDelta(self, error):
        self.delta = self.output * (1 - self.output) * error

    def updateParams(self, learningRate, prevLayer):
        self.bias = self.bias * learningRate * self.delta
        for i, node in enumerate(prevLayer):
            self.weights[i] = (self.weights[i] + learningRate *
                               node.output * self.delta)

    def __str__(self):
        return "Node(out=" + str(self.output) + ",lr=" + str(self.layer) + ")"

    def __repr__(self):
        return str(self)
