# ## Raw Dataset
# ## Train: https://github.com/nghuyong/rasa-nlu-benchmark/blob/master/data/SMP2019/train.md
# ## Test: https://github.com/nghuyong/rasa-nlu-benchmark/blob/master/data/SMP2019/test.md
    
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import markdown
import pynlpir

pynlpir.open()

intent_list = {}
entity_list_all = []
example = markdown.markdown(open("<path to training .md file>").read())
soup = BeautifulSoup(example, 'html.parser')
for header in soup.find_all('h2'):
    intent_list[header.get_text().replace("intent:", "")] = []
    nextNode = header
    while True:
        nextNode = nextNode.nextSibling
        if nextNode is None:
            break
        if isinstance(nextNode, NavigableString):
            print (nextNode.strip())
        if isinstance(nextNode, Tag):
            if nextNode.name == "h2":
                break
            all_Text = nextNode.get_text(strip=False).split("\n")
            all_Text.pop(0)
            all_Text.pop(-1)
            for elem in nextNode.find_all("li"):
                entity_val = []
                entity_start = []
                # print("##", elem)
                fulltext = elem.get_text(strip=False)
                entity_list = []
                for a in elem.find_all('a', href=True): 
                    if a.text:
                        entity_value = a.text
                        entity = a["href"]
                        # print(entity, entity_value)
                        start = fulltext.find(entity_value)
                        end = fulltext.find(entity_value) + len(entity_value)
                        entity_list.append({'entity': entity, 'value': entity_value, 'start':start, 'end':end})
                entity_list_all.append(entity_list)
            intent_list[header.get_text().replace("intent:", "")] = all_Text
            # intent_list[header.get_text().replace("intent:", "")] = entity_list

text = []
intent_t = []
type = []
for key in intent_list:
    for elem in intent_list[key]:
        text.append(elem)
        intent_t.append(key)
        type.append("train")
data = [{'text': tex, 'intent': int_t, 'type':train, 'entities':ent} for tex, int_t, train, ent in zip(text, intent_t, type, entity_list_all)]
# print(data)
import json
with open('train.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)