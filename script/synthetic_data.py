import pandas as pd
import numpy as np
from sklearn.utils import resample
import random
from collections import Counter

# Define constants based on your specifications
SPECIALITE_BAC = ['Lettres', 'SE', 'SGC', 'SH', 'SM', 'SP', 'STE', 'STM', 'SVT']
SEXE = ['M', 'F']
VILLES = ['agadir', 'ain taoujdate', 'alhoceima', 'azrou', 'benguerir', 'beni mellal', 'berkane', 'casa', 
          'el hajeb', 'fes', 'immouzzer', 'khenifra', 'khouribga', 'ksar el kebir', 'larache', 'marrakech', 
          'meknes', 'midelt', 'mohammedia', 'mrirt', 'nador', 'ouazzane', 'ouezzane', 'oujda', 'qatar', 
          'rabat', 'rich', 'safi', 'sale', 'sefrou', 'sidi slimane', 'tanger', 'tantan', 'taourirt', 
          'taroudant', 'taza', 'tetouan']
NIVEAU_LANGUE = ['Débutant', 'Intermédiaire', 'Avancé', 'Courant', 'Avance']
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

# Define relationships between variables for realistic data generation
TECH_SPECIALITES = ['Réseaux et télécommunication', 'Statistique et informatique décisionnelle', 
                   'Génie mécanique et productique', 'Génie électrique', 'Génie des procédés', 
                   'Informatique', 'Génie industriel et maintenance', 'Génie thermique et énergétique']

MANAGEMENT_SPECIALITES = ['Gestion des ressources humaines', 'Technique de gestion commerciale', 
                         'Technique de management', 'Gestion logistique et transport']

TECH_BAC = ['SM', 'SP', 'STE', 'STM', 'SVT']
MANAGEMENT_BAC = ['SE', 'SGC', 'SH', 'Lettres']

# Define subject alignment with specialties
TECH_SUBJECTS = ['Mathématiques', 'Physique', 'Chimie', 'Informatique', 'Sciences de l\'Ingénieur']
MANAGEMENT_SUBJECTS = ['Économie', 'Gestion', 'Histoire', 'Géographie', 'Philosophie']

# Function to load and analyze existing data for bootstrapping
def load_existing_data(file_path=None):
    # If you have a real file, replace this with actual loading
    # For demonstration, we'll create a mock dataset with reasonable distributions
    np.random.seed(42)  # For reproducibility
    
    # Generate mock data with similar structure to your description
    n_samples = 160
    
    data = {
        'specialite_BAC': np.random.choice(SPECIALITE_BAC, n_samples, p=[0.1, 0.15, 0.05, 0.05, 0.2, 0.15, 0.1, 0.1, 0.1]),
        'Sexe': np.random.choice(SEXE, n_samples, p=[0.55, 0.45]),
        'ville': np.random.choice(VILLES, n_samples),
        'Anglais': np.random.choice(NIVEAU_LANGUE, n_samples, p=[0.2, 0.4, 0.25, 0.1, 0.05]),
        'Francais': np.random.choice(NIVEAU_LANGUE, n_samples, p=[0.1, 0.3, 0.35, 0.2, 0.05]),
        'Nationale': np.clip(np.random.normal(12, 3, n_samples), 0, 20),
        'regional': np.clip(np.random.normal(13, 3, n_samples), 0, 20),
        'General': np.clip(np.random.normal(14, 2, n_samples), 0, 20),
        'deteste': np.random.choice(SUBJECTS, n_samples),
        'preferee': np.random.choice(SUBJECTS, n_samples),
        'specialite': np.random.choice(SPECIALITES, n_samples),
        'satisfation': np.random.randint(0, 6, n_samples),
        'performance': np.random.randint(0, 11, n_samples)
    }
    
    # Add loisirs (1-3 hobbies per student)
    data['loisirs'] = [', '.join(np.random.choice(LOISIRS, random.randint(1, 3), replace=False)) for _ in range(n_samples)]
    
    # Add skills (2-4 skills per student)
    data['skills'] = [', '.join(np.random.choice(SKILLS, random.randint(2, 4), replace=False)) for _ in range(n_samples)]
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Make the data more realistic by ensuring preferred and hated subjects are different
    for i in range(len(df)):
        while df.loc[i, 'preferee'] == df.loc[i, 'deteste']:
            df.loc[i, 'deteste'] = np.random.choice(SUBJECTS)
    
    # Create some realistic patterns
    for i in range(len(df)):
        bac = df.loc[i, 'specialite_BAC']
        
        # Align grades with bac specialization
        if bac in ['SM', 'SP']:
            df.loc[i, 'Nationale'] = min(20, df.loc[i, 'Nationale'] + np.random.normal(1, 0.5))
            df.loc[i, 'regional'] = min(20, df.loc[i, 'regional'] + np.random.normal(1, 0.5))
        
        # Align language levels with bac specialization
        if bac == 'Lettres':
            lang_levels = ['Intermédiaire', 'Avancé', 'Courant']
            df.loc[i, 'Francais'] = np.random.choice(lang_levels)
        
        # Align specialite with BAC background
        if bac in TECH_BAC and df.loc[i, 'specialite'] in MANAGEMENT_SPECIALITES:
            if np.random.random() < 0.7:  # 70% chance to align
                df.loc[i, 'specialite'] = np.random.choice(TECH_SPECIALITES)
        elif bac in MANAGEMENT_BAC and df.loc[i, 'specialite'] in TECH_SPECIALITES:
            if np.random.random() < 0.7:  # 70% chance to align
                df.loc[i, 'specialite'] = np.random.choice(MANAGEMENT_SPECIALITES)
    
    return df

# Function to generate synthetic data
def generate_synthetic_data(base_data, n_samples=1000):
    # Bootstrap from existing data
    synthetic_data = resample(base_data, replace=True, n_samples=n_samples)
    
    # Reset index
    synthetic_data = synthetic_data.reset_index(drop=True)
    
    # Add variation to make it less repetitive
    for i in range(len(synthetic_data)):
        # Vary grades slightly
        synthetic_data.loc[i, 'Nationale'] = min(20, max(0, synthetic_data.loc[i, 'Nationale'] + np.random.normal(0, 1)))
        synthetic_data.loc[i, 'regional'] = min(20, max(0, synthetic_data.loc[i, 'regional'] + np.random.normal(0, 1)))
        synthetic_data.loc[i, 'General'] = min(20, max(0, synthetic_data.loc[i, 'General'] + np.random.normal(0, 0.8)))
        
        # Occasionally change city
        if np.random.random() < 0.3:
            synthetic_data.loc[i, 'ville'] = np.random.choice(VILLES)
        
        # Occasionally change hobbies
        if np.random.random() < 0.4:
            n_hobbies = random.randint(1, 3)
            synthetic_data.loc[i, 'loisirs'] = ', '.join(np.random.choice(LOISIRS, n_hobbies, replace=False))
        
        # Occasionally change skills
        if np.random.random() < 0.4:
            n_skills = random.randint(2, 4)
            synthetic_data.loc[i, 'skills'] = ', '.join(np.random.choice(SKILLS, n_skills, replace=False))
            
        # Vary satisfaction and performance
        synthetic_data.loc[i, 'satisfation'] = min(5, max(0, int(round(synthetic_data.loc[i, 'satisfation'] + np.random.normal(0, 0.8)))))
        synthetic_data.loc[i, 'performance'] = min(10, max(0, int(round(synthetic_data.loc[i, 'performance'] + np.random.normal(0, 1.2)))))
    
    return synthetic_data

# Function to apply realistic constraints and relationships
def apply_realistic_constraints(df):
    for i in range(len(df)):
        bac = df.loc[i, 'specialite_BAC']
        specialite = df.loc[i, 'specialite']
        anglais = df.loc[i, 'Anglais']
        prefered = df.loc[i, 'preferee']
        hated = df.loc[i, 'deteste']
        
        # 1. Relationship between English level and IT specialization
        if specialite == 'Informatique' and anglais in ['Débutant']:
            # Lower performance and satisfaction for students with poor English in IT
            df.loc[i, 'performance'] = max(0, min(10, df.loc[i, 'performance'] - random.randint(2, 4)))
            df.loc[i, 'satisfation'] = max(0, min(5, df.loc[i, 'satisfation'] - random.randint(1, 2)))
        
        # 2. Match performance based on BAC speciality and chosen specialization
        # For technical specialties
        if specialite in TECH_SPECIALITES:
            if bac in TECH_BAC:
                # Better performance for students with aligned background
                df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + random.uniform(0.5, 1.5))
            else:
                # Lower performance for humanities students in technical fields
                df.loc[i, 'performance'] = max(0, df.loc[i, 'performance'] - random.uniform(0.5, 1.5))
        
        # For management specialties
        if specialite in MANAGEMENT_SPECIALITES:
            if bac in MANAGEMENT_BAC:
                # Better performance for students with aligned background
                df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + random.uniform(0.5, 1.5))
        
        # 3. Align preferred/hated subjects with specialization
        if specialite in TECH_SPECIALITES:
            # If they hate a technical subject but are in technical specialty, lower performance
            if hated in TECH_SUBJECTS:
                df.loc[i, 'performance'] = max(0, df.loc[i, 'performance'] - random.uniform(0.5, 1))
                df.loc[i, 'satisfation'] = max(0, df.loc[i, 'satisfation'] - random.randint(0, 1))
            
            # If they prefer a technical subject, better performance
            if prefered in TECH_SUBJECTS:
                df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + random.uniform(0.5, 1))
                df.loc[i, 'satisfation'] = min(5, df.loc[i, 'satisfation'] + random.randint(0, 1))
        
        # Similar logic for management specialties
        if specialite in MANAGEMENT_SPECIALITES:
            if hated in MANAGEMENT_SUBJECTS:
                df.loc[i, 'performance'] = max(0, df.loc[i, 'performance'] - random.uniform(0.5, 1))
                df.loc[i, 'satisfation'] = max(0, df.loc[i, 'satisfation'] - random.randint(0, 1))
            
            if prefered in MANAGEMENT_SUBJECTS:
                df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + random.uniform(0.5, 1))
                df.loc[i, 'satisfation'] = min(5, df.loc[i, 'satisfation'] + random.randint(0, 1))
        
        # 4. Relationship between grades and performance
        avg_grade = (df.loc[i, 'Nationale'] + df.loc[i, 'regional'] + df.loc[i, 'General']) / 3
        if avg_grade > 15:  # High achiever
            df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + random.uniform(0.5, 1.5))
        elif avg_grade < 10:  # Struggling student
            df.loc[i, 'performance'] = max(0, df.loc[i, 'performance'] - random.uniform(0.5, 1.5))
        
        # 5. Consider hobbies and skills for specific fields
        hobbies = df.loc[i, 'loisirs'].split(', ')
        skills = df.loc[i, 'skills'].split(', ')
        
        # For IT specialties, technology as a hobby is beneficial
        if specialite == 'Informatique' and 'Technologie' in hobbies:
            df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + random.uniform(0.5, 1))
            df.loc[i, 'satisfation'] = min(5, df.loc[i, 'satisfation'] + random.randint(0, 1))
        
        # For management, communication skills are important
        if specialite in MANAGEMENT_SPECIALITES and 'Communication' in skills:
            df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + random.uniform(0.5, 1))
            
        # Problem-solving is valuable in technical fields
        if specialite in TECH_SPECIALITES and 'Resolutiondeproblemes' in skills:
            df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + random.uniform(0.5, 1))
        
        # Round performance and satisfaction to integers
        df.loc[i, 'performance'] = int(round(df.loc[i, 'performance']))
        df.loc[i, 'satisfation'] = int(round(df.loc[i, 'satisfation']))
    
    return df

# Main function to generate the dataset
def generate_dataset(n_samples=1000, output_file="synthetic_student_data.csv"):
    # Load existing data or create mock data
    base_data = load_existing_data('./script/data/basedData.csv')
    
    # Generate synthetic data by bootstrapping
    synthetic_data = generate_synthetic_data(base_data, n_samples)
    
    # Apply realistic constraints
    synthetic_data = apply_realistic_constraints(synthetic_data)
    
    # Round numerical columns
    synthetic_data['Nationale'] = synthetic_data['Nationale'].round(2)
    synthetic_data['regional'] = synthetic_data['regional'].round(2)
    synthetic_data['General'] = synthetic_data['General'].round(2)
    
    # Save to CSV
    synthetic_data.to_csv(output_file, index=False)
    
    # Print sample and statistics
    print(f"Generated {n_samples} synthetic student records")
    print("\nSample records:")
    print(synthetic_data.head())
    
    print("\nDistribution of specializations:")
    print(synthetic_data['specialite'].value_counts())
    
    print("\nDistribution of BAC specialties:")
    print(synthetic_data['specialite_BAC'].value_counts())
    
    print("\nAverage performance by specialization:")
    print(synthetic_data.groupby('specialite')['performance'].mean().sort_values(ascending=False))
    
    return synthetic_data

# Generate the dataset
if __name__ == "__main__":
    synthetic_data = generate_dataset(1000)
    
    # Display some correlation statistics
    print("\nCorrelation between grades and performance:")
    print(synthetic_data[['Nationale', 'regional', 'General', 'performance']].corr()['performance'])
    
    # Check if our constraints worked - Example: IT speciality and English level
    print("\nAverage performance in IT by English level:")
    it_students = synthetic_data[synthetic_data['specialite'] == 'Informatique']
    print(it_students.groupby('Anglais')['performance'].mean().sort_values(ascending=False))