from sys import argv, exit
import csv
import re


def main():

    # ensure the correct usage
    if (len(argv) != 3):
        exit("Usage: python dna.py data.csv sequence.txt")

    # put csv, txt files into variables
    csvFile = argv[1]
    txtFile = argv[2]

    # read title from csv file into variable
    dictSTR = []
    with open(csvFile) as c:
        reader = csv.DictReader(c)
        for row in reader:
            dictSTR.append(row)

    # copy the first row from list -> {'name': 'Alice', 'AGATC': '2', 'AATG': '8', 'TATC': '3'}
    temp = dictSTR[0]

    # read str dna code into list -> read only the keys -> name, AGATC, AATG, TATC
    strTitle = []
    for key in temp.keys():
        strTitle.append(key)

    # delete first position from list str, cause there have a 'name'
    strTitle.pop(0)

    # read txtFile into a string
    with open(txtFile) as t:
        sequence = t.readline()

    # assign to dictionary the pairs key (strCode) and value (count)
    # how many strCode have in the sequence string
    # i.e.: {'AGATC': 4, 'AATG': 1, 'TATC': 5}
    result = {}
    for strCode in strTitle:
        count = countSTRSequence(sequence, strCode)
        if (strCode not in result.keys()):
            result[strCode] = count
        else:
            result[strCode] = 0

    matches = 0
    name = ""
    lenResult = len(result)

    # check for each row, if each key is equals to dictSTR -> row[key] == result[key] -> have to convert to string cause the row is string
    # if is equals increment matches to one. Each interation on row assign 0 to matches
    # if the value of matches is equals to length of result, store the name in variable
    for row in dictSTR:
        matches = 0
        for key in result:
            if row[key] == str(result[key]):
                matches += 1
                if matches == lenResult:
                    name = row['name']
                    break

    # if the name is empty, nobody matches
    if (name == ""):
        print("No match")
    else:
        print(name)


def countSTRSequence(sequence, strCode):
    searchRe = re.compile('(?:' + strCode + ')+')
    return max((len(seq) for seq in searchRe.findall(sequence)), default=0) // len(strCode)


if __name__ == "__main__":
    main()