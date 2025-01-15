import pandas as pd
import numpy as np

data = pd.read_csv('Weather Forecasting.csv')
print(data.head(10))

from sklearn import linear_model

X1 = data[['pres', 'clouds', 'wind_spd', 'wind_dir']]
y1 = data[['temp','app_temp']]

model = linear_model.LinearRegression()
model.fit(X1,y1)

prediction = model.predict([[5,6,7,8]])
print(prediction)

from sklearn.metrics import r2_score

y_pred = model.predict(X1)
acc = r2_score(y1,y_pred)
print(acc)


