import pandas as pd
import joblib
import numpy as np

scaler = joblib.load('our_scaler.pkl')
model = joblib.load('student_performance_model.pkl')

data = pd.read_csv('outpu3t.csv')

num_cols = ['Nationale', 'Regional', 'Generale', 'Francais', 'Anglais']

X = pd.DataFrame(columns=model.feature_names_in_)

for col in model.feature_names_in_:
    if col in data.columns:
        X[col] = data[col]
    else:
        X[col] = 0

X_copy = X.copy()
X_copy[num_cols] = scaler.transform(X[num_cols])

predictions = model.predict(X_copy)

if predictions.ndim > 1 and predictions.shape[1] == 2:
    data['predicted_performance'] = predictions[:, 0]
    data['predicted_satisfaction'] = predictions[:, 1]
else:
    data['prediction'] = predictions

data.to_csv('predictions.csv', index=False)
print("Predictions saved to 'predictions.csv'")