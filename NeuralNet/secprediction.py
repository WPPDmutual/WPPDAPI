
# coding: utf-8

# In[1]:


from __future__ import print_function

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import json
from os import listdir
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import TensorBoard
from time import time
import keras.backend as K
from keras import metrics


# In[2]:


def removeNone(input):
    data = []
    for i in input:
        temp = []
        for g in i:
            if g is None:
                temp.append(0)
            else:
                temp.append(g)
        data.append(temp)
    return data


# In[3]:


train = json.loads(open('train.json', 'r').read())
test = json.loads(open('test.json', 'r').read())
current = json.loads(open('current.json', 'r').read())
tickers = json.loads(open('test.json', 'r').read())['ticker']

trainlength = len(train['growth'])
testlength = len(test['growth'])

x_train = removeNone(train['data'][:trainlength])
x_test = removeNone(test['data'])
currentData = removeNone(current['data'])
y_train = removeNone(np.array(train['growth']).reshape((trainlength, 1)).tolist())
y_test = removeNone(np.array(test['growth']).reshape((testlength, 1)).tolist())


# In[4]:


xscaler = MinMaxScaler()
xscaler.fit(x_train + x_test)
x_train = xscaler.transform(x_train)
x_test = xscaler.transform(x_test)
currentData = xscaler.transform(currentData)

yscaler = MinMaxScaler()
yscaler.fit(y_train + y_test)
y_train = yscaler.transform(y_train)
y_test = yscaler.transform(y_test)


# In[5]:


model = Sequential()

model.add(Dense(units=1024, activation='relu', input_dim=224))
model.add(Dense(units=512, activation='relu'))
model.add(Dense(units=256, activation='relu'))
model.add(Dense(units=128, activation='relu'))
model.add(Dense(units=1))

def mean_err():
    correct = yscaler.inverse_transform(y_test)
    pred = yscaler.inverse_transform(model.predict(x_test))
    averageError = 0;
    
    for i in range(424):
        averageError += abs(correct[i][0]/pred[i][0]-1)
        if i > 0:
            averageError = averageError/2
    return averageError

model.compile(loss='mean_squared_error', optimizer='adam')


# In[6]:


import matplotlib.pyplot as plt
from tqdm import tqdm

batchSize = 32
n_epochs = 100000
error = []

for i in tqdm(range(n_epochs)):
    indices = np.random.choice(y_test.shape[0], batchSize, replace=False)
    x_batch = x_train[indices, :]
    y_batch = y_train[indices, :]
    
    model.train_on_batch(x_batch, y_batch)
    error.append(mean_err())
plt.plot(error[1::n_epochs//100])


# In[9]:


model.save_weights("model.h5")


# In[7]:


import operator

correct = yscaler.inverse_transform(y_test)

# pred = model.predict(x_test)
pred = yscaler.inverse_transform(model.predict(x_test))

averageError = 0;
predictions = {}
corrections = {}

for i in range(424):
    averageError += abs(correct[i][0]/pred[i][0]-1)
    if i > 0:
        averageError = averageError/2
    predictions[tickers[i]] = pred[i][0]
    corrections[tickers[i]] = correct[i][0]

    sortedItems = sorted(predictions.items(), key=operator.itemgetter(1))

average = 0    

for i in sortedItems[-10:]:
    print(i[0])
    print(corrections[i[0]])
    average += corrections[i[0]]

print(average/10)
print(averageError)


# In[8]:


pred = yscaler.inverse_transform(model.predict(currentData))

predictions = {}

for i in range(424):
    predictions[tickers[i]] = pred[i][0]

sortedItems = sorted(predictions.items(), key=operator.itemgetter(1))

average = 0 

for i in sortedItems[-50:]:
    print(i[0])
    print(i[1])
    average += i[1]

print(average/50)

