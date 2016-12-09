from abc import ABCMeta, abstractmethod


# abstract base class for defining labels

class ClassificationLabel:
    def __init__(self):
        # ASSUMING 10 GENRES
        self.label = [0 for i in xrange(0, 10)]

    def __str__(self):
        return str(self.label)


class FeatureVector:
    def __init__(self):
        self.feature_vector = {}

    def __str__(self):
        return str(self.feature_vector)

    def __repr__(self):
        return str(self.feature_vector)

    def __len__(self):
        return len(self.feature_vector)

    def add(self, index, value):
        self.feature_vector[index] = value

    def get(self, index):
        if index in self.feature_vector:
            return self.feature_vector[index]
        else:
            return 0

    def modify(self, index, addedValue):
        self.feature_vector[index] += addedValue

    def dot(self, other):
        total = 0
        for i in self.feature_vector:
            total += self.get(i) * other.get(i)
        return total


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
