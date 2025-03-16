import pandas as pd
import numpy as np

def preprocess_data(input_file, output_file=None):
    """
    Preprocess the student dataset by applying one-hot encoding to categorical variables
    and specific transformations as required.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str, optional): Path to save the processed data. If None, returns the DataFrame
        
    Returns:
        pandas.DataFrame: The processed DataFrame if output_file is None
    """
    # Load the data
    df = pd.read_csv(input_file)
    
    # Create a new DataFrame to store the processed data
    processed_data = pd.DataFrame()
    
    # Process Sexe: F=1, M=0
    processed_data['Sexe'] = df['Sexe'].map({'F': 1, 'M': 0})
    
    # Process Anglais and Francais: Convert language levels to numerical values
    language_mapping = {
        'Débutant': 1,
        'Intermédiaire': 2,
        'Avancé': 3,
        'Courant': 4,
        'Avance': 4  # Handling both spellings as mentioned in your requirements
    }
    
    processed_data['Anglais'] = df['Anglais'].map(language_mapping)
    processed_data['Francais'] = df['Francais'].map(language_mapping)
    
    # Keep numerical values as they are
    numerical_cols = ['Nationale', 'regional', 'General', 'satisfation', 'performance']
    for col in numerical_cols:
        processed_data[col] = df[col]
    
    # One-hot encode specialite_BAC
    bac_dummies = pd.get_dummies(df['specialite_BAC'], prefix='BAC')
    processed_data = pd.concat([processed_data, bac_dummies], axis=1)
    
    # One-hot encode ville
    ville_dummies = pd.get_dummies(df['ville'], prefix='ville')
    processed_data = pd.concat([processed_data, ville_dummies], axis=1)
    
    # One-hot encode deteste and preferee
    deteste_dummies = pd.get_dummies(df['deteste'], prefix='deteste')
    preferee_dummies = pd.get_dummies(df['preferee'], prefix='preferee')
    processed_data = pd.concat([processed_data, deteste_dummies, preferee_dummies], axis=1)
    
    # One-hot encode specialite
    specialite_dummies = pd.get_dummies(df['specialite'], prefix='specialite')
    processed_data = pd.concat([processed_data, specialite_dummies], axis=1)
    
    # Process skills (one-hot encoding for each skill)
    # First, get all unique skills
    all_skills = set()
    for skills_str in df['skills']:
        if isinstance(skills_str, str):  # Check if it's a string
            skills_list = [skill.strip() for skill in skills_str.split(',')]
            all_skills.update(skills_list)
    
    # Create columns for each skill
    for skill in all_skills:
        skill_name = skill.strip()
        processed_data[f'skills_{skill_name}'] = 0
    
    # Fill the skill columns
    for idx, skills_str in enumerate(df['skills']):
        if isinstance(skills_str, str):  # Check if it's a string
            skills_list = [skill.strip() for skill in skills_str.split(',')]
            for skill in skills_list:
                processed_data.at[idx, f'skills_{skill}'] = 1
    
    # Process loisirs (one-hot encoding for each loisir)
    # First, get all unique loisirs
    all_loisirs = set()
    for loisirs_str in df['loisirs']:
        if isinstance(loisirs_str, str):  # Check if it's a string
            loisirs_list = [loisir.strip() for loisir in loisirs_str.split(',')]
            all_loisirs.update(loisirs_list)
    
    # Create columns for each loisir
    for loisir in all_loisirs:
        loisir_name = loisir.strip()
        processed_data[f'loisirs_{loisir_name}'] = 0
    
    # Fill the loisir columns
    for idx, loisirs_str in enumerate(df['loisirs']):
        if isinstance(loisirs_str, str):  # Check if it's a string
            loisirs_list = [loisir.strip() for loisir in loisirs_str.split(',')]
            for loisir in loisirs_list:
                processed_data.at[idx, f'loisirs_{loisir}'] = 1
    
    # Save to file if specified
    if output_file:
        processed_data = processed_data.replace({'TRUE': 1, 'FALSE': 0, 'True': 1, 'False': 0, True: 1, False: 0})
        processed_data.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
        print(f"Shape of processed data: {processed_data.shape}")
        print(f"Total number of features: {processed_data.shape[1]}")
    
    return processed_data

# Example usage
if __name__ == "__main__":
    # input_file = "synthetic_student_data.csv"
    # output_file = "processed_student_data.csv"
    
    input_file = "interface/Backend/data.csv"
    output_file = "interface/Backend/xx.csv"
    processed_df = preprocess_data(input_file, output_file)
    
    # Display information about the processed data
    print("\nSample of processed data:")
    print(processed_df.head())
    
    # Count number of features by category
    feature_counts = {
        "Base features": 7,  # Sexe, Anglais, Francais, Nationale, regional, General, satisfation, performance
        "BAC features": len([col for col in processed_df.columns if col.startswith('BAC_')]),
        "Ville features": len([col for col in processed_df.columns if col.startswith('ville_')]),
        "Subject features": len([col for col in processed_df.columns if col.startswith('deteste_') or col.startswith('preferee_')]),
        "Specialite features": len([col for col in processed_df.columns if col.startswith('specialite_')]),
        "Skills features": len([col for col in processed_df.columns if col.startswith('skills_')]),
        "Loisirs features": len([col for col in processed_df.columns if col.startswith('loisirs_')])
    }
    
    print("\nFeature count by category:")
    for category, count in feature_counts.items():
        print(f"{category}: {count}")