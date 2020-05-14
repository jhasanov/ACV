import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
np.random.seed(212)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import metrics
# Importing the dataset
colors = pd.read_csv(r'celab2000_sample_input-10k.csv')
results = np.squeeze(pd.read_csv(r'celab2000_sample_output-10k.csv').values)


colors_Train, colors_Test, results_Train, results_Test = train_test_split(colors,
                                                                          results,
                                                                          test_size=0.2,
                                                                          random_state=121)
eval_colors = pd.read_csv(r'celab2000_sample_input-1k.csv')
eval_results = pd.read_csv(r'celab2000_sample_output-1k.csv')

# Feature Scaling
sc = StandardScaler()

# Initialising the ANN
classifier = Sequential()
classifier.add(Dense(units=16, kernel_initializer='uniform', activation='relu', input_dim=6))
# classifier.add(Dense(units=50, kernel_initializer='uniform', activation='relu', input_dim=10))
# classifier.add(Dense(units=100, kernel_initializer='uniform', activation='relu', input_dim=6))
# classifier.add(Dense(units=50, kernel_initializer='uniform', activation='relu', input_dim=6))
# classifier.add(Dense(units=50, kernel_initializer='uniform', activation='relu', input_dim=50))
# classifier.add(Dense(units=20, kernel_initializer='uniform', activation='relu', input_dim=50))
# classifier.add(Dense(units=10, kernel_initializer='uniform', activation='relu', input_dim=50))
# classifier.add(Dense(units=10, kernel_initializer='uniform', activation='relu', input_dim=10))
# classifier.add(Dense(units=4, kernel_initializer='uniform', activation='relu', input_dim=10))
classifier.add(Dense(units=1, kernel_initializer='uniform', activation='relu'))
classifier.compile(optimizer='adam', loss='mean_squared_error', metrics=[metrics.mae])
classifier.fit(colors_Train, results_Train, validation_data=(eval_colors, eval_results),
               batch_size=1024, epochs=800, shuffle=False)
classifier.evaluate(colors_Test, results_Test, verbose=1)
print(classifier.metrics)