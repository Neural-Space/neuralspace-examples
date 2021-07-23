import json
import re
from pathlib import Path

file = Path("datasets/nlu/en/chatbot_corpus/raw.json")

data = json.loads(file.read_text())

x = data["sentences"]
y = [d["intent"] for d in data["sentences"]]

from sklearn.model_selection import StratifiedShuffleSplit

sss = StratifiedShuffleSplit(n_splits=2, test_size=0.2, random_state=0)

train_x = []
test_x = []


def get_formatted_entity(raw_entity, text):
    res = re.search(f'{raw_entity["text"]}', text)
    return {
        "entity": raw_entity["entity"],
        "value": raw_entity["text"],
        "start": res.start(),
        "end": res.end()
    }

for train_index, test_index in sss.split(x, y):
    for idx in train_index:
        sample = x[idx]
        formatted_example = {
            "text": sample["text"],
            "intent": sample["intent"],
            "type": "train",
            # "entities": [
            #     get_formatted_entity(e, sample["text"])
            #     for e in sample["entities"]
            # ]
        }
        train_x.append(formatted_example)

    for idx in test_index:
        sample = x[idx]
        formatted_example = {
            "text": sample["text"],
            "intent": sample["intent"],
            "type": "test",
            # "entities": [
            #     get_formatted_entity(e, sample["text"])
            #     for e in sample["entities"]
            # ]
        }
        test_x.append(formatted_example)
    break

json.dump(train_x, open("datasets/nlu/en/chatbot_corpus/train_intent.json", "w"), indent=4, ensure_ascii=False)
json.dump(test_x, open("datasets/nlu/en/chatbot_corpus/test_intent.json", "w"), indent=4, ensure_ascii=False)