import json
import random
# Opening JSON file

f = open('rasa_dataset_training.json',)
 
data = json.load(f)


random.shuffle(data)

train_data = data[:819]
test_data = data[819:]

all_train_data = []
for i in train_data:
    i["type"] = "train"
    all_train_data.append(i)

all_test_data = []
for i in test_data:
    i["type"] = "test"
    all_test_data.append(i)

with open('rasa_dataset_chinese_train.json', 'w', encoding='utf-8') as f:
    json.dump(all_train_data, f, ensure_ascii=False, indent=4)

with open('rasa_dataset_chinese_test.json', 'w', encoding='utf-8') as f:
    json.dump(all_test_data, f, ensure_ascii=False, indent=4)