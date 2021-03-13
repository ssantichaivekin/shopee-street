import csv

with open('scl-2021-ds/test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(f'id,POI/street')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            raw_address = row[1]
            comma_stripped = raw_address.split(",")
            words = comma_stripped[0].split()
            #  print(words)
            if len(words) > 1:
                print(f'{line_count-1},/{words[0]} {words[1]}')
            elif len(words) == 1:
                print(f'{line_count-1},/{words[0]}')
            else:
                print(f'{line_count-1},/')
        line_count += 1
