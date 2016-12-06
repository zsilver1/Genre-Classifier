import unicodedata
from nltk import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def main():
    args = sys.argv
    if len(args) != 2:
        print("Error: wrong number of arguments")
        return 1
    input_file = args[1]
    createFeatures(input_file)
def createFeatures(filename):
    features = []
    titles = []
    genres = []
    featureWeights = {}
    with open(filename) as reader:
        for line in reader:
            if len(line.strip()) == 0:
                continue
            lineComponents = line.split("|")
            titles.append(lineComponents[0])
            genres.append(lineComponents[1])
            features.append(lineComponents[2])
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    for list in features:
        list = unicode(list, errors='ignore')
        for word in list.split(" "):
          words = lemmatizer.lemmatize(word)
          words = stemmer.stem(words)
          if words not in featureWeights:
                featureWeights[words] = 1
          else:
                featureWeights[words] +=1
    print "here"
    for word in featureWeights:
        print "in"
        print word, featureWeights[word]
        unicodedata.normalize('NFKD', word).encode('ascii', 'ignore')
        for ss in wordnet.synsets(str(word)):
            print(word, ss.name(), ss.lemma_names())
        break
if __name__ == "__main__":
    main()