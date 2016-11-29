import sys
import re
import ast


def parse(file_name, dest_file):
    inFile = open(file_name, 'r')
    outFile = open(dest_file, 'w')
    line = inFile.readline()
    genreSet = set()
    while line != "":
        line = re.split(r'\t+', line)
        if len(line) > 5:
            title = line[2]
            if line[3].startswith('{'):
                genres = ast.literal_eval(line[3]).values()
                summary = line[4]
            elif line[4].startswith('{'):
                genres = ast.literal_eval(line[4]).values()
                summary = line[5]
            elif line[5].startswith('{'):
                genres = ast.literal_eval(line[5]).values()
                summary = line[6]
        outFile.write(title + '|')
        string = ""
        for g in genres:
            if '\\' not in g:
                genreSet.add(g)
                string += g + ','
        outFile.write(string[:-1])
        outFile.write('|' + summary)
        line = inFile.readline()
    inFile.close()
    outFile.close()
    return genreSet


def main():
    args = sys.argv
    if len(args) != 3:
        print("Error: wrong number of arguments")
        return 1
    input_file = args[1]
    output_file = args[2]
    genreSet = parse(input_file, output_file)
    print genreSet

if __name__ == "__main__":
    main()
