import json

import pandas as pd
from fuzzysearch import find_near_matches
from tqdm import tqdm

# df = pd.read_csv("datasets/nlu/multilingual/hinglish/hasoc_combined/hindi_dataset.tsv", sep="\t")

with open("datasets/nlu/multilingual/hinglish/facebook-post-aggression-identification/train.json", "r") as trjf:
    train_data = json.load(trjf)

with open("datasets/nlu/multilingual/hinglish/facebook-post-aggression-identification/test.json", "r") as tsjf:
    test_data = json.load(tsjf)

with open("datasets/nlu/multilingual/hinglish/hate_lexicon/hinglish_lookup.json", "r") as hf:
    hatephrases = json.load(hf)["examples"]


train_dataset = []
test_dataset = []


for r in tqdm(train_data):
    text = r["text"]
    label = r["intent"]
    entities = []
    all_matches = []
    if label == "Overtly Aggressive" or label == "Covertly Aggressive":
        for phrase in hatephrases:
            matches = find_near_matches(
                phrase, text, max_l_dist=0
            )
            all_matches += matches
    for m in all_matches:
        entities.append(
            {
                "entity": "hate_phrase",
                "value": text[m.start: m.end],
                "start": m.start,
                "end": m.end,
                "entityType": "lookup"
            }
        )
    train_dataset.append({
        "text": text,
        "intent": label,
        "type": "train",
        "entities": entities
    })

for r in tqdm(test_data):
    text = r["text"]
    label = r["intent"]
    entities = []
    all_matches = []
    if label == "Overtly Aggressive" or label == "Covertly Aggressive":
        for phrase in hatephrases:
            matches = find_near_matches(
                phrase, text, max_l_dist=0
            )
            all_matches += matches
    for m in all_matches:
        entities.append(
            {
                "entity": "hate_phrase",
                "value": text[m.start: m.end],
                "start": m.start,
                "end": m.end,
                "entityType": "lookup"
            }
        )
    test_dataset.append({
        "text": text,
        "intent": label,
        "type": "test",
        "entities": entities
    })

with open("datasets/nlu/multilingual/hinglish/facebook-post-aggression-identification/formatted_train.json", "w") as jf:
    json.dump(train_dataset, jf, ensure_ascii=False, indent=4)

with open("datasets/nlu/multilingual/hinglish/facebook-post-aggression-identification/formatted_test.json", "w") as jf:
    json.dump(test_dataset, jf, ensure_ascii=False, indent=4)
