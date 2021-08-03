import json
import re
from pathlib import Path

DATASET = "en/multilingual_task_oriented"


def get_formatted_entity(raw_entity, text):
    res = re.search(re.escape(rf'{raw_entity["text"]}'), text)
    return {
        "entity": raw_entity["entity"].split("__")[-1],
        "value": raw_entity["text"],
        "start": res.start(),
        "end": res.end()
    }


def convert_bilou_to_entities(
        tokens, tags, text
):
    entities = []
    entity_buffer = []
    for i, (token, tag) in enumerate(zip(tokens, tags)):
        if tag.startswith("B"):
            entity_buffer = [(token, tag)]
        elif tag.startswith("I") and entity_buffer != []:
            entity_buffer.append((token, tag))
        elif tag.startswith("O") and entity_buffer != []:
            # entity_buffer.append((token, tag))
            # if the first and the last token in the buffer don't have the same label then reject
            if entity_buffer[0][1][2:] != entity_buffer[-1][1][2:]:
                entity_buffer = []
                continue
            entity_text = " ".join(
                [token for (token, tag) in entity_buffer]
            )
            e = {
                "entity": entity_buffer[-1][1][2:],
                "text": entity_text
            }
            entities.append(
                get_formatted_entity(e, text)
            )
            entity_buffer = []
        elif entity_buffer:
            entity_buffer.append((token, tag))
        else:
            continue
    return entities


training_dataset = Path(f"datasets/nlu/{DATASET}/train.txt")
valid_dataset = Path(f"datasets/nlu/{DATASET}/valid.txt")
test_dataset = Path(f"datasets/nlu/{DATASET}/test.txt")




train_x = []
valid_x = []
test_x = []

lines = training_dataset.read_text().split("\n")
for line in list(set(lines)):
    word_slots, intents = line.strip('\r\n').split(' <=> ')
    tokens = []
    tags = []
    for word_slot in word_slots.split(' '):
        tmp = word_slot.split(':')
        word, slot = ':'.join(tmp[:-1]), tmp[-1]
        tokens.append(word)
        tags.append(slot)
    text = " ".join(tokens)
    train_x.append(
        {
            "intent": intents.split("__")[-1],
            "text": text,
            "type": "train",
            "entities": convert_bilou_to_entities(tokens, tags, text)
        }
    )


lines = valid_dataset.read_text().split("\n")
for line in list(set(lines)):
    word_slots, intents = line.strip('\r\n').split(' <=> ')
    tokens = []
    tags = []
    for word_slot in word_slots.split(' '):
        tmp = word_slot.split(':')
        word, slot = ':'.join(tmp[:-1]), tmp[-1]
        tokens.append(word)
        tags.append(slot)
    text = " ".join(tokens)
    valid_x.append(
        {
            "intent": intents.split("__")[-1],
            "text": text,
            "type": "test",
            "entities": convert_bilou_to_entities(tokens, tags, text)
        }
    )

lines = test_dataset.read_text().split("\n")
for line in list(set(lines)):
    word_slots, intents = line.strip('\r\n').split(' <=> ')
    tokens = []
    tags = []
    for word_slot in word_slots.split(' '):
        tmp = word_slot.split(':')
        word, slot = ':'.join(tmp[:-1]), tmp[-1]
        tokens.append(word)
        tags.append(slot)
    text = " ".join(tokens)
    test_x.append(
        {
            "intent": intents.split("__")[-1],
            "text": text,
            "type": "test",
            "entities": convert_bilou_to_entities(tokens, tags, text)
        }
    )

json.dump(train_x, open(f"datasets/nlu/{DATASET}/train.json", "w"), indent=4, ensure_ascii=False)
json.dump(valid_x, open(f"datasets/nlu/{DATASET}/valid.json", "w"), indent=4, ensure_ascii=False)
json.dump(test_x, open(f"datasets/nlu/{DATASET}/test.json", "w"), indent=4, ensure_ascii=False)
