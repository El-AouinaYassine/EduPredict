import pandas as pd

# Define mapping between categories and their corresponding values
CATEGORIES = {
    # Hex comma-separated columns
    'Ville': [
        'agadir', 'ain taoujdate', 'alhoceima', 'azrou', 'benguerir',
        'beni mellal', 'berkane', 'casa', 'el hajeb', 'fes', 'fez', 'fès',
        'immouzzer', 'khenifra', 'khouribga', 'ksar el kebir', 'larache',
        'marrakech', 'meknes', 'midelt', 'mohammedia', 'mrirt', 'nador',
        'ouazzane', 'ouezzane', 'oujda', 'qatar', 'rabat', 'rich', 'safi',
        'sale', 'sefrou', 'sidi slimane', 'tanger', 'tantan', 'taourirt',
        'taroudant', 'taza', 'tetouan'
    ],
    'specialite_BAC': [
        'Lettres', 'SE', 'SGC', 'SH', 'SM', 'SP', 'STE', 'STM', 'SVT'
    ],
    'Sexe': ['Femme', 'Homme'],
    'specialite': [
        'Informatique', 'Ingenierie', 'Medecine', 'Mathematiques appliquees', 'Droit',
        'Physique', 'Economie', 'Architecture', 'Sciences humaines et sociales', 'Histoire',
        'Arts et design', 'Education', 'Langues étrangeres', 'Geographie', 'Sciences politiques',
        'Biologie', 'Chimie', 'Logistique', 'Reseau', 'Infirmerie'
    ],
    'Loisirs': [
        'chess', 'Lecture', 'Sport', 'Musique', 'Voyage', 'Cinema', 'Jeuxvideo',
        'Artsplastiques', 'Benevolat', 'Technologie', 'Ecriture', 'Photographie'
    ],
    'Skills': [
        'Communication', 'Travailenequipe', 'Gestiondutemps', 'Adaptabilite', 'Creativite',
        'Resolutiondeproblemes', 'Leadership', 'Empathie', 'Espritcritique', 'Autonomie'
    ],
    'detestee': [
        'Mathematiques', 'Physique', 'Chimie', 'Litterature', 'Histoire',
        'Langues', 'Informatique', 'Biologie'
    ],
    'preferee': [
        'Mathematiques', 'Physique', 'Chimie', 'Litterature', 'Histoire',
        'Langues', 'Informatique', 'Biologie'
    ]
}

LANGUAGE_MAPPING = {
    'Débutant': 1,
    'Intermédiaire': 2,
    'Avancé': 3,
    'Courant': 4,
    'Avance': 3  # Assuming 'Avance' is a typo for 'Avancé'
}

def convert_language(value):
    return LANGUAGE_MAPPING.get(value, 2)  # Default to Intermediate (2) if unknown

def process_comma_col(df, column_name, prefix, categories):
    if column_name not in df.columns:
        return pd.DataFrame()
    values = df[column_name].fillna('').astype(str).str.split(',', expand=True)
    values.columns = [f"{prefix}_{cat}" for cat in categories]
    values = values.apply(lambda x: x.apply(lambda v: 1 if v.strip().lower() in cat else 0))
    return values

def process_csv(input_file, output_file):
    df = pd.read_csv(input_file, dtype=str, keep_default_na=False)
    
    # Process numerical columns
    numerical_cols = df[['Age', 'Nationale', 'Regional', 'Generale']]
    # Convert language levels to numeric
    df['Francais'] = df['Francais'].map(lambda x: convert_language(x.strip()))
    df['Anglais'] = df['Anglais'].map(lambda x: convert_language(x.strip()))
    
    # Process categorical columns
    ville = pd.Categorical(df['Ville'], categories=CATEGORIES['Ville'])
    ville_dummies = pd.get_dummies(ville, prefix='Ville')
    
    sexe = pd.Categorical(df['Sexe'], categories=CATEGORIES['Sexe'])
    sexe_dummies = pd.get_dummies(sexe, prefix='Sexe')
    
    bac = pd.Categorical(df['specialite_BAC'], categories=CATEGORIES['specialite_BAC'])
    bac_dummies = pd.get_dummies(bac, prefix='specialite_BAC')
    
    # Process comma-separated columns
    # For detestee
    detestee_categories = CATEGORIES['detestee']
    detestee = df['detestee'].fillna('').astype(str).str.split(',', expand=True)
    detestee = detestee.apply(lambda x: x.str.strip().replace('', 'undefined')).replace('undefined', '')
    detestee = detestee.apply(lambda x: x.apply(lambda v: v if v in detestee_categories else ''))
    detestee = detestee.apply(lambda row: pd.Series((1 if val in detestee_categories else 0 for val in row), index=detestee_categories), axis=1)
    detestee.columns = [f'detestee_{cat}' for cat in detestee_categories]
    
    # For preferee
    preferee_categories = CATEGORIES['preferee']
    preferee = df['preferee'].fillna('').astype(str).str.split(',', expand=True)
    preferee = preferee.apply(lambda x: x.str.strip().replace('', 'undefined')).replace('undefined', '')
    preferee = preferee.apply(lambda x: x.apply(lambda v: v if v in preferee_categories else ''))
    preferee = preferee.apply(lambda row: pd.Series((1 if val in preferee_categories else 0 for val in row), index=preferee_categories), axis=1)
    preferee.columns = [f'preferee_{cat}' for cat in preferee_categories]
    
    # For Loisirs
    loisir_categories = CATEGORIES['Loisirs']
    loisirs = df['Loisirs'].fillna('').astype(str).str.split(',', expand=True)
    loisirs = loisirs.apply(lambda x: x.str.strip().replace('', 'undefined')).replace('undefined', '')
    loisirs = loisirs.apply(lambda x: x.apply(lambda v: v if v in loisir_categories else ''))
    loisirs = loisirs.apply(lambda row: pd.Series((1 if val in loisir_categories else 0 for val in row), index=loisir_categories), axis=1)
    loisirs.columns = [f'Loisir_{cat}' for cat in loisir_categories]
    
    # For Skills
    skill_categories = CATEGORIES['Skills']
    skills = df['Skills'].fillna('').astype(str).str.split(',', expand=True)
    skills = skills.apply(lambda x: x.str.strip().replace('', 'undefined')).replace('undefined', '')
    skills = skills.apply(lambda x: x.apply(lambda v: v if v in skill_categories else ''))
    skills = skills.apply(lambda row: pd.Series((1 if val in skill_categories else 0 for val in row), index=skill_categories), axis=1)
    skills.columns = [f'Skill_{cat}' for cat in skill_categories]
    
    # Process specialite columns (assuming specialite is a comma-separated column)
    specialite_categories = CATEGORIES['specialite']
    specialite = df['specialite'].fillna('').astype(str).str.split(',', expand=True)
    specialite = specialite.apply(lambda x: x.str.strip().replace('', 'undefined')).replace('undefined', '')
    specialite = specialite.apply(lambda x: x.apply(lambda v: v if v in specialite_categories else ''))
    specialite = specialite.apply(lambda row: pd.Series((1 if val in specialite_categories else 0 for val in row), index=specialite_categories), axis=1)
    specialite.columns = [f'specialite_{cat}' for cat in specialite_categories]
    
    # Combine all DataFrames
    result = pd.concat([
        numerical_cols,
        df[['Francais', 'Anglais']],
        sexe_dummies,
        ville_dummies,
        bac_dummies,
        detestee,
        preferee,
        specialite,
        loisirs,
        skills
    ], axis=1)
    
    # Ensure all categories are present in the result
    # This part might need adjustments based on the final columns required
    # For example, existing columns may have different names, so a check is needed
    
    # Reorder columns and rename if necessary to match the desired structure
    
    # Save to CSV
    result.to_csv(output_file, index=False)

# Example usage
if __name__ == "__main__":
    process_csv('interface/Backend/data.csv', 'output_long.csv')