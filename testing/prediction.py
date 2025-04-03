import pandas as pd
import joblib
import numpy as np

cats = ['Réseaux et télécommunication', 'Statistique et informatique décisionnelle', 
        'Génie mécanique et productique', 'Génie électrique', 'Génie des procédés', 
        'Gestion des ressources humaines', 'Technique de gestion commerciale', 
        'Technique de management', 'Gestion logistique et transport', 
        'Génie thermique et énergétique', 'Informatique', 'Génie industriel et maintenance']

def turn_all_zero_but_spe(df, spe):
    """Set all speciality columns to 0 except for the specified one"""
    df_copy = df.copy()
    for cat in cats:
        df_copy[f"specialite_{cat}"] = 0
    df_copy[f"specialite_{spe}"] = 1
    return df_copy

# Load models and data
scaler = joblib.load('models/feature_scaler.pkl')
model = joblib.load('models/student_performance_model.pkl')
data = pd.read_csv("interface/Backend/tr1.csv")
num_cols = ['Nationale', 'regional', 'General', 'Francais', 'Anglais']

# Create a DataFrame with model's expected features
X = pd.DataFrame(columns=model.feature_names_in_)
for col in model.feature_names_in_:
    if col in data.columns:
        X[col] = data[col]
    else:
        X[col] = 0

# Create a results DataFrame to store all predictions
results = []

# Loop through each specialty
for specialty in cats:
    # Apply the specialty
    X_specialty = turn_all_zero_but_spe(X, specialty)
    
    # Scale numerical columns
    X_copy = X_specialty.copy()
    X_copy[num_cols] = scaler.transform(X_copy[num_cols])
    
    # Get prediction
    predictions = model.predict(X_copy)
    
    # Create a row for the results
    result_row = data.copy()
    result_row['specialty'] = specialty
    
    # Add predictions
    if predictions.ndim > 1 and predictions.shape[1] == 2:
        result_row['predicted_performance'] = predictions[:, 0]
        result_row['predicted_satisfaction'] = predictions[:, 1]
        # Calculate combined score (adjust weights as needed)
        result_row['combined_score'] = 0.5 * predictions[:, 0] + 0.5 * predictions[:, 1]*2
    else:
        result_row['prediction'] = predictions
    
    results.append(result_row)

# Combine all results
all_results = pd.concat(results)

# Sort by combined score (or other metric if preferred)
if 'combined_score' in all_results.columns:
    all_results = all_results.sort_values(by='combined_score', ascending=False)

# Save to CSV
all_results.to_csv('predictions.csv', index=False)
print("Predictions for all specialties saved to 'predictions.csv'")

if 'combined_score' in all_results.columns:
    top3 = all_results.drop_duplicates(subset=['specialty']).nlargest(3, 'combined_score')
    print("\nTop 3 recommended specialties:")
    for i, (_, row) in enumerate(top3.iterrows(), 1):
        print(f"{i}. {row['specialty']} - Performance: {row['predicted_performance']:.2f}, Satisfaction: {row['predicted_satisfaction']:.2f}")