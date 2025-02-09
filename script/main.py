import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib 

def getInpute(ville , sexe , bac_spe , nat , reg , gen , fr ,ang ,hobbies , skills , prefered , deteste ,target_spec):
    
    return 0

df = pd.read_csv('./script/data/final.csv') 


# features w targets
X = df.drop(['performance', 'satisfaction'], axis=1)
y = df[['performance', 'satisfaction']]

# 9ssm data l trainin w 20% ltesting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# scalliw les donnes fl meme intervale numerique
scaler = StandardScaler()
num_cols = ['Nationale', 'Regional', 'Generale', 'Francais', 'Anglais']
X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])

model = RandomForestRegressor(
    n_estimators=200, # swb 200 decision tree
    max_depth=5, # 10 layers fdepth
    random_state=42,
    n_jobs=-1  # ga3 lcores
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(y_pred)
print("true values")
print(y_test["performance"])

# Evaluate performance
def evaluate_model(y_true, y_pred):
    metrics = {}
    for i, col in enumerate(y.columns):
        mae = mean_absolute_error(y_true.iloc[:, i], y_pred[:, i])
        mse = mean_squared_error(y_true.iloc[:, i], y_pred[:, i])
        r2 = r2_score(y_true.iloc[:, i], y_pred[:, i])
        
        metrics[col] = {
            'MAE': round(mae, 2),
            'MSE': round(mse, 2),
            'R_2': round(r2, 2)
        }
    return metrics

results = evaluate_model(y_test, y_pred)
print("Performance Metrics:")
for result_item in results.items():
    print(f"\n{result_item}:")


# Save the model 
joblib.dump(scaler, 'our_scaler.pkl')
joblib.dump(model, 'student_performance_model.pkl')
