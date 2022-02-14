import pandas as pd

df = pd.read_csv("<path to training marathi csv file", header=None, names=["intent", "text"])
intent_list = df["intent"]
text_list = df["text"]

all_train = []
for i, line in enumerate(text_list):
    dict_train = {}
    dict_train["text"] = line
    dict_train["intent"] = intent_list[i]
    dict_train["type"] = "train"
    all_train.append(dict_train)

import json
with open('marathi_train.json', 'w', encoding='utf-8') as f:
    json.dump(all_train, f, ensure_ascii=False, indent=4)

