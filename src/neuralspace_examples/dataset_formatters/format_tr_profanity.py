import json
import pandas as pd

train_ds = pd.read_csv("datasets/nlu/tr/profanity/train.csv")
test_ds = pd.read_csv("datasets/nlu/tr/profanity/test.csv")


train_x = []
test_x = []

for row in train_ds.iterrows():
    train_x.append(
        {
            "intent": str(row[1]["subtask_a"]),
            "text": row[1]["tweet"].replace("@USER", "").strip(),
            "type": "train"
        }
    )

for row in test_ds.iterrows():
    test_x.append(
        {
            "intent": str(row[1]["subtask_a"]),
            "text": row[1]["tweet"].replace("@USER", "").strip(),
            "type": "test"
        }
    )

json.dump(train_x, open("../../../datasets/nlu/tr/profanity/train.json", "w"), indent=4, ensure_ascii=False)
json.dump(test_x, open("../../../datasets/nlu/tr/profanity/test.json", "w"), indent=4, ensure_ascii=False)
