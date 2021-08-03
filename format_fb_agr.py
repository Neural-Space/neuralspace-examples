import json
import re

import pandas as pd

train_ds = pd.read_csv("datasets/nlu/hi/facebook-post-aggression-identification/agr_hi_train.csv")
test_ds = pd.read_csv("datasets/nlu/hi/facebook-post-aggression-identification/agr_hi_dev.csv")
phrases_ds = pd.read_csv("datasets/nlu/hi/facebook-post-aggression-identification/abusive_phrases.csv")

train_ds.dropna()
test_ds.dropna()
phrases_ds.dropna()

train_x = []
test_x = []
phrases = []


def process_text(text):
    FLAGS = re.MULTILINE | re.DOTALL
    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    # function so code less repetitive
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=FLAGS)

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", " url ")
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


for row in train_ds.iterrows():
    try:
        train_x.append(
            {
                "intent": str(row[1][2]),
                "text": process_text(row[1][1]).strip(),
                "type": "train"
            }
        )
    except Exception as e:
        print(e)
        print(row)
        continue

for row in test_ds.iterrows():
    try:
        test_x.append(
            {
                "intent": str(row[1][2]),
                "text": process_text(row[1][1]).strip(),
                "type": "test"
            }
        )
    except Exception as e:
        print(e)
        print(row)
        continue


for row in phrases_ds.iterrows():
    phrases.append(row[1][0])


json.dump(train_x, open("datasets/nlu/hi/facebook-post-aggression-identification/train.json", "w"), indent=4, ensure_ascii=False)
json.dump(test_x, open("datasets/nlu/hi/facebook-post-aggression-identification/test.json", "w"), indent=4, ensure_ascii=False)
json.dump(phrases, open("datasets/nlu/hi/facebook-post-aggression-identification/abusive_phrases.json", "w"), indent=4, ensure_ascii=False)
