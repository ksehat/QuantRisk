import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure
from sklearn.metrics import confusion_matrix as cm
from xgboost import XGBClassifier as xgb
import seaborn as sns

df = pd.read_csv('classified_load_by_target.csv')
print(df.isna().sum())
# df.dropna(inplace=True)

# df['load-class'] = np.where(df['load'].values, )
df['error'] = df['target'] - df['dap']

column_name = 'target'
mean_value = df[column_name].mean()
std_value = df[column_name].std()
cut_bins = [-np.inf, -std_value + mean_value, std_value + mean_value, np.inf]
cut_labels = [i for i in range(len(cut_bins) - 1)]
df['class'] = pd.cut(df[column_name], bins=cut_bins, labels=cut_labels)

# df.to_csv(f'classified_load_by_{column_name}.csv')

# plt.plot(df['dap'],c=df['class'])
# plt.plot(df['class'])
# plt.show()

plt.figure(figsize=(12,8))
sns.scatterplot(data=df[-140:], x=df[-140:].index, y='dap', hue='class2')
plt.show()

plt.figure(figsize=(12,8))
sns.scatterplot(data=df[-140:], x=df[-140:].index, y='target', hue='class2')
plt.show()

plt.figure(figsize=(12,8))
sns.scatterplot(data=df[-140:], x=df[-140:].index, y='error', hue='class2')
plt.show()
