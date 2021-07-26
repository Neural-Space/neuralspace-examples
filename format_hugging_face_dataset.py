import os

import pandas as pd
import json

LANGUAGE = input("Enter the Language associated with the project: ")
PATH_TO_DATA = input("enter the name of the data: ")

main_json = []


def create_path(PATH_TO_DATA,LANGUAGE):
    data_in = "./datasets/nlu"
    path_to_language = os.path.join(data_in, LANGUAGE)
    PATH_TO_DATA = os.path.join(path_to_language, PATH_TO_DATA)
    dir = os.listdir(PATH_TO_DATA)
    print("There are: ", dir)
    return PATH_TO_DATA, dir
def create_json(dir, PATH_TO_DATA, limit=3000):
    for data in dir:
        present_path = os.path.join(PATH_TO_DATA, data)
        df = pd.read_csv(present_path)
        columns = df.columns
        print(columns)
        if len(columns) > 2:
            raise Exception("There are more than two columns")
        else:
            labels = df[columns[0]]
            sentences = df[columns[1]]
            count = 0
            for label, sentence in zip(labels, sentences):
                count+=1
                if count > limit:
                    break
                unit_example_dict = {}
                unit_example_dict["text"] = sentence
                unit_example_dict["intent"] = str(label)
                unit_example_dict["type"] = "test" if "validation" in data[:4] else data[:-4]
                main_json.append(unit_example_dict)
        with open(os.path.join(PATH_TO_DATA, f"{data[:-4]}.json"), 'w') as js:
            json.dump(main_json, js, indent=4, ensure_ascii=False)


path, dir = create_path(PATH_TO_DATA, LANGUAGE)
json = create_json(dir, path)