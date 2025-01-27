import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer


df = pd.read_csv("ko_v1.csv")  # Load your actual CSV file

loisir_categories = ["chess","Lecture", "Sport", "Musique", "Voyage", "Cinema", 
                    "Jeuxvideo", "Artsplastiques", "Benevolat", "Technologie", 
                    "Ecriture", "Photographie"]

skill_categories = ["Communication", "Travailenequipe", "Gestiondutemps", 
                   "Adaptabilite", "Creativite", "Resolutiondeproblemes", 
                   "Leadership", "Empathie", "Espritcritique", "Autonomie"]

df['Loisirs'] = df['Loisirs'].str.split(',')
df['Skills'] = df['Skills'].str.split(',')

# Create binary features for Loisirs
mlb_loisirs = MultiLabelBinarizer(classes=loisir_categories)
loisir_encoded = pd.DataFrame(mlb_loisirs.fit_transform(df['Loisirs']),
                             columns=[f"Loisir_{cat}" for cat in loisir_categories],
                             index=df.index)

mlb_skills = MultiLabelBinarizer(classes=skill_categories)
skills_encoded = pd.DataFrame(mlb_skills.fit_transform(df['Skills']),
                             columns=[f"Skill_{cat}" for cat in skill_categories],
                             index=df.index)

# Merge encoded features with original dataframe
df_encoded = pd.concat([df, loisir_encoded, skills_encoded], axis=1)

# Drop original text columns
df_encoded = df_encoded.drop(['Loisirs', 'Skills'], axis=1)

# Handle other categorical columns (example for 'Sexe' and 'Ville')
df_encoded = pd.get_dummies(df_encoded, columns=['Sexe', 'Ville', 'specialite_BAC'])

# Convert numeric columns with commas to floats
numeric_cols = ['Nationale', 'Regional', 'Generale']
for col in numeric_cols:
    df_encoded[col] = df_encoded[col].str.replace(',', '.').astype(float)

df.to_csv("newFuckingShit.csv" , index=False)