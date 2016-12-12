import NN
import sys
import random
import argparse
import pickle
import os

GENRE_DICT = {"Fiction": 0, "Speculative fiction": 1, "Science Fiction": 2,
              "Fantasy": 3, "Mystery": 4, "Suspense": 5, "Crime Fiction": 6,
              "Horror": 7, "Romance novel": 8, "Children's literature": 9,
              "Historical novel": 10, "Non-fiction": 11}


def importData(input_file, words_file):
    data = []
    infile = open(input_file, 'r')
    words = open(words_file, 'r')
    wordsList = words.readlines()
    for i, item in enumerate(wordsList):
        wordsList[i] = item.strip()
    wordListLength = len(wordsList)
    line = infile.readline()
    while line != "":
        line = line.split("|")
        vector = [0] * wordListLength
        title = line[0]
        genre = [0] * 12
        if line[1] == "":
            line = infile.readline()
            continue
        genre[GENRE_DICT[line[1]]] = 1
        summary = line[2].split()
        for item in summary:
            item = item.split(":")
            i = wordsList.index(item[0])
            vector[i] = float(item[1])
        data.append((vector, genre, title))
        line = infile.readline()
    infile.close()
    words.close()
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True,
                        help="The data to use for training or testing.")

    parser.add_argument("--words", type=str, required=True,
                        help="Words file used for training.")

    parser.add_argument("--mode", type=str, required=True,
                        choices=["train", "test"],
                        help="Operating mode: train or test.")

    parser.add_argument("--model-file", type=str, required=True,
                        help="The name of the model file to create/load.")

    parser.add_argument("--training-iterations", type=int,
                        help="The number of training iterations.", default=1)

    parser.add_argument("--ratio-training", type=float,
                        help="The ratio of training to testing data.",
                        default=0.9)

    parser.add_argument("--learning-rate", type=float,
                        help="The learning rate of the network.",
                        default=0.5)

    args = parser.parse_args()

    data = importData(args.data, args.words)
    print "Finished Loading Data"

    numInputs = len(data[0][0])
    numExamples = len(data)
    numTraining = int(numExamples * args.ratio_training)
    print "Total number of examples: " + str(numExamples)
    print "Training examples: " + str(numTraining)
    print "Testing examples: " + str(numExamples - numTraining)

    # TRAINING
    if args.mode == "train":
        nn = NN.NeuralNetwork(numInputs, numInputs / 128, numOutputNodes=12,
                              numHiddenLayers=2,
                              learningRate=args.learning_rate)
        for iteration in xrange(args.training_iterations):
            for instance in data[:numTraining]:
                output = nn.forwardPropagate(instance)
                nn.backPropagate(output[0], output[1])
            print "Done iteration " + str(iteration)
        with open(args.model_file, 'w') as f:
            pickle.dump(nn, f)

    # TESTING
    else:
        with open(args.model_file, 'r') as f:
            nn = pickle.load(f)
        total = 0
        correct = 0
        for instance in data[numTraining:]:
            output = nn.forwardPropagate(instance)
            index1 = output[0].index(max(output[0]))
            #index1 = random.randint(0, 3)
            # index1 = random.randint(0, 11)
            index2 = output[1].index(max(output[1]))
            # print "Predicted: " + str(index1) + ", Real: " + str(index2)
            if index1 == index2:
                correct += 1
            total += 1
        print "ACCURACY: " + str(float(correct) / total)
        os.system('say "finished"')


if __name__ == "__main__":
    main()
