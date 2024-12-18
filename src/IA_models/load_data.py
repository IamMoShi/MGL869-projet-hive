import os
import pandas as pd



def load_data(directory: str):
    data_dict = {}
    liste = ['CCViolDensityLine', 'CCViolDensityCode', 'RatioCommentToCode']

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path)
            for elm in liste:
                data[elm] = data[elm].replace(',', '.').astype(float)
            data_dict[filename] = data

    return data_dict
