from abc import ABCMeta, abstractmethod


# abstract base class for defining labels

class ClassificationLabel:
    def __init__(self, label):
        self.label = []
        pass

    def add(self, index, value):
        self.label[index] = value
        pass

    def append(self, value):
        self.label.append(value)

    def get(self, index):
        return self.label[index]


class FeatureVector:
    def __init__(self):
        self.feature_vector = {}
        pass

    def add(self, index, value):
        self.feature_vector[index] = value
        pass

    def get(self, index):
        return self.feature_vector[index]

class Title:
    def __init__(self):
        self.title = ""
        pass

    def add(self, value):
        self.title = value
        pass

    def get(self):
        return self.title


class Instance:
    def __init__(self, feature_vector, label, title):
        self._feature_vector = feature_vector
        self._label = label
        self._title = title


# abstract base class for defining predictors
class Predictor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def train(self, instances): pass

    @abstractmethod
    def predict(self, instance): pass


