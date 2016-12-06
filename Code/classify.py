import os
import argparse
import sys
import pickle
from collections import defaultdict

import numpy as np

from predictor import Predictor
from dataTypes import ClassificationLabel, FeatureVector, Instance, Predictor, Title


def load_data(filename):
    instances = []
    with open(filename) as reader:
        for line in reader:
            if len(line.strip()) == 0:
                continue
            # Divide the line into title, features and label.
            # Features are in the form word : count
            split_line = line.split("|")
            title_string = split_line[0]
            title = Title()
            title.add(title_string)
            labels = split_line[1]
            label = ClassificationLabel()
            for lab in labels.split(","):
                label.append(lab)
            feature_vector = FeatureVector()
            for item in split_line[2:]:
                    index = item.split(":")[0]
                    try:
                        value = float(item.split(":")[1])
                    except ValueError:
                        raise ValueError("Unable to convert value " + item.split(":")[1] + " to float.")
                    if value != 0.0:
                        feature_vector.add(index, value)
            instance = Instance(feature_vector, label, title)
            instances.append(instance)
    print instances
    return instances


def get_args():
    parser = argparse.ArgumentParser(
        description="This is the main test harness for your algorithms.")
    parser.add_argument("--data", type=str, required=True, help="The parsed filename")
    parser.add_argument("--algorithm", type=str, help="The name of the algorithm for training.")
    parser.add_argument("--train-percent", type=int, help="Percentage of training data. The rest will automatically be used for testing", default=50)
    parser.add_argument("--iterations", type=int, help="Number of training iterations", default=10)
    parser.add_argument("--learning-rate", type=float, help="Learning rate for the aalgorithm", default=1.0)
    args = parser.parse_args()
    check_args(args)

    return args


def check_args(args):
    if args.algorithm is None:
            raise Exception("--algorithm should be specified in mode \"train\"")
    if not os.path.exists(args.data):
            raise Exception("data file specified by --data does not exist.")


def train(learning, iterations, instances, algorithm):
    prediction = Predictor(defaultdict(float))
    predictions = prediction.train(learning, iterations, instances, algorithm)
    trained = Predictor(predictions)
    return trained


def write_predictions(predictor, instances, predictions_file):
    try:
        with open(predictions_file+"_predict", 'w') as writer:
            for instance in instances:
                label = predictor.predict(instance)
                writer.write(str(label))
                writer.write('\n')
    except IOError:
        raise Exception("Exception while opening/writing file for writing predicted labels: " + predictions_file)


def main():
        args = get_args()
        filename = args.data
        allInstances = load_data(args.data)
        numRows = len(allInstances)
        trainingRows = int((args.train_percent * numRows)/100)
        # Load the training data.
        with open(args.data) as datafile:
            trainInstances = [next(datafile) for x in xrange(trainingRows)]
        # Train the model.
        predictor = train(args.leraning_rate, args.iterations, trainInstances, args.algorithm)
        try:
            mfilename = filename + "_model"
            with open(mfilename, 'wb') as writer:
                pickle.dump(predictor, writer)
        except IOError:
            raise Exception("Exception while writing to the model file.")        
        except pickle.PickleError:
            raise Exception("Exception while dumping pickle.")
        # Load the test data.
        with open(args.data) as datafile:
            testInstances = [next(datafile) for x in xrange(numRows - trainingRows)]

        predictor = None
        # Load the model.
        try:
            with open(mfilename, 'rb') as reader:
                predictor = pickle.load(reader)
        except IOError:
            raise Exception("Exception while reading the model file.")
        except pickle.PickleError:
            raise Exception("Exception while loading pickle.")
        write_predictions(predictor, testInstances, filename)

        # Check the accuracy:
        try:
            with open(filename+"_predict", 'rb') as reader:
                testLabels = pickle.load(reader)
        except IOError:
                raise Exception("Exception while reading the prredictions file.")
        except pickle.PickleError:
            raise Exception("Exception while loading pickle.")
        total = allInstances - trainingRows
        correct = 0
        num = 0
        for instance in testInstances:
            if instance._label == testLabels[num]:
                correct +=1
            num += 1
        print "Accuracy of predictions is :", correct/total, " with ", correct, "labels out os total ", total, "labels"

if __name__ == "__main__":
    main()
