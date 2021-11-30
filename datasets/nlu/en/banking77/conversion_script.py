import json

text = []
with open ("<Add path to seq file>", "r") as f:
    lines = f.readlines()
    for line in lines:
        text.append(line.replace("\n", ""))

intent = []
with open ("<Add path to label file>", "r") as f:
    lines = f.readlines()
    for line in lines:
        intent.append(line.replace("\n", ""))
data = []

for i in range(len(text)):
    dic = {}
    dic["text"] = text[i]
    dic["intent"] = intent[i]
    dic["type"] = "train"
    data.append(dic)

with open('banking77_train.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
