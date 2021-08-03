import json
import re
from pathlib import Path

file = Path("datasets/nlu/en/ask_ubuntu/raw.json")

data = json.loads(file.read_text())

x = data["sentences"]
y = [d["intent"] for d in data["sentences"]]

train_x = []
test_x = []


def get_formatted_entity(raw_entity, text):
    res = re.search(re.escape(rf'{raw_entity["text"]}'), text)
    return {
        "entity": raw_entity["entity"],
        "value": raw_entity["text"],
        "start": res.start(),
        "end": res.end()
    }


for sample in data["sentences"]:
    formatted_example = {
        "text": sample["text"],
        "intent": sample["intent"],
        "entities": [
            get_formatted_entity(e, sample["text"])
            for e in sample["entities"]
        ]
    }
    if sample["training"]:
        formatted_example["type"] = "train"
        train_x.append(formatted_example)
    else:
        formatted_example["type"] = "test"
        test_x.append(formatted_example)


json.dump(train_x, open("../../../datasets/nlu/en/ask_ubuntu/train.json", "w"), indent=4, ensure_ascii=False)
json.dump(test_x, open("../../../datasets/nlu/en/ask_ubuntu/test.json", "w"), indent=4, ensure_ascii=False)