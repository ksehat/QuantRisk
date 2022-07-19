import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%

data = pd.read_csv('data.csv',index_col = 0)
data.head()

#%%
train_input_df = data.drop(['target'],axis=1)
train_output_df = data[['target']]
train_input_df.head()
train_output_df.head()
#%%
train_input= train_input_df.to_numpy()
m, n = train_input.shape
s0, s1 = train_input.strides
W=3
train_input = np.lib.stride_tricks.as_strided(train_input, shape=(m - W + 1, W, n), strides=(s0, s0, s1))

print(train_input.shape)
#%%
train_output= train_output_df.to_numpy()
m, n = train_output.shape
s0, s1 = train_output.strides
W=4
train_output = np.lib.stride_tricks.as_strided(train_output, shape=(m - W + 1, W), strides=(s0, s1))

print(train_output.shape)

#%%

train_input[0]

#%%
train_output[0]


