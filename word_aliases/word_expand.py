import csv
from collections import defaultdict

with open('scl-2021-ds/train.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    aliases = {}
    for row in csv_reader:
        if line_count != 0:
            raw_address = row[1]
            raw_address = raw_address.replace(',', '')
            raw_words = raw_address.split()

            actual_address = row[2].split("/")[1]
            actual_address = actual_address.replace(',', '')
            actual_address = actual_address.split()

            for word in actual_address:
                for abbrev in raw_words:
                    if (abbrev in word) and (abbrev != word) and (len(abbrev) >
                                                                  1):
                        if word not in aliases:
                            aliases[word] = {}
                        if abbrev not in aliases[word]:
                            aliases[word][abbrev] = 1
                        else:
                            aliases[word][abbrev] += 1
        line_count += 1

    print(aliases)

