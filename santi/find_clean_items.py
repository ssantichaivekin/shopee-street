"""
Find whether a row is clean.
Sanitize ',' to ' ,' so that comma becomes its own word.
A clean row is a row where both street and poi word list is a sublist of raw address word list.
"""

def is_space_or_end_of_string(string: str, index: int):
    if index < 0 or index >= len(string):
        return True
    if string[index] == ' ':
        return True
    return False

def is_clean_individual(source: str, pattern: str):
    if pattern == '':
        return True
    pattern_start_loc = source.find(pattern)
    if pattern_start_loc == -1:
        return False
    pattern_end_loc = pattern_start_loc + len(pattern)
    if is_space_or_end_of_string(source, pattern_start_loc-1) and is_space_or_end_of_string(source, pattern_end_loc):
        return True
    return False

def is_clean(row):
    sanitized_raw_address = row['sanitized_raw_address']
    poi, street = row['POI/street'].split('/')
    return is_clean_individual(sanitized_raw_address, poi) and is_clean_individual(sanitized_raw_address, street)

def sanitize(row):
    raw_address = row['raw_address']
    sanitized_raw_address = raw_address.replace(',', ' ,')
    return sanitized_raw_address

DATA_PATH = './scl-2021-ds/train_split.csv'
OUT_PATH = './santi/train_split_clean.csv'

import pandas as pd
df = pd.read_csv(DATA_PATH)
df['sanitized_raw_address'] = df.apply(sanitize, axis=1)
df['is_clean'] = df.apply(is_clean, axis=1)
print(f'{df.is_clean.sum()} / {len(df)}')
df.to_csv(OUT_PATH)

    