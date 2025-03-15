import pandas as pd
import numpy as np
import joblib
import os
import sys
from pathlib import Path

def load_models(model_path='models/student_performance_model.pkl', scaler_path='models/feature_scaler.pkl'):
    """
    Load the trained model and scaler
    
    Args:
        model_path: Path to the trained model
        scaler_path: Path to the feature scaler
        
    Returns:
        model: Trained RandomForest model
        scaler: Feature scaler
    """
    try:
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        
        try:
            scaler = joblib.load(scaler_path)
            print(f"Scaler loaded from {scaler_path}")
        except:
            print(f"Warning: Scaler not found at {scaler_path}. Proceeding without scaling.")
            scaler = None
            
        return model, scaler
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

def process_input_data(input_file, encoding_reference_file=None):
    """
    Process input data from website CSV and convert it to the same format as training data
    
    Args:
        input_file: Path to input CSV file
        encoding_reference_file: Optional path to a reference file with encoding columns
        
    Returns:
        processed_df: DataFrame with processed features ready for prediction
    """
    try:
        # Load input data
        input_df = pd.read_csv(input_file)
        print(f"Input data loaded, shape: {input_df.shape}")
        
        # Create a new DataFrame for processed data
        processed_data = pd.DataFrame()
        
        # If we have a reference file, use it to determine expected columns
        expected_columns = None
        if encoding_reference_file and os.path.exists(encoding_reference_file):
            reference_df = pd.read_csv(encoding_reference_file)
            print(f"Using reference file for column structure with {len(reference_df.columns)} columns")
            expected_columns = reference_df.columns
        
        # Process Sexe: Convert text to binary (M=0, F=1, Homme=0, Femme=1)
        if 'Sexe' in input_df.columns:
            processed_data['Sexe'] = input_df['Sexe'].replace({
                'M': 0, 'F': 1, 
                'Homme': 0, 'Femme': 1,
                'H': 0, 'h': 0, 'f': 1
            })
        
        # Process language levels
        language_mapping = {
            'Débutant': 1,
            'Intermédiaire': 2, 
            'Intermediaire': 2,
            'Avancé': 3,
            'Avance': 3,
            'Courant': 4
        }
        
        # Process Anglais
        if 'Anglais' in input_df.columns:
            processed_data['Anglais'] = input_df['Anglais'].map(language_mapping)
        
        # Process Francais
        if 'Francais' in input_df.columns:
            processed_data['Francais'] = input_df['Francais'].map(language_mapping)
        
        # Keep numerical values as they are
        numerical_cols = ['Nationale', 'regional', 'General', 'Age']
        for col in numerical_cols:
            if col in input_df.columns:
                processed_data[col] = input_df[col]
        
        # One-hot encode categorical columns
        categorical_cols = {
            'specialite_BAC': 'BAC',
            'ville': 'ville',
            'deteste': 'deteste',
            'preferee': 'preferee',
            'specialite': 'specialite'
        }
        
        for col, prefix in categorical_cols.items():
            if col in input_df.columns:
                # Get one-hot encoding
                dummies = pd.get_dummies(input_df[col], prefix=prefix)
                processed_data = pd.concat([processed_data, dummies], axis=1)
        
        # Process multi-value fields (skills and loisirs)
        multi_fields = ['skills', 'loisirs']
        
        for field in multi_fields:
            if field in input_df.columns:
                # Process each value in the field
                if isinstance(input_df[field].iloc[0], str):
                    # Split by comma if it's a comma-separated string
                    values = set()
                    for val_str in input_df[field]:
                        if isinstance(val_str, str):
                            items = [item.strip() for item in val_str.split(',')]
                            values.update(items)
                    
                    # Create binary columns for each value
                    for value in values:
                        col_name = f"{field}_{value}"
                        processed_data[col_name] = 0
                        
                        # Set 1 for rows that contain this value
                        for idx, val_str in enumerate(input_df[field]):
                            if isinstance(val_str, str) and value in val_str:
                                processed_data.loc[idx, col_name] = 1
        
        # If we have expected columns from reference, align processed data with it
        if expected_columns is not None:
            # Add missing columns with zeros
            for col in expected_columns:
                if col not in processed_data.columns and col not in ['performance', 'satisfation']:
                    processed_data[col] = 0
            
            # Keep only columns that are in expected_columns
            processed_data = processed_data[[col for col in expected_columns if col != 'performance' and col != 'satisfation']]
        
        return processed_data
    
    except Exception as e:
        print(f"Error processing input data: {e}")
        sys.exit(1)

def make_prediction(input_data, model, scaler=None):
    """
    Make predictions using the trained model
    
    Args:
        input_data: Processed DataFrame with features
        model: Trained model
        scaler: Feature scaler (optional)
        
    Returns:
        predictions: DataFrame with predicted values
    """
    try:
        # Copy input data to avoid modifying the original
        X = input_data.copy()
        
        # Apply scaling if scaler is provided
        if scaler is not None:
            # Identify numerical columns that should be scaled
            num_cols = []
            for col in ['Nationale', 'regional', 'General', 'Anglais', 'Francais']:
                if col in X.columns:
                    num_cols.append(col)
            
            if num_cols:
                try:
                    X[num_cols] = scaler.transform(X[num_cols])
                except Exception as e:
                    print(f"Warning: Error applying scaler: {e}. Proceeding with unscaled data.")
        
        # Make prediction
        y_pred = model.predict(X)
        
        # Create a DataFrame with predictions
        try:
            # For multi-target models
            predictions = pd.DataFrame({
                'performance': y_pred[:, 0],
                'satisfation': y_pred[:, 1]
            })
        except IndexError:
            # For single-target model
            predictions = pd.DataFrame({
                'prediction': y_pred
            })
        
        return predictions
    
    except Exception as e:
        print(f"Error making prediction: {e}")
        sys.exit(1)

def save_results(input_df, predictions, output_path):
    """
    Save predictions along with input data
    
    Args:
        input_df: Original input DataFrame
        predictions: Predictions DataFrame
        output_path: Path to save results
    """
    try:
        # Combine input data with predictions
        results = pd.concat([input_df, predictions], axis=1)
        
        # Save to CSV
        results.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")
        
        # Also print predictions
        print("\nPredictions:")
        print(predictions)
        
        return results
    
    except Exception as e:
        print(f"Error saving results: {e}")
        sys.exit(1)

def predict_student_performance(input_file, output_file='prediction_results.csv', 
                               model_path='models/student_performance_model.pkl',
                               scaler_path='models/feature_scaler.pkl',
                               reference_file='processed_student_data.csv'):
    """
    Main function to predict student performance from raw input data
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to save results
        model_path: Path to trained model
        scaler_path: Path to feature scaler
        reference_file: Path to reference file with encoding structure
    """
    print("\n==== Student Performance Prediction ====")
    print(f"Input file: {input_file}")
    
    # Step 1: Load models
    model, scaler = load_models(model_path, scaler_path)
    
    # Step 2: Process input data
    processed_data = process_input_data(input_file, reference_file)
    print(f"Processed data shape: {processed_data.shape}")
    
    # Step 3: Make predictions
    predictions = make_prediction(processed_data, model, scaler)
    print(f"Generated predictions for {len(predictions)} students")
    
    # Step 4: Save results
    input_df = pd.read_csv(input_file)
    results = save_results(input_df, predictions, output_file)
    
    # Format predictions for display
    for index, row in predictions.iterrows():
        try:
            performance = round(float(row['performance']), 1)
            satisfaction = round(float(row['satisfation']), 1)
            
            performance_level = "Low"
            if performance >= 7:
                performance_level = "Excellent"
            elif performance >= 5:
                performance_level = "Good"
            elif performance >= 3:
                performance_level = "Average"
                
            satisfaction_level = "Low"
            if satisfaction >= 4:
                satisfaction_level = "High"
            elif satisfaction >= 2:
                satisfaction_level = "Medium"
                
            print(f"\nStudent prediction summary:")
            print(f"- Performance: {performance}/10 ({performance_level})")
            print(f"- Satisfaction: {satisfaction}/5 ({satisfaction_level})")
            
        except Exception as e:
            print(f"Error formatting prediction: {e}")
    
    print("\nPrediction completed successfully!")

if __name__ == "__main__":
    # If input file is provided as command line argument
    if len(sys.argv) > 1:
        input_file = "interface/Backend/data.csv"
        predict_student_performance(input_file)
    else:
        # Default input file
        input_file = "interface/Backend/data.csv"
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} not found.")
            print("Usage: python predict.py <input_file.csv>")
            sys.exit(1)
        predict_student_performance(input_file)
