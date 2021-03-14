import csv
import pprint
from collections import defaultdict

with open('../scl-2021-ds/train.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first_line = False
    exact_address = {}
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

        for word in raw_words:
            if word not in exact_address:
                exact_address[word] = True
            if word not in actual_address:
                exact_address[word] = False

for k,v in exact_address.items():
    if v == True:
        print(k)
