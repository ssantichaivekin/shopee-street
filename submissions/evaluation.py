import pandas as pd
import numpy as np

SUBMISSION_FILE_NAME = "submission.csv"
ANSWERS_FILE_NAME = "train.csv"


def evaluate(submission, label):
    submission_df = pd.read_csv(submission)
    label_df = pd.read_csv(label)
    label_df.columns = ['id', 'raw_address', 'correct_POI/street']
    result = pd.concat([submission_df, label_df.loc[:, ['correct_POI/street']]], axis=1)
    result['correct'] = np.where(
        result['POI/street'] == result['correct_POI/street'], 1, np.where(
            result['POI/street'] != result['correct_POI/street'], 0, -1))
    score = result['correct'].sum()
    accuracy = (score/len(result)) * 100
    print(accuracy)
    return accuracy


evaluate(SUBMISSION_FILE_NAME, ANSWERS_FILE_NAME)
