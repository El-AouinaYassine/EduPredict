import pandas as pd 
import joblib
from sklearn.preprocessing import StandardScaler

students_model = joblib.load('../script/student_performance_model.pkl')
students_scaler = joblib.load('../script/scaler.pkl')

new_data = pd.read_csv('new_future_data.csv')

