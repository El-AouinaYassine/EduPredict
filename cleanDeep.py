import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

# Load your dataset (replace with your CSV path)
df = pd.read_csv("ko_v11.csv")

# Clean commas and split entries into lists
df['Loisirs'] = df['Loisirs'].str.split(',')
df['Skills'] = df['Skills'].str.split(',')

# New: Clean and split preferee/detestee/specialite
df['preferee'] = df['preferee'].str.split(',')
df['detestee'] = df['detestee'].str.split(',')
df['specialite'] = df['specialite'].str.split(',')

# Define all possible categories
preferee_categories = ["Mathematiques", "Physique", "Chimie", "Litterature", 
                      "Histoire", "Langues", "Informatique", "Biologie"]
detestee_categories = ["Mathematiques", "Physique", "Chimie", "Litterature", 
                      "Histoire", "Langues", "Informatique", "Biologie"]
specialite_categories = ["Informatique", "Ingenierie", "Medecine", "Mathematiques appliquees",
                        "Droit", "Physique", "Economie", "Architecture", 
                        "Sciences humaines et sociales", "Histoire", "Arts et design",
                        "Education", "Langues étrangeres", "Geographie", "Sciences politiques",
                        "Biologie", "Chimie", "Logistique", "Reseau", "Infirmerie"]

# Encode preferee
mlb_preferee = MultiLabelBinarizer(classes=preferee_categories)
pref_encoded = pd.DataFrame(
    mlb_preferee.fit_transform(df['preferee']),
    columns=[f"preferee_{cat}" for cat in preferee_categories],
    index=df.index
)

# Encode detestee
mlb_detestee = MultiLabelBinarizer(classes=detestee_categories)
detest_encoded = pd.DataFrame(
    mlb_detestee.fit_transform(df['detestee']),
    columns=[f"detestee_{cat}" for cat in detestee_categories],
    index=df.index
)

# Encode specialite
mlb_specialite = MultiLabelBinarizer(classes=specialite_categories)
spec_encoded = pd.DataFrame(
    mlb_specialite.fit_transform(df['specialite']),
    columns=[f"specialite_{cat}" for cat in specialite_categories],
    index=df.index
)

# Merge all encoded features
df_encoded = pd.concat(
    [df, pref_encoded, detest_encoded, spec_encoded], 
    axis=1
)

# Drop original text columns
df_encoded = df_encoded.drop(
    ['Loisirs', 'Skills', 'preferee', 'detestee', 'specialite'], 
    axis=1
)

# Handle other categorical columns (e.g., Sexe, Ville, specialite_BAC)
df_encoded = pd.get_dummies(
    df_encoded, 
    columns=['Sexe', 'Ville', 'specialite_BAC']
)
df_encoded.to_csv('deep.csv' , index=False)
# Fix numeric columns (convert commas to decimals)
numeric_cols = ['Nationale', 'Regional', 'Generale']
for col in numeric_cols:
    df_encoded[col] = df_encoded[col].str.replace(',', '.').astype(float)

# Final preprocessed dataset
print(df_encoded.head())