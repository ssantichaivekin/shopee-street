import csv

with open('scl-2021-ds/test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(f'id,POI/street')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            print(f'{line_count-1},/')
        line_count += 1
