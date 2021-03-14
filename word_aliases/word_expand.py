import csv
import pprint
from collections import defaultdict

with open('scl-2021-ds/train.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    aliases = {}
    for line_count, row in enumerate(csv_reader):
        if line_count == 0:
            continue
        raw_address = row[1]
        raw_address = raw_address.replace(',', '')
        raw_words = raw_address.split()

        actual_address = row[2].replace('/', ' ')
        actual_address = actual_address.replace(',', ' ')
        actual_address = actual_address.split()

        for word in actual_address:
            if word not in raw_words:
                for abbrev in raw_words:
                    if (abbrev in word) and (abbrev != word) and (len(abbrev) >
                                                                1):
                        if word not in aliases:
                            aliases[word] = {}
                        if abbrev not in aliases[word]:
                            aliases[word][abbrev] = 1
                        else:
                            aliases[word][abbrev] += 1
                if word in aliases:
                    if '_count' not in aliases[word]:
                        aliases[word]['_count'] = 1
                    else:
                        aliases[word]['_count'] += 1

pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(aliases)

aliases_list = list(aliases.items())
print(aliases_list[:10])
aliases_list.sort(key = lambda tup: tup[1]['_count'], reverse=True)
pp.pprint(aliases_list)
