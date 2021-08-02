from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd

df = pd.read_csv('/Users/prakashramesh/others/neuralspace-examples/datasets/nlu/ur/roman-urudu/train.csv')
X = df['sentence']
y = df['sentiment']

split = StratifiedShuffleSplit(train_size=0.9, test_size=0.1, random_state=30)
for train_index, test_index in split.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]


training = pd.DataFrame({"label": y_train, "text":X_train}, columns=['label', 'text'])

testing = pd.DataFrame(data={"label": y_test, "text": X_test}, columns=['label', 'text'])

training.to_csv('/Users/prakashramesh/others/neuralspace-examples/datasets/nlu/ur/roman-urudu/train.csv', index=False)
testing.to_csv('/Users/prakashramesh/others/neuralspace-examples/datasets/nlu/ur/roman-urudu/test.csv', index=False)
