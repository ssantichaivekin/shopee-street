import pandas as pd

# https://drive.google.com/drive/folders/1qUfjXR1xj5VOKSm_4eg3dbInffs9aKEo

RANDOM_SEED = 42

source_path = "./scl-2021-ds/parsed_train.csv"
augmented_source_paths = [
    "./santi/parsed_train_aug_no_commas.csv",
    "./santi/parsed_train_aug_no_street.csv",
    "./santi/parsed_train_aug_no_poi.csv",
    "./santi/parsed_train_aug_replaced_street.csv",
    "./santi/parsed_train_aug_replaced_poi.csv",
]

source_df = pd.read_csv("./scl-2021-ds/parsed_train.csv")
del source_df['id']
source_df = source_df.dropna()

augmented_dfs = []
for augmented_path in augmented_source_paths:
    augmented_df = pd.read_csv(augmented_path)
    augmented_dfs.append(augmented_df)

aug_all_df = pd.concat([source_df, *augmented_dfs], ignore_index=True)
aug_all_df.sample(frac=1, random_state=RANDOM_SEED)
aug_all_df.to_csv("./santi/parsed_train_aug_all.csv", index=False)