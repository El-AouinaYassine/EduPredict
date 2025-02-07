import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

# Load your dataset (replace with your CSV path)
df = pd.read_csv("mee.csv")
df.columns = df.columns.str.strip()

# Clean commas and split entries into lists for multi-label columns
df['Loisirs'] = df['Loisirs'].str.split(',')
df['Skills'] = df['Skills'].str.split(',')
df['preferee'] = df['preferee'].str.split(',')
df['detestee'] = df['detestee'].str.split(',')
df['specialite'] = df['specialite'].str.split(',')

# Define fixed categories for the multi-label columns
preferee_categories = ["Mathematiques", "Physique", "Chimie", "Litterature", 
                       "Histoire", "Langues", "Informatique", "Biologie"]

detestee_categories = ["Mathematiques", "Physique", "Chimie", "Litterature", 
                        "Histoire", "Langues", "Informatique", "Biologie"]

specialite_categories = ["Informatique", "Ingenierie", "Medecine", "Mathematiques appliquees",
                         "Droit", "Physique", "Economie", "Architecture", 
                         "Sciences humaines et sociales", "Histoire", "Arts et design",
                         "Education", "Langues étrangeres", "Geographie", "Sciences politiques",
                         "Biologie", "Chimie", "Logistique", "Reseau", "Infirmerie"]

loisirs_categories = ["chess", "Lecture", "Sport", "Voyage", "Cinema", "Jeuxvideo", 
                      "Loisir_Artsplastiques", "Benovolat", "Technologie", "Ecriture", "Photographie"]

skills_categories = ["Communication", "Travailenequipe", "Gestiondutemps", "Adaptabilite", 
                     "Creativite", "Resolutiondeproblemes", "Leadership", "Empathie", 
                     "Espritcritique", "Autonomie"]

# Define the list of cities (as provided)
cities_categories = [
    "larache", "sale", "oujda", "midelt", "rabat", "tetouan", "casa", "taroudant",
    "ouazzane", "beni mellal", "meknes", "el hajeb", "immouzzer", "tantan", "alhoceima",
    "mohammedia", "agadir", "sidi slimane", "rich", "azrou", "taza", "tanger", "berkane",
    "marrakech", "taourirt", "mrirt", "khenifra", "fes", "ain taoujdate", "khouribga",
    "sefrou", "safi", "ouezzane", "nador", "ksar el kebir", "benguerir"
]

# Encode the multi-label columns using MultiLabelBinarizer

# For 'preferee'
mlb_preferee = MultiLabelBinarizer(classes=preferee_categories)
pref_encoded = pd.DataFrame(
    mlb_preferee.fit_transform(df['preferee']),
    columns=[f"preferee_{cat}" for cat in preferee_categories],
    index=df.index
)

# For 'detestee'
mlb_detestee = MultiLabelBinarizer(classes=detestee_categories)
detest_encoded = pd.DataFrame(
    mlb_detestee.fit_transform(df['detestee']),
    columns=[f"detestee_{cat}" for cat in detestee_categories],
    index=df.index
)

# For 'specialite'
mlb_specialite = MultiLabelBinarizer(classes=specialite_categories)
spec_encoded = pd.DataFrame(
    mlb_specialite.fit_transform(df['specialite']),
    columns=[f"specialite_{cat}" for cat in specialite_categories],
    index=df.index
)

# For 'Loisirs'
mlb_loisirs = MultiLabelBinarizer(classes=loisirs_categories)
loisirs_encoded = pd.DataFrame(
    mlb_loisirs.fit_transform(df['Loisirs']),
    columns=[f"loisir_{cat}" for cat in loisirs_categories],
    index=df.index
)

# For 'Skills'
mlb_skills = MultiLabelBinarizer(classes=skills_categories)
skills_encoded = pd.DataFrame(
    mlb_skills.fit_transform(df['Skills']),
    columns=[f"skill_{cat}" for cat in skills_categories],
    index=df.index
)

# For 'Ville': If each row has a single city as a string, convert it to a one-element list
df['Ville'] = df['Ville'].apply(lambda x: [x.strip()] if isinstance(x, str) else x)
mlb_ville = MultiLabelBinarizer(classes=cities_categories)
ville_encoded = pd.DataFrame(
    mlb_ville.fit_transform(df['Ville']),
    columns=[f"Ville_{city}" for city in cities_categories],
    index=df.index
)

# Merge all encoded features with the original DataFrame
df_encoded = pd.concat(
    [df, pref_encoded, detest_encoded, spec_encoded, loisirs_encoded, skills_encoded, ville_encoded],
    axis=1
)

# Drop original text columns that have been encoded
df_encoded = df_encoded.drop(['Loisirs', 'Skills', 'preferee', 'detestee', 'specialite', 'Ville'], axis=1)

# Handle other categorical columns (e.g., 'Sexe', 'specialite_BAC') using get_dummies
df_encoded = pd.get_dummies(
    df_encoded, 
    columns=['Sexe', 'specialite_BAC']
)

# Save the final preprocessed dataset
df_encoded.to_csv('rmrf.csv', index=False)

# Display a preview of the final DataFrame
print(df_encoded.head())
