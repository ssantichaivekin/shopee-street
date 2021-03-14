"""
Create pickle training set for deepparse
Output Format:
[ (raw_address: str, ['LabelName', ...]) ]
[
    ('3 jersey road un 28 nsw 2064', ['Street', 'Street', 'PointOfInterest', 'Other', 'Other', 'Other', 'Other']),
    ...
]
"""

DATA_PATH = './santi/train_split_clean.csv'
CSV_OUT_PATH = './santi/deepprase_clean_only_train_split.csv'
PICKLE_OUT_PATH = './santi/deepprase_clean_only_train_split.p'

def match_percent(source_list, pattern_list):
    assert(len(source_list) == len(pattern_list))
    count_match = 0
    for source_word, pattern_word in zip(source_list, pattern_list):
        if source_word == pattern_word:
            count_match += 1
    return count_match / len(source_list)

def find_matching_range(source_list, pattern_list):
    """
    Note: we define matching as match or almost match,
    that is, matching at least 2/3 of the sequence
    """
    for i in range(0, len(source_list) - len(pattern_list)):
        source_sublist = source_list[i:i+len(pattern_list)]
        if match_percent(source_sublist, pattern_list) >= 2/3:
            return i, i+len(pattern_list)
    return None

def tag(address, poi, street):
    """
    return list of labels
    """
    address_word_list = address.split()
    poi_word_list = poi.split()
    street_word_list = street.split()

    labels = ['Other'] * len(address_word_list)

    if poi_word_list:
        matching_poi_range = find_matching_range(address_word_list, poi_word_list)
        if matching_poi_range is not None:
            poi_start, poi_end = matching_poi_range
            for i in range(poi_start, poi_end):
                labels[i] = 'PointOfInterest'
    
    if street_word_list:
        matching_street_range = find_matching_range(address_word_list, street_word_list)
        if matching_street_range is not None:
            street_start, street_end = matching_street_range
            for i in range(street_start, street_end):
                labels[i] = 'Street'
    
    return labels

def tag_row(row):
    if row['is_clean']:
        sanitized_raw_address = row['sanitized_raw_address']
        poi, street = row['POI/street'].split('/')
        labels = tag(sanitized_raw_address, poi, street)
        return labels
    return None

import pandas as pd
import pickle
from itertools import islice

df = pd.read_csv(DATA_PATH)
df['labels'] = df.apply(tag_row, axis=1)
df.to_csv(CSV_OUT_PATH)

pickle_data = []
for i, row in islice(df.iterrows(), 1, None):
    if row['labels']:
        sanitized_raw_address = row['sanitized_raw_address']
        labels = row['labels']
        pickle_row = (sanitized_raw_address, labels)
        pickle_data.append(pickle_row)


with open(PICKLE_OUT_PATH, "wb") as outfile:
    pickle.dump(pickle_data, outfile, pickle.HIGHEST_PROTOCOL)




