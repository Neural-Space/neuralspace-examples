from datasets import load_dataset
import json

dataset = load_dataset("urdu_fake_news", split="train")
dataset = dataset[:638]
all_train = []
for i, line in enumerate(dataset["news"]):
    dict_train = {}
    # print(line)
    dict_train["text"] = line
    if dataset["label"][i] == 0:
        dict_train["intent"] = "REAL"
    else:
        dict_train["intent"] = "FAKE"
    dict_train["type"] = "train"
    all_train.append(dict_train)

with open('urdu_train.json', 'w') as f:
    json.dump(all_train, f, ensure_ascii=False, indent=4)

