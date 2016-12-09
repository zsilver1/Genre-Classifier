from operator import itemgetter

from nltk import PorterStemmer, WordNetLemmatizer, defaultdict
from nltk.compat import iteritems
from nltk.corpus import wordnet
import sys


reload(sys)
sys.setdefaultencoding('utf8')


def main():
    args = sys.argv
    if len(args) != 3:
        print("Error: wrong number of arguments")
        return 1
    input_file = args[1]
#    genre_list = args[3]
    output_file = args[2]
    createFeatures(input_file, output_file)#, genre_list)


def check_synonym(word, word2):
    """checks to see if word and word2 are synonyms"""
    l_syns = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            l_syns.append(l.name())
    print l_syns
    if word2 in l_syns:
        return True
    return False


def createFeatures(infile, outfile):#, genrelist):
    features = {}
    titles = []
    genres = {}
    featureWeights = {}
    genreList = {}
    with open(infile) as reader:
        for line in reader:
            if len(line.strip()) == 0:
                continue
            lineComponents = line.split("|")
            titles.append(lineComponents[0])
            temp = []
            for genre in lineComponents[1].split(","):
                temp.append(genre)
            genres[lineComponents[0]] = temp
            summary = lineComponents[2]
            wordList = []
            for word in summary.rstrip("\n").split(" "):
                wordList.append(word)
            features[lineComponents[0]] = wordList
    reader.close()
    '''
        with open(genrelist) as reader:
            for line in reader:
                if len(line.strip()) == 0:
                    continue
                lineComponents = line.split(":")
                genreList[lineComponents[0]] = lineComponents[1]
        reader.close()'''

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    tf = {}
    idf = defaultdict(int)
    tf_idf = {}
    numdocs = len(titles)
    for list in features:
        temptf = {}
        tempList = []
        wordlist = []
        length = len(features[list])
        for word in features[list]:
            words = unicode(word, errors='ignore')
            words = lemmatizer.lemmatize(words)
            words = stemmer.stem(words)
            tempList.append(word)
            if words not in wordlist:
                wordlist.append(words)
                idf[word] += 1
            if word not in temptf:
                temptf[word] = 1
            else:
                temptf[word] += 1
            if word not in featureWeights:
                featureWeights[word] = 1
            else:
                featureWeights[word] += 1
        features[list] = tempList
        for word in temptf:
            temptf[word] = float(temptf[word])/float(length)
        tf[list] = temptf
    deleteList = []
    for key, value in sorted(idf.iteritems(), key=lambda (k, v): (v, k), reverse= True):
        #print key, value
        if value < 100:
            deleteList.append(key)
        idf[key] = numdocs/idf[key]
    for list in features:
        tmp = defaultdict(float)
        for word in features[list]:
            tmp[word] = tf[list][word] * idf[word]
        tf_idf[list] = tmp
    writer = open(outfile, "w")
    for title in titles:
            genre = ""
            GENRE_LIST = ["Fiction", "Speculative fiction", "Science Fiction",
                          "Fantasy", "Children's literature", "Mystery",
                          "Suspense", "Crime Fiction", "Historical novel",
                          "Horror", "Romance novel", "Non-fiction"]
            for g in genres[title]:
                if g in GENRE_LIST:
                    genre = g
                    break
            temp = []
            tempVector = ""
            for feature in features[title]:
                if feature not in temp:
                 temp.append(feature)
                 if feature not in deleteList:
                  tempVector += feature + ":" + str(tf_idf[title][feature]) + " "
            writer.write(title+"|"+genre+"|"+tempVector+"\n")
    writer.close()
if __name__ == "__main__":
    main()
