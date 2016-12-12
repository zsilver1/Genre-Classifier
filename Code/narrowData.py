import sys


def main():
    args = sys.argv
    if len(args) != 4:
        print("Error: wrong number of arguments")
        return 1
    input_file = args[1]
    output_file = args[2]
    words_file = args[3]
    with open(input_file, 'r') as f:
        with open(output_file, 'w') as outf:
            line = f.readline()
            while line != "":
                line = line.split("|")
                summary = line[2]
                summary = summary.split()
                for w in summary:
                    if w not in words:
                        summary.remove(w)
                summary = ' '.join(summary)
                outf.write(line[0]+"|"+line[1]+"|"+summary+"\n")
                line = f.readline()


def findNumUnique(input_file):
    words = {}
    with open(input_file, 'r') as f:
        line = f.readline()
        while line != "":
            line = line.split("|")
            summary = line[2]
            for w in summary.split():
                if w in words:
                    words[w] += 1
                else:
                    words[w] = 1
            line = f.readline()
    # words = words.items()
    # total = sum(pair[1] for pair in words)
    # return sorted(words, key=lambda tup: tup[1], reverse=True)[:10000], total
    return sorted(words.keys(), key=words.get, reverse=True)[:10000]


if __name__ == "__main__":
    main()
