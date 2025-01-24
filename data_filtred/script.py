import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_csv(
    'DATASET.csv',
    delimiter=',',
    quotechar='"',
    skipinitialspace=True,  # Skip spaces after delimiters
    engine='python',       
    )

features = data.drop(columns=['performance', 'satisfaction'])
targets = data[['performance', 'satisfaction']]

# Define numeric and categorical columns
numeric_columns = ['Age', 'Nationale', 'examen_Régional', 'Note_Générale', 'Français', 'Anglais']
categorical_columns = ['Ville', 'Sexe', 'spécialité_BAC', 'Loisirs', 'préférée', 'détestée', 'Skills', 'Spécialité']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_columns),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
    ]
)

# Apply preprocessing
X = preprocessor.fit_transform(features)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, targets, test_size=0.2, random_state=42)

# Train model
model = MultiOutputRegressor(RandomForestRegressor(random_state=42))
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
for i, target in enumerate(targets.columns):
    mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])
    r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])
    print(f"Evaluation for {target}:")
    print(f"  - Mean Squared Error: {mse}")
    print(f"  - R² Score: {r2}\n")
