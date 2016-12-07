import unicodedata
from nltk import PorterStemmer, WordNetLemmatizer, defaultdict
from nltk.corpus import wordnet
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def main():
    args = sys.argv
    if len(args) != 4:
        print("Error: wrong number of arguments")
        return 1
    input_file = args[1]
    genre_list = args[3]
    output_file = args[2]
    createFeatures(input_file, output_file, genre_list)

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

def createFeatures(infile, outfile, genrelist):
    features = {}
    titles = []
    genres = {}
    featureWeights = {}
    genreList = {}
    with open(genrelist) as reader:
        for line in reader:
            if len(line.strip()) == 0:
                continue
            lineComponents = line.split(":")
            genreList[lineComponents[0]] = lineComponents[1]
    reader.close()
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
          word = unicode(word, errors='ignore')
          word = lemmatizer.lemmatize(word)
          word = stemmer.stem(word)
          tempList.append(word)
          if word not in wordlist:
              wordlist.append(word)
              idf[word] += 1
          if word not in temptf:
                temptf[word] = 1
          else:
              temptf[word] +=1
          if word not in featureWeights:
                featureWeights[word] = 1
          else:
                featureWeights[word] +=1
        features[list] = tempList
        for word in temptf:
            temptf[word] = float(temptf[word])/float(length)
        tf[list] = temptf
    for word in idf:
        idf[word] = numdocs/idf[word]
    for list in features:
        tmp = defaultdict(float)
        for word in features[list]:
            tmp[word] = tf[list][word] * idf[word]
        tf_idf[list] = tmp
    #Need to fix synonym weights.
    #for word1 in idf:
     #   for word2 in idf:
      #      if check_synonym(word1,word2):
       #         for title in titles:
        #            if word1 in features[title] & word2 in features[title]:
         #               if tf_idf[title][word1]>tf_idf[title][word2]:
          #                  tf_idf[title][word2] = tf_idf[title][word1]
        #             else:
         #                   tf_idf[title][word1] = tf_idf[title][word2]
    writer =  open(outfile, "w")
    for title in titles:
            genresVector = ""
            for genre in genres[title]:
                try:
                    if (genre in genreList) & (genreList[genre] > 100):
                        genresVector += genre + ","
                except:
                    continue
            genresVector = genresVector[:-1]
            tempVector = ""
            for feature in features[title]:
                tempVector += feature +":"+ str(tf_idf[title][feature]) +" "
            writer.write(title+"|"+genresVector+"|"+tempVector+"\n")
    writer.close()
if __name__ == "__main__":
    main()