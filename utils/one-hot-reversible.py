import itertools

from pandas import read_csv
import numpy as np
from sklearn.preprocessing import OneHotEncoder

def reverse_one_hot(X, encoder):
    reversed_data = []
    all_categories = list(itertools.chain(*encoder.categories_))

    for _row_index, feature_index in zip(*X.nonzero()):
        category_value = all_categories[feature_index]
        reversed_data.append(category_value)

    return reversed_data

def run():
    data = read_csv('datasets/taxi.csv')
    data = data.iloc[1:500, :]

    ohc = OneHotEncoder()
    #encoded_data = ohc.fit_transform(data)

    encoded_data = ohc.fit_transform(np.array(data['cat_5']).reshape(-1, 1))
    reverse_one_hot(encoded_data, ohc)

if __name__ == '__main__':
    run()


