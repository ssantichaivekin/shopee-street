import pandas as pd
from tqdm import tqdm
import random
import ast

# https://drive.google.com/drive/folders/1qUfjXR1xj5VOKSm_4eg3dbInffs9aKEo

POI_TAG = 0
STREET_TAG = 1
OTHER_TAG = 2

def main():
    source_df = pd.read_csv("./scl-2021-ds/parsed_train.csv")
    del source_df['id']
    source_df = source_df.dropna()
    source_df['parsed'] = source_df['parsed'].apply(ast.literal_eval)

    augmented_no_commas_df = df_with_commas_removed(source_df)
    augmented_no_commas_df.to_csv("./santi/parsed_train_aug_no_commas.csv", index=False)

    augmented_no_street_df = df_with_street_names_removed(source_df)
    augmented_no_street_df.to_csv("./santi/parsed_train_aug_no_street.csv", index=False)

    augmented_no_poi_df= df_with_poi_removed(source_df)
    augmented_no_poi_df.to_csv("./santi/parsed_train_aug_no_poi.csv", index=False)

    street_tuples_list = find_tag_tup_list(source_df, STREET_TAG)
    augmented_replaced_street_df = df_with_street_replaced(source_df, street_tuples_list)
    augmented_replaced_street_df.to_csv("./santi/parsed_train_aug_replaced_street.csv", index=False)

    poi_tuples_list = find_tag_tup_list(source_df, POI_TAG)
    augmented_replaced_poi_df = df_with_poi_replaced(source_df, poi_tuples_list)
    augmented_replaced_poi_df.to_csv("./santi/parsed_train_aug_replaced_poi.csv", index=False)

def df_with_commas_removed(source_df):
    data = []
    for _, row in tqdm(source_df.iterrows()):
        if ',' in row['raw_address']:
            raw_address, poi_street, parsed = create_copy_with_commas_removed(row)
            data.append((raw_address, poi_street, parsed))
    augmented_no_commas_df = pd.DataFrame(data, columns=['raw_address', 'POI/street', 'parsed'])
    return augmented_no_commas_df

def create_copy_with_commas_removed(original_row):
    poi_street =  original_row['POI/street']
    raw_address = original_row['raw_address'].replace(',', ' ').replace('  ', ' ')
    parsed = list(filter(lambda tup: tup[0] != ',', original_row['parsed']))
    return raw_address, poi_street, parsed

def df_with_street_names_removed(source_df):
    data = []
    for _, row in tqdm(source_df.iterrows()):
        new_row = create_copy_with_street_names_removed(row)
        if new_row is not None:
            data.append(new_row)
    augmented_no_street_df = pd.DataFrame(data, columns=['raw_address', 'POI/street', 'parsed'])
    return augmented_no_street_df

def create_copy_with_street_names_removed(original_row):
    new_parsed = list(filter(lambda tup: tup[1] != STREET_TAG, original_row['parsed']))
    if not new_parsed or new_parsed == original_row['parsed']:
        return None

    new_raw_address_list, _, _ = zip(*new_parsed)
    new_raw_address = ' '.join(new_raw_address_list)
    new_raw_address = new_raw_address.replace(' ,', ',')
    
    old_poi, _ = original_row['POI/street'].split('/')
    poi_street = old_poi + '/'

    return new_raw_address, poi_street, new_parsed

def df_with_poi_removed(source_df):
    data = []
    for _, row in tqdm(source_df.iterrows()):
        new_row = create_copy_with_poi_removed(row)
        if new_row is not None:
            data.append(new_row)
    augmented_no_poi_df = pd.DataFrame(data, columns=['raw_address', 'POI/street', 'parsed'])
    return augmented_no_poi_df

def create_copy_with_poi_removed(original_row):
    new_parsed = list(filter(lambda tup: tup[1] != POI_TAG, original_row['parsed']))
    if not new_parsed or new_parsed == original_row['parsed']:
        return None

    new_raw_address_list, _, _ = zip(*new_parsed)
    new_raw_address = ' '.join(new_raw_address_list)
    new_raw_address = new_raw_address.replace(' ,', ',')
    
    _, old_street = original_row['POI/street'].split('/')
    poi_street = '/' + old_street

    return new_raw_address, poi_street, new_parsed

def df_with_street_replaced(source_df, street_tup_list):
    data = []
    for _, row in tqdm(source_df.iterrows()):
        if has_street(row):
            for _ in range(5):
                new_row = create_copy_with_street_replaced(row, street_tup_list)
                data.append(new_row)
    augmented_street_replaced_df = pd.DataFrame(data, columns=['raw_address', 'POI/street', 'parsed'])
    return augmented_street_replaced_df

def has_street(row):
    return row['POI/street'].split('/')[1] != ""

def create_copy_with_street_replaced(original_row, street_tup_list):
    old_parsed = original_row['parsed']
    # find the location of old street
    new_parsed = []
    new_street_tup = random.choice(street_tup_list)
    new_street_added = False
    for word, tag, new_word in old_parsed:
        if tag == STREET_TAG:
            if not new_street_added:
                new_parsed.extend(new_street_tup)
                new_street_added = True
            continue
        new_parsed.append((word, tag, new_word))

    new_raw_address_list, _, _ = zip(*new_parsed)
    new_raw_address = ' '.join(new_raw_address_list)
    new_raw_address = new_raw_address.replace(' ,', ',')
    
    new_street = ' '.join([new_word for old_word, tag, new_word in new_street_tup if tag == STREET_TAG])
    new_street = new_street.replace(' ,', ',')
    old_poi, _ = original_row['POI/street'].split('/')
    poi_street = old_poi + '/' + new_street

    return new_raw_address, poi_street, new_parsed

def df_with_poi_replaced(source_df, poi_tup_list):
    data = []
    for _, row in tqdm(source_df.iterrows()):
        if has_poi(row):
            for _ in range(5):
                new_row = create_copy_with_poi_replaced(row, poi_tup_list)
                data.append(new_row)
    augmented_street_replaced_df = pd.DataFrame(data, columns=['raw_address', 'POI/street', 'parsed'])
    return augmented_street_replaced_df

def has_poi(row):
    return row['POI/street'].split('/')[0] != ""

def create_copy_with_poi_replaced(original_row, poi_tup_list):
    old_parsed = original_row['parsed']
    new_parsed = []
    new_poi_tup = random.choice(poi_tup_list)
    new_poi_added = False
    for word, tag, new_word in old_parsed:
        if tag == POI_TAG:
            if not new_poi_added:
                new_parsed.extend(new_poi_tup)
                new_poi_added = True
            continue
        new_parsed.append((word, tag, new_word))

    new_raw_address_list, _, _ = zip(*new_parsed)
    new_raw_address = ' '.join(new_raw_address_list)
    new_raw_address = new_raw_address.replace(' ,', ',')
    
    new_poi = ' '.join([new_word for old_word, tag, new_word in new_poi_tup if tag == POI_TAG])
    new_poi = new_poi.replace(' ,', ',')
    _, old_street = original_row['POI/street'].split('/')
    poi_street = new_poi + '/' + old_street

    return new_raw_address, poi_street, new_parsed

def find_tag_tup_list(source_df, tag):
    """
    return a list of (street name string, [(street name 3-tuple), ...])
    """
    tag_tuples_list = []
    for _, row in source_df.iterrows():
        tag_tuples = list(filter(lambda tup: tup[1] == tag, row['parsed']))
        if tag_tuples:
            tag_tuples_list.append(tag_tuples)
    return tag_tuples_list

if __name__ == '__main__':
    main()
