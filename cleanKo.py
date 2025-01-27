import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load dataset (replace ',' with '.' in numerical values)
df = pd.read_csv('ko_v1.csv', delimiter=',')
df.replace(',', '.', regex=True, inplace=True)  # Fix numeric values with commas

# Label encoding for binary values (Gender)
label_encoder = LabelEncoder()
df['Sexe'] = label_encoder.fit_transform(df['Sexe'])  # 'Homme' -> 0, 'Femme' -> 1

# One-hot encoding for categorical columns
df = pd.get_dummies(df, columns=['Ville', 'specialite_BAC', 'specialite', 'preferee', 'detestee'])

# Ordinal encoding for language proficiency levels
ordinal_mapping = {'Debutant': 0, 'Intermediaire': 1, 'Avance': 2}
df['Francais'] = df['Francais'].map(ordinal_mapping)
df['Anglais'] = df['Anglais'].map(ordinal_mapping)

# Multi-label binarization for hobbies and skills (splitting by ', ')
unique_hobbies = set()
df['Loisirs'].dropna().str.split(', ').apply(unique_hobbies.update)
df_hobbies = pd.DataFrame(0, index=df.index, columns=[f'Loisir_{hobby}' for hobby in unique_hobbies])
for hobby in unique_hobbies:
    df_hobbies[f'Loisir_{hobby}'] = df['Loisirs'].apply(lambda x: 1 if pd.notna(x) and hobby in x else 0)
df = pd.concat([df, df_hobbies], axis=1).drop(columns=['Loisirs'])

unique_skills = set()
df['Skills'].dropna().str.split(', ').apply(unique_skills.update)
df_skills = pd.DataFrame(0, index=df.index, columns=[f'Skill_{skill}' for skill in unique_skills])
for skill in unique_skills:
    df_skills[f'Skill_{skill}'] = df['Skills'].apply(lambda x: 1 if pd.notna(x) and skill in x else 0)
df = pd.concat([df, df_skills], axis=1).drop(columns=['Skills'])

# Convert numerical columns to float after replacement
df[['Nationale', 'Regional', 'Generale']] = df[['Nationale', 'Regional', 'Generale']].astype(float)

# Save processed data
df.to_csv('processed_data.csv', index=False)

print("Data preprocessing completed successfully!")
