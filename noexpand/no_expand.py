import csv
import pprint
from collections import defaultdict

with open('scl-2021-ds/train.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first_line = False
    no_expand = defaultdict(int)
    for row in csv_reader:
        if first_line == True:
            first_line = False
            continue
        raw_address = row[1]
        raw_address = raw_address.replace(',', '')
        raw_words = raw_address.split()

        actual_address = row[2].split("/")[1]
        actual_address = actual_address.replace(',', '')
        actual_address = actual_address.split()

        for address_word in actual_address:
            for word in raw_words:
                if word == address_word:
                    no_expand[word] += 1

pp = pprint.PrettyPrinter(indent=4)
no_expand_list = list(no_expand.items())
no_expand_list.sort(key = lambda tup: tup[1], reverse=True)
pp.pprint(no_expand_list)
