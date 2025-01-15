# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# **Data Preprocessing**

# Load the dataset
filename = 'Weather Forecasting.csv'  # Replace with your actual CSV file path
df = pd.read_csv(filename)
print(df.head(10))

# Map weather descriptions to numerical values
d = {
    'Few clouds': 0, 
    'Scattered clouds': 1, 
    'Clear Sky': 2, 
    'Overcast clouds': 3, 
    'Light shower rain': 4, 
    'Broken clouds': 5, 
    'Thunderstorm with rain': 6
}
df['description'] = df['description'].map(d)

df = df.drop(['city'], axis=1)

# Check for missing values
missing_mask = df.isnull()
plt.figure(figsize=(8, 6))
sns.heatmap(missing_mask, cmap='viridis', cbar=False, linewidths=0.5, linecolor='red')
plt.title('Heatmap of Missing Values in Weather Forecast')
plt.xlabel('Features')
plt.ylabel('Observations')
plt.show()

# Handle outliers
dataset_dropped_1 = df.drop(['description'], axis=1)
lower_quantile = dataset_dropped_1.quantile(0.01)
upper_quantile = dataset_dropped_1.quantile(0.99)
median_values = dataset_dropped_1.median()

def replace_outliers_with_median(column):
    return np.where(
        (column < lower_quantile[column.name]) | 
        (column > upper_quantile[column.name]), 
        median_values[column.name], 
        column
    )

dataset_dropped_1 = dataset_dropped_1.apply(replace_outliers_with_median)
df.update(dataset_dropped_1)

# **Data Visualization**
# (Your data visualization code goes here)

# **Multiple Regression Model**
from sklearn import linear_model
from sklearn.metrics import r2_score

X1 = df[['app_temp', 'pres', 'clouds', 'wind_spd', 'wind_dir', 'description']]
y1 = df['temp']

regr1 = linear_model.LinearRegression()
regr1.fit(X1, y1)

# Predictions
y_pred1 = regr1.predict(X1)
acc1 = r2_score(y1, y_pred1)
print("Accuracy Score:", acc1)

# Save the model performance
predicted_temps_1 = []
future_features1 = np.array([
    [105.0, 1002.0, 60, 10.0, 250, 1],  # Day 1
    [106.5, 1003.0, 62, 11.0, 255, 1],  # Day 2
    [107.0, 1004.0, 65, 12.0, 260, 1],  # Day 3
    [108.5, 1005.0, 64, 9.5, 250, 1],   # Day 4
    [109.0, 1006.0, 66, 11.5, 265, 1],  # Day 5
    [110.0, 1007.0, 67, 12.5, 270, 1],  # Day 6
    [111.0, 1008.0, 68, 13.5, 275, 1]   # Day 7
])

predicted_temps_12 = regr1.predict(future_features1)
predicted_temps_1.append(predicted_temps_12)

# **Multivariate Regression Model**
X2 = df[['clouds', 'pres', 'wind_dir', 'wind_spd', 'description']]
y2 = df[['temp', 'app_temp']]

regr2 = linear_model.LinearRegression()
regr2.fit(X2, y2)

acc2 = []
for i, target_name in enumerate(y2.columns):
    print(f"Performance for {target_name}:")
    print("Accuracy Score:", r2_score(y2[target_name], regr2.predict(X2)[:, i]))
    acc2.append(r2_score(y2[target_name], regr2.predict(X2)[:, i]))

# Predictions for next 7 days
predicted_temps_2 = []
future_features2 = np.array([
    [60, 1002.0, 240, 11.0, 1],  # Day 1
    [62, 1003.0, 245, 12.0, 1],  # Day 2
    [65, 1004.0, 250, 12.5, 1],  # Day 3
    [64, 1005.0, 255, 11.5, 1],  # Day 4
    [66, 1006.0, 260, 13.0, 1],  # Day 5
    [68, 1007.0, 265, 13.5, 1],  # Day 6
    [70, 1008.0, 270, 14.0, 1]   # Day 7
])

predicted_temps_22 = regr2.predict(future_features2)
predicted_temps_2.append(predicted_temps_22)

# **Random Forest Model**
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

X3 = df[['clouds', 'pres', 'wind_dir', 'wind_spd', 'description']]
y3 = df[['temp', 'app_temp']]

forest = RandomForestRegressor(n_estimators=100, random_state=42)
multi_target_forest = MultiOutputRegressor(forest)
multi_target_forest.fit(X3, y3)

y_pred3 = multi_target_forest.predict(X3)

acc3 = []
for i, target_name in enumerate(y3.columns):
    print(f"Performance for {target_name}:")
    print("Accuracy Score:", r2_score(y3[target_name], y_pred3[:, i]))
    acc3.append(r2_score(y3[target_name], y_pred3[:, i]))

predicted_temps_3 = []
future_features3 = np.array([
    [55, 1002.3, 240, 12.1, 2],  # Day 1
    [60, 1003.0, 250, 13.5, 2],  # Day 2
    [65, 1004.1, 260, 14.2, 2],  # Day 3
    [70, 1005.2, 270, 15.0, 2],  # Day 4
    [75, 1006.0, 280, 15.8, 2],  # Day 5
    [80, 1007.5, 290, 16.6, 2],  # Day 6
    [85, 1008.0, 300, 17.4, 2]   # Day 7
])

predicted_temps_RF = multi_target_forest.predict(future_features3)
predicted_temps_3.append(predicted_temps_RF)

# Save accuracies and predictions to pickle files
with open('model_1.pkl', 'wb') as f:
    pickle.dump({'accuracy': acc1, 'predictions': predicted_temps_1}, f)

with open('model_2.pkl', 'wb') as f:
    pickle.dump({'accuracy': acc2, 'predictions': predicted_temps_2}, f)

with open('model_3.pkl', 'wb') as f:
    pickle.dump({'accuracy': acc3, 'predictions': predicted_temps_3}, f)

print("Models and predictions have been saved.")
