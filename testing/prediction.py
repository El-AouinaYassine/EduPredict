import pandas as pd
import joblib
import numpy as np
# models/feature_scaler.pkl
scaler = joblib.load('models/feature_scaler.pkl')
model = joblib.load('models/student_performance_model.pkl')

# data/synthetic/synthetic_student_data.csv
data = pd.read_csv("interface/Backend/tr1.csv")
num_cols = ['Nationale', 'regional', 'General', 'Francais', 'Anglais']

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