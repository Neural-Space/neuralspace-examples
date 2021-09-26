import json
import re

import pandas as pd
from fuzzysearch import find_near_matches
from tqdm import tqdm

FLAGS = re.MULTILINE | re.DOTALL


def clean_text(text):
    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    # function so code less repetitive
    def re_sub(pattern, repl, flag=None):
        set_flags = FLAGS if flag is None else flag
        return re.sub(pattern, repl, text, flags=set_flags)

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", " url ")
    text = re_sub(r"^(?!.*\bRT\b)(?:.+\s)?@\w+", "@user")
    # text = re_sub(r"#(\S+)", r"\1") # replace #name with name
    text = re_sub(r"(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))", " em_positive ")  # Smile -- :), : ), :-), (:, ( :, (-:, :')
    text = re_sub(r"(:\s?D|:-D|x-?D|X-?D)", " em_positive ")  # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    text = re_sub(r"(<3|:\*)", " em_positive ")  # Love -- <3, :*
    text = re_sub(r"(;-?\)|;-?D|\(-?;)", " em_positive ")  # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    text = re_sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', " em_negative ")  # Sad -- :-(, : (, :(, ):, )-:
    text = re_sub(r'(:,\(|:\'\(|:"\()', " em_negative ")  # Cry -- :,(, :'(, :"(
    text = re_sub(r"(.)\1+", r"\1\1")  # remove funnnnny --> funny
    text = re_sub(r"(-|\')", "")  # remove &
    # text = re_sub(r"/"," / ")
    text = re_sub(r"@[0-9]+-", " number ")
    text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), " em_positive ")
    text = re_sub(r"{}{}p+".format(eyes, nose), " em_positive ")
    text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), " em_negative ")
    text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), " em_neutralface ")
    # text = re_sub(r"<3"," heart ")
    # text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", " ")
    # text = re_sub(r"#\S+", hashtag)
    # text = re_sub(r"([!?.]){2,}", r" \1 ")
    # text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 ")
    # text = re_sub(r"([A-Z]){2,}", allcaps)
    # text = re_sub(r'([\w!.,?();*\[\]":\”\“])([!.,?();*\[\]":\”\“])', r'\1 \2')
    # text = re_sub(r'([!.,?();*:\[\]":\”\“])([\w!.,?();*\[\]":\”\“])', r'\1 \2')
    # text = re_sub(r'(.)(<)', r'\1 \2')
    # text = re_sub(r'(>)(.)', r'\1 \2')
    # text = re_sub(r'[\'\`\’\‘]', r'')
    # text = re_sub(r'\\n', r' ')
    text = re_sub(r'-', r' ')
    # text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", " url ")
    text = re_sub(r"([pls?s]){2,}", r"\1")
    text = re_sub(r"([plz?z]){2,}", r"\1")
    text = re_sub(r'\\n', r' ')
    # text = re_sub(r"<3","love")
    text = re_sub(r" sx ", " sex ")
    text = re_sub(r" u ", " you ")
    text = re_sub(r" r ", " are ")
    text = re_sub(r" y ", " why ")
    text = re_sub(r" Y ", " WHY ")
    text = re_sub(r"Y ", " WHY ")
    text = re_sub(r" hv ", " have ")
    text = re_sub(r" c ", " see ")
    text = re_sub(r" bcz ", " because ")
    text = re_sub(r" coz ", " because ")
    text = re_sub(r" v ", " we ")
    text = re_sub(r" ppl ", " people ")
    text = re_sub(r" pepl ", " people ")
    text = re_sub(r" r b i ", " rbi ")
    text = re_sub(r" R B I ", " RBI ")
    text = re_sub(r" R b i ", " rbi ")
    text = re_sub(r" R ", " ARE ")
    text = re_sub(r" hav ", " have ")
    text = re_sub(r"R ", " ARE ")
    text = re_sub(r" U ", " you ")
    text = re_sub(r" 👎 ", " OAG ")
    text = re_sub(r"U ", " you ")
    text = re_sub(r" pls ", " please ")
    text = re_sub(r"Pls ", "Please ")
    text = re_sub(r"plz ", "please ")
    text = re_sub(r"Plz ", "Please ")
    text = re_sub(r"PLZ ", "Please ")
    text = re_sub(r"Pls", "Please ")
    text = re_sub(r"plz", "please ")
    text = re_sub(r"Plz", "Please ")
    text = re_sub(r"PLZ", "Please ")
    text = re_sub(r" thankz ", " thanks ")
    text = re_sub(r" thnx ", " thanks ")
    text = re_sub(r"fuck\w+ ", " fuck ")
    text = re_sub(r"f\*\* ", " fuck ")
    text = re_sub(r"\*\*\*k ", " fuck ")
    text = re_sub(r"F\*\* ", " fuck ")
    text = re_sub(r"mo\*\*\*\*\* ", " fucker ")
    text = re_sub(r"b\*\*\*\* ", " blody ")
    text = re_sub(r" mc ", " fucker ")
    text = re_sub(r" MC ", " fucker ")
    text = re_sub(r" wtf ", " fuck ")
    text = re_sub(r" ch\*\*\*ya ", " fucker ")
    text = re_sub(r" ch\*\*Tya ", " fucker ")
    text = re_sub(r" ch\*\*Tia ", " fucker ")
    text = re_sub(r" C\*\*\*yas ", " fucker ")
    text = re_sub(r"l\*\*\*\* ", "shit ")
    text = re_sub(r" A\*\*\*\*\*\*S", " ASSHOLES")
    text = re_sub(r" di\*\*\*\*s", " cker")
    text = re_sub(r" nd ", " and ")
    text = re_sub(r"Nd ", "and ")
    text = re_sub(r"([!?!]){2,}", r"! ")
    text = re_sub(r"([.?.]){2,}", r". ")
    text = re_sub(r"([*?*]){2,}", r"* ")
    text = re_sub(r"([,?,]){2,}", r", ")
    text = re_sub(r"([!]){2,}", r"! ")
    text = re_sub(r"([.]){2,}", r". ")
    text = re_sub(r"([*]){2,}", r"* ")
    text = re_sub(r"([,]){2,}", r", ")
    text = re_sub(r"\n\r", " ")
    text = re_sub(r"(ind[vs]pak)", " india versus pakistan ")
    text = re_sub(r"(pak[vs]ind)", " pakistan versus india ")
    text = re_sub(r"(indvsuae)", " india versus United Arab Emirates ")
    text = re_sub(r"[sS]hut[Dd]own[jnuJNU]", " shut down jnu ")
    # text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", " number ")
    return text


df = pd.read_csv("datasets/nlu/multilingual/hinglish/hasoc_combined/hindi_dataset.tsv", sep="\t")

with open("datasets/nlu/multilingual/hinglish/hate_lexicon/hinglish_lookup.json", "r") as hf:
    hatephrases = json.load(hf)["examples"]


dataset = []
for r in tqdm(df.iterrows()):
    raw_label = r[1]["task_1"]
    if raw_label == "NOT" or raw_label == "HOF":
        label = "Non Hate-Offensive" if raw_label == "NOT" else "Hate and Offensive"
        text = clean_text(r[1]["text"])
        entities = []
        all_matches = []
        if label == "Hate and Offensive":
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
        dataset.append({
            "text": text,
            "intent": label,
            "type": "test",
            "entities": entities
        })

with open("datasets/nlu/multilingual/hinglish/hasoc_combined/hasoc2021_hi_test.json", "w") as jf:
    json.dump(dataset, jf, ensure_ascii=False, indent=4)