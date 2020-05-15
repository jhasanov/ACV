import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import pandas as pd
np.random.seed(212)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import metrics
from delta00 import getdelta_e_cie2000
import time


# Importing the dataset
colors = pd.read_csv(r'cielab2000_sample_input-15000.csv')
results = np.squeeze(pd.read_csv(r'cielab2000_sample_output-15000-normalized.csv').values)


colors_Train, colors_Test, results_Train, results_Test = train_test_split(colors,results,test_size=0.2,random_state=121)
eval_colors = pd.read_csv(r'cielab2000_sample_input-1750.csv')
eval_results = pd.read_csv(r'cielab2000_sample_output-1750-normalized.csv')

# Feature Scaling
sc = StandardScaler()

# Initialising the ANN
model = Sequential()
# model.add(Dense(units=10, kernel_initializer='uniform', activation='relu', input_dim=6))
model.add(Dense(units=20, kernel_initializer='uniform', activation='relu', input_dim=6))
# model.add(Dense(units=100, kernel_initializer='uniform', activation='relu', input_dim=50))
# model.add(Dense(units=100, kernel_initializer='uniform', activation='relu', input_dim=100))
model.add(Dense(units=20, kernel_initializer='uniform', activation='relu', input_dim=20))
# model.add(Dense(units=50, kernel_initializer='uniform', activation='relu', input_dim=50))
# model.add(Dense(units=20, kernel_initializer='uniform', activation='relu', input_dim=50))
# model.add(Dense(units=10, kernel_initializer='uniform', activation='relu', input_dim=20))
# model.add(Dense(units=4, kernel_initializer='uniform', activation='relu', input_dim=10))
model.add(Dense(units=1, kernel_initializer='uniform', activation='relu'))
model.compile(optimizer='adam', loss='mean_squared_error', metrics=[metrics.mae,metrics.mse,metrics.MAPE])
history=model.fit(colors_Train, results_Train, validation_data=(eval_colors, eval_results),
               batch_size=1024, epochs=250, shuffle=False)
# model.evaluate(colors_Test, results_Test, verbose=1)
print(model.metrics)

plt.plot(history.history['mean_squared_error'], label='MSE (testing data)')
plt.plot(history.history['val_mean_squared_error'], label='MSE (validation data)')
plt.title('MSE for cielab2000')
plt.ylabel('MSE value')
plt.xlabel('No. epoch')
plt.legend(loc="upper left")
plt.show()
plt.plot(history.history['mean_absolute_error'], label='MSE (testing data)')
plt.plot(history.history['val_mean_absolute_error'], label='MSE (validation data)')
plt.title('MAE for celab2000')
plt.ylabel('MAE value')
plt.xlabel('No. epoch')
plt.legend(loc="upper left")
plt.show()

#predictions

#getting the input as list
inputs=genfromtxt('cielab2000_sample_input-15000.csv',delimiter=',')

start1 = time.time() #pin starting point
#model prediction
prediction=model.predict_on_batch(np.array(inputs))
end1 = time.time() #pin ending point
print(prediction)
print(end1-start1)
# print(end1-start1)
# print(results1)

results2=list()
#color math delta calculation
start2=time.time() #pin starting point
for j in range(0,len(inputs)):
    l1,a1,b1,l2,a2,b2=np.array(inputs[j])
    output=getdelta_e_cie2000(l1,a1,b1,l2,a2,b2)
    rounded_output=np.round(output,5)
    results2.append(rounded_output)
norm=[float(k)/max(results2) for k in results2]

end2=time.time() #pin ending point
 
print(end2-start2)
# print(norm)
