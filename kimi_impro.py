import pandas as pd

def convert_boolean_columns(df):
    df_copy = df.copy()
    for column in df_copy.columns:
        unique_values = set(df_copy[column].dropna().unique())
        if unique_values.issubset({True, False}) or unique_values.issubset({'TRUE', 'FALSE', 'True', 'False'}):
            if df_copy[column].dtype == 'object':
                df_copy[column] = df_copy[column].map({'TRUE': True, 'FALSE': False, 
                                                       'True': True, 'False': False})
            df_copy[column] = df_copy[column].fillna(False).astype(int)  # Fill NaN with False
    return df_copy

CATEGORIES = {
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
    'Avance': 3
}

def convert_language(value):
    return LANGUAGE_MAPPING.get(value.strip(), 2)

def process_comma_column(series, categories, prefix):
    processed = series.fillna('').str.strip().str.lower().str.replace(' ', '_')
    exploded = processed.str.split(',').explode().str.strip()
    exploded = exploded[exploded != '']
    exploded = pd.Series(
        pd.Categorical(exploded.values, categories=categories),
        index=exploded.index
    )
    dummies = pd.get_dummies(exploded, prefix=prefix)
    result = dummies.groupby(level=0).max().fillna(0).astype(int)
    return result

def process_csv(input_file, output_file):
    df = pd.read_csv(input_file, dtype=str, keep_default_na=False)
    df.columns = df.columns.str.strip()
    print("Columns in the DataFrame:", df.columns.tolist())

    # Updated numerical columns to include 'performance' and 'satisfaction'
    expected_numerical_cols = ['Nationale', 'Regional', 'Generale', 'performance', 'satisfaction']
    available_numerical_cols = [col for col in expected_numerical_cols if col in df.columns]
    if not available_numerical_cols:
        print("Warning: None of the expected numerical columns found.")
        numerical_cols = pd.DataFrame(index=df.index)
    else:
        # Convert to float to handle numerical values properly
        numerical_cols = df[available_numerical_cols].astype(float)

    language_cols = {}
    for lang in ['Francais', 'Anglais']:
        if lang in df.columns:
            language_cols[lang] = df[lang].apply(lambda x: convert_language(x))
        else:
            print(f"Warning: '{lang}' column not found. Using default value (2).")
            language_cols[lang] = pd.Series(2, index=df.index)

    if 'Sexe' in df.columns:
        sexe = pd.Categorical(df['Sexe'], categories=CATEGORIES['Sexe'])
        sexe_dummies = pd.get_dummies(sexe, prefix='Sexe')
    else:
        raise ValueError("Required column 'Sexe' not found in the CSV.")

    if 'Ville' in df.columns:
        ville = pd.Categorical(df['Ville'], categories=CATEGORIES['Ville'])
        ville_dummies = pd.get_dummies(ville, prefix='Ville')
    else:
        raise ValueError("Required column 'Ville' not found in the CSV.")

    if 'specialite_BAC' in df.columns:
        bac = pd.Categorical(df['specialite_BAC'], categories=CATEGORIES['specialite_BAC'])
        bac_dummies = pd.get_dummies(bac, prefix='specialite_BAC')
    else:
        raise ValueError("Required column 'specialite_BAC' not found in the CSV.")

    if 'preferee' in df.columns:
        preferee = process_comma_column(df['preferee'], CATEGORIES['preferee'], 'preferee')
    else:
        print("Warning: 'preferee' column not found.")
        preferee = pd.DataFrame(0, index=df.index, columns=[f'preferee_{cat}' for cat in CATEGORIES['preferee']])

    if 'detestee' in df.columns:
        detestee = process_comma_column(df['detestee'], CATEGORIES['detestee'], 'detestee')
    else:
        print("Warning: 'detestee' column not found.")
        detestee = pd.DataFrame(0, index=df.index, columns=[f'detestee_{cat}' for cat in CATEGORIES['detestee']])

    if 'specialite' in df.columns:
        specialite = process_comma_column(df['specialite'], CATEGORIES['specialite'], 'specialite')
    else:
        print("Warning: 'specialite' column not found.")
        specialite = pd.DataFrame(0, index=df.index, columns=[f'specialite_{cat}' for cat in CATEGORIES['specialite']])

    if 'Loisirs' in df.columns:
        loisirs = process_comma_column(df['Loisirs'], CATEGORIES['Loisirs'], 'Loisir')
    else:
        print("Warning: 'Loisirs' column not found.")
        loisirs = pd.DataFrame(0, index=df.index, columns=[f'Loisir_{cat}' for cat in CATEGORIES['Loisirs']])

    if 'Skills' in df.columns:
        skills = process_comma_column(df['Skills'], CATEGORIES['Skills'], 'Skill')
    else:
        print("Warning: 'Skills' column not found.")
        skills = pd.DataFrame(0, index=df.index, columns=[f'Skill_{cat}' for cat in CATEGORIES['Skills']])

    result = pd.concat([
        numerical_cols,
        pd.DataFrame(language_cols),
        preferee,
        detestee,
        specialite,
        ville_dummies,
        sexe_dummies,
        bac_dummies,
        loisirs,
        skills
    ], axis=1)

    result = convert_boolean_columns(result)
    result.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

if __name__ == "__main__":
    process_csv('data.csv', 'newDataCleaned.csv')