import pandas as pd
import numpy as np

def preprocess_data_robust(input_file, output_file=None, is_prediction_data=False):
    SPECIALITE_BAC = ['Lettres', 'SE', 'SGC', 'SH', 'SM', 'SP', 'STE', 'STM', 'SVT']
    VILLES = ['agadir', 'ain taoujdate', 'alhoceima', 'azrou', 'benguerir', 'beni mellal', 'berkane', 'casa', 
              'el hajeb', 'fes', 'immouzzer', 'khenifra', 'khouribga', 'ksar el kebir', 'larache', 'marrakech', 
              'meknes', 'midelt', 'mohammedia', 'mrirt', 'nador', 'ouazzane', 'ouezzane', 'oujda', 'qatar', 
              'rabat', 'rich', 'safi', 'sale', 'sefrou', 'sidi slimane', 'tanger', 'tantan', 'taourirt', 
              'taroudant', 'taza', 'tetouan']
    SUBJECTS = ['Mathématiques', 'Physique', 'Chimie', 'Biologie', 'Histoire', 'Géographie', 
                'Philosophie', 'Langue Arabe', 'Langue Française', 'Informatique', 'Économie', 
                'Gestion', 'Sciences de l\'Ingénieur', 'Anglais']
    LOISIRS = ['Lecture', 'Sport', 'Musique', 'Voyage', 'Cinema', 'Jeuxvideo', 'Artsplastiques', 
               'Benevolat', 'Technologie', 'Ecriture', 'Photographie']
    SKILLS = ['Adaptabilite', 'Creativite', 'Resolutiondeproblemes', 'Autonomie', 'Espritcritique', 
              'Leadership', 'Empathie', 'Ecouteactive', 'Gestiondustress', 'Communication', 
              'Gestiondutemps', 'Travailenequipe']
    SPECIALITES = ['Réseaux et télécommunication', 'Statistique et informatique décisionnelle', 
                   'Génie mécanique et productique', 'Génie électrique', 'Génie des procédés', 
                   'Gestion des ressources humaines', 'Technique de gestion commerciale', 
                   'Technique de management', 'Gestion logistique et transport', 
                   'Génie thermique et énergétique', 'Informatique', 'Génie industriel et maintenance']
    
    df = pd.read_csv(input_file)
    
    processed_data = pd.DataFrame(index=range(len(df)))
    
    processed_data['Sexe'] = df['Sexe'].map({'Femme': 1, 'Homme': 0})
    
    language_mapping = {
        'Debutant': 1,
        'Intermediaire': 2,
        'Avance': 3,
        'Courant': 4,
    }
    
    processed_data['Anglais'] = df['Anglais'].map(language_mapping)
    processed_data['Francais'] = df['Francais'].map(language_mapping)
    
    # Keep numerical values as they are (except target features if prediction data)
    numerical_cols = ['Nationale', 'regional', 'General']
    if not is_prediction_data:
        numerical_cols.extend(['satisfation', 'performance'])
    
    for col in numerical_cols:
        if col in df.columns:  # Only include if column exists
            processed_data[col] = df[col]
    
    # Create complete one-hot encodings for all categorical variables
    
    # 1. Specialite_BAC - Create one-hot columns for ALL possible BAC types
    bac_df = pd.DataFrame(0, index=df.index, columns=[f'BAC_{bac}' for bac in SPECIALITE_BAC])
    # Now mark the ones that are present in the data
    for i, bac in enumerate(df['specialite_BAC']):
        if bac in SPECIALITE_BAC:
            bac_df.at[i, f'BAC_{bac}'] = 1
    
    # 2. Ville - Create one-hot columns for ALL possible cities
    ville_df = pd.DataFrame(0, index=df.index, columns=[f'ville_{ville}' for ville in VILLES])
    # Mark the ones that are present
    for i, ville in enumerate(df['ville']):
        if ville in VILLES:
            ville_df.at[i, f'ville_{ville}'] = 1
    
    # 3. Subjects (deteste and preferee) - Create one-hot columns for ALL possible subjects
    deteste_df = pd.DataFrame(0, index=df.index, columns=[f'deteste_{subject}' for subject in SUBJECTS])
    preferee_df = pd.DataFrame(0, index=df.index, columns=[f'preferee_{subject}' for subject in SUBJECTS])
    
    # Mark the ones that are present
    for i, subject in enumerate(df['deteste']):
        if subject in SUBJECTS:
            deteste_df.at[i, f'deteste_{subject}'] = 1
    
    for i, subject in enumerate(df['preferee']):
        if subject in SUBJECTS:
            preferee_df.at[i, f'preferee_{subject}'] = 1
    
    # 4. Specialite - Create one-hot columns for ALL possible specialties
    specialite_df = pd.DataFrame(0, index=df.index, columns=[f'specialite_{spec}' for spec in SPECIALITES])
    # Mark the ones that are present
    for i, spec in enumerate(df['specialite']):
        if spec in SPECIALITES:
            specialite_df.at[i, f'specialite_{spec}'] = 1
    
    # 5. Skills - Create one-hot columns for ALL possible skills
    skills_df = pd.DataFrame(0, index=df.index, columns=[f'skills_{skill}' for skill in SKILLS])
    # Fill the skill columns
    for idx, skills_str in enumerate(df['skills']):
        if isinstance(skills_str, str):  # Check if it's a string
            skills_list = [skill.strip() for skill in skills_str.split(',')]
            for skill in skills_list:
                if skill in SKILLS:
                    skills_df.at[idx, f'skills_{skill}'] = 1
    
    # 6. Loisirs - Create one-hot columns for ALL possible loisirs
    loisirs_df = pd.DataFrame(0, index=df.index, columns=[f'loisirs_{loisir}' for loisir in LOISIRS])
    # Fill the loisir columns
    for idx, loisirs_str in enumerate(df['loisirs']):
        if isinstance(loisirs_str, str):  # Check if it's a string
            loisirs_list = [loisir.strip() for loisir in loisirs_str.split(',')]
            for loisir in loisirs_list:
                if loisir in LOISIRS:
                    loisirs_df.at[idx, f'loisirs_{loisir}'] = 1
    
    # Combine all dataframes
    all_dfs = [processed_data, bac_df, ville_df, deteste_df, 
               preferee_df, specialite_df, skills_df, loisirs_df]
    processed_data = pd.concat(all_dfs, axis=1)
    
    # Remove target columns if this is prediction data
    if is_prediction_data and 'satisfation' in processed_data.columns:
        processed_data = processed_data.drop(['satisfation', 'performance'], axis=1, errors='ignore')
    
    # Save to file if specified
    if output_file:
        processed_data = processed_data.replace({'TRUE': 1, 'FALSE': 0, 'True': 1, 'False': 0, True: 1, False: 0})
        processed_data.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
        print(f"Shape of processed data: {processed_data.shape}")
        print(f"Total number of features: {processed_data.shape[1]}")
    
    return processed_data

# Function for processing a single data point (e.g., from a web form)
def preprocess_single_datapoint(data_dict, output_file=None):
    """
    Process a single data point (e.g., from a web form) to make predictions
    
    Args:
        data_dict (dict): Dictionary containing the student data
        output_file (str, optional): Path to save the processed data
        
    Returns:
        pandas.DataFrame: Processed dataframe with one row ready for prediction
    """
    # Convert the dictionary to a dataframe with one row
    df = pd.DataFrame([data_dict])
    
    # Save to temporary CSV
    temp_csv = 'temp_single_datapoint.csv'
    df.to_csv(temp_csv, index=False)
    
    # Process using our robust function
    processed_df = preprocess_data_robust(temp_csv, output_file, is_prediction_data=True)
    
    # Clean up temporary file
    import os
    try:
        os.remove(temp_csv)
    except:
        pass

    return processed_df

# Example usage
if __name__ == "__main__":
    # Process training data
    training_input = "interface/Backend/data.csv"
    training_output = "interface/Backend/tr1.csv"
    training_df = preprocess_data_robust(training_input, training_output)
    
    # Process prediction data (new data without target variables)
    prediction_input = "prediction_data.csv"
    prediction_output = "processed_prediction_data.csv"
    prediction_df = preprocess_data_robust(prediction_input, prediction_output, is_prediction_data=True)
    
    # Example of processing a single data point (e.g., from a web form)
    single_data = {
        'Sexe': 'M',
        'Anglais': 'Intermédiaire',
        'Francais': 'Avancé',
        'Nationale': 15.6,
        'regional': 16.2,
        'General': 15.8,
        'specialite_BAC': 'SM',
        'ville': 'fes',
        'deteste': 'Histoire',
        'preferee': 'Mathématiques',
        'specialite': 'Informatique',
        'skills': 'Resolutiondeproblemes, Travailenequipe, Communication',
        'loisirs': 'Sport, Technologie'
    }
    
    single_processed = preprocess_single_datapoint(single_data, "processed_single_datapoint.csv")
    print("\nSample of processed single datapoint:")
    print(f"Shape: {single_processed.shape}")