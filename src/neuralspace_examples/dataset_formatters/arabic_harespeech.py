import json
import re

import pandas as pd
from fuzzysearch import find_near_matches
from tqdm import tqdm

df_hsab = pd.read_csv("datasets/nlu/ar/arabic_hatespeech/L-HSAB.tsv", sep="\t")
df_ar = pd.read_csv("datasets/nlu/ar/arabic_hatespeech/ar_dataset.csv", sep=",")


