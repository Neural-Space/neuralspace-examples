import pandas as pd

df = pd.read_csv(r'/Users/prakashramesh/others/dataset_for_text_classification/dataset/telugu_news/train.csv', encoding='UTF-8')

print(df['body'])