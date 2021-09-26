import json
import re

import pandas as pd
from fuzzysearch import find_near_matches
from tqdm import tqdm


with open("datasets/nlu/multilingual/hinglish/hasoc_combined/hasoc2019_hi_train.json", "r") as trjf:
    train_data_2019 = json.load(trjf)

with open("datasets/nlu/multilingual/hinglish/hasoc_combined/hasoc2021_hi_test.json", "r") as tsjf:
    test_data_2021 = json.load(tsjf)


with open("datasets/nlu/multilingual/hinglish/hasoc_combined/hasoc2021_hi_train.json", "r") as tsjf:
    train_data_2021 = json.load(tsjf)


train_data_combined = []
test_data = []

for r in tqdm(train_data_2019 + train_data_2021):
    if r["intent"] == "Non Hate-Offensive":
        r["intent"] = "Non-aggressive"
    elif r["intent"] == "Hate and Offensive":
        r["intent"] = "Overtly Aggressive"
    else:
        continue
    train_data_combined.append(r)

for r in tqdm(test_data_2021):
    if r["intent"] == "Non Hate-Offensive":
        r["intent"] = "Non-aggressive"
    elif r["intent"] == "Hate and Offensive":
        r["intent"] = "Overtly Aggressive"
    else:
        continue
    test_data.append(r)

with open("datasets/nlu/multilingual/hinglish/facebook-post-aggression-identification/hasoc_train.json", "w") as jf:
    json.dump(train_data_combined, jf, ensure_ascii=False, indent=4)


with open("datasets/nlu/multilingual/hinglish/facebook-post-aggression-identification/hasoc_test.json", "w") as jf:
    json.dump(test_data, jf, ensure_ascii=False, indent=4)
