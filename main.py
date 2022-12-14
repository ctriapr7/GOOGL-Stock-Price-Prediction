 #import libraries
import os

import matplotlib
import numpy as np #making arrays
import pandas as pd #for data management
import matplotlib.pyplot as plt #for data visualization

dataset_train = pd.read_csv("GOOGL_Stock_Price_Train.csv")
dataset_train.head()
#Using Google's stock open price to train the model
training_set= dataset_train.iloc[:, 1:2].values
print(training_set)
print(training_set.shape)

#Normalizing the dataset
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_training_set = scaler.fit_transform(training_set)
print(scaled_training_set)

#Creating data structure with 60 timesteps and 1 output
X_train = []
Y_train = []
for i in range(60, 1258):
    X_train.append(scaled_training_set[i-60:i, 0])
    Y_train.append(scaled_training_set[i, 0])

#set them into numpy arrays
X_train = np.array(X_train)
Y_train = np.array(Y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

print(X_train.shape)
print(Y_train.shape)

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

#initializing the Recurrent Neural Network
regressor = Sequential()

#Adding different layers to LSTM
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units=1))

regressor.compile(optimizer='adam', loss='mean_squared_error')

regressor.fit(X_train, Y_train, epochs=100, batch_size=32)

#visualizing the data
dataset_test = pd.read_csv('GOOGL_Stock_Price_Test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total)-len(dataset_test)-60:].values #getting input of each previous financial days

inputs = inputs.reshape(-1, 1)
inputs = scaler.transform(inputs)
print(inputs)

X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)

plt.plot(real_stock_price, color = 'red', label = 'Actual Google Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()

from sklearn.metrics import accuracy_score
print(accuracy_score(predicted_stock_price, real_stock_price))




