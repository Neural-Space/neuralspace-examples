"""
tell:O me:O the:O weather:B-weather__noun report:I-weather__noun for:O half:B-location moon:I-location bay:I-location <=> weather__find
"""
import re
from pathlib import Path


def get_formatted_entity(raw_entity, text):
    res = re.search(re.escape(rf'{raw_entity["text"]}'), text)
    return {
        "entity": raw_entity["entity"],
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


training_dataset = Path("datasets/nlu/en/multilingual_task_oriented/train.txt")

lines = training_dataset.read_text().split("\n")

for line in lines:
    word_slots, intents = line.strip('\r\n').split(' <=> ')
    tokens = []
    tags = []
    for word_slot in word_slots.split(' '):
        tmp = word_slot.split(':')
        word, slot = ':'.join(tmp[:-1]), tmp[-1]
        tokens.append(word)
        tags.append(slot)
    text = " ".join(tokens)
