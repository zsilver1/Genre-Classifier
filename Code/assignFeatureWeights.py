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
    features = {}
    titles = []
    genres = {}
    featureWeights = {}
    with open(filename) as reader:
        for line in reader:
            if len(line.strip()) == 0:
                continue
            lineComponents = line.split("|")
            titles.append(lineComponents[0])
            genres[lineComponents[0]]=lineComponents[1]
            summary = lineComponents[2]
            wordList = []
            for word in summary.rstrip("\n").split(" "):
                wordList.append(word)
            features[lineComponents[0]] = wordList
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    for list in features:
        tempList = []
        for word in features[list]:
          word = unicode(word, errors='ignore')
          word = lemmatizer.lemmatize(word)
          word = stemmer.stem(word)
          tempList.append(word)
          if word not in featureWeights:
                featureWeights[word] = 1
          else:
                featureWeights[word] +=1
        features[list] = tempList
    #Need to fix synonym weights.
    '''
    print "here"
    for word in featureWeights:
        print "in"
        print word, featureWeights[word]
        unicodedata.normalize('NFKD', word).encode('ascii', 'ignore')
        for ss in wordnet.synsets(str(word)):
            print(word, ss.name(), ss.lemma_names())
    '''
    writer =  open(filename+"feature", "w")
    for title in titles:
            tempVector = ""
            for feature in features[title]:
                tempVector += feature +":"+ str(featureWeights[feature])
            writer.write(title+"|"+genres[title]+"|"+tempVector)

if __name__ == "__main__":
    main()