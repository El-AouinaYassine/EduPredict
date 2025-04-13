
# Définir des constantes basées sur les données réelles
SPECIALITE_BAC = ['Lettres', 'SE', 'SGC', 'SH', 'SM', 'SP', 'STE', 'STM', 'SVT']
SPECIALITES = ['Informatique', 'Génie électrique', 'Gestion des ressources humaines', 'Gestion logistique']

def load_existing_data():
    # Simuler un jeu de données avec 137 réponses
    data = {
        'specialite_BAC': np.random.choice(SPECIALITE_BAC, 137),
        'Nationale': np.random.normal(12, 3, 137),  # Note moyenne autour de 12
        'performance': np.random.randint(0, 11, 137),  # Performance de 0 à 10
        'satisfation': np.random.randint(0, 6, 137),  # Satisfaction de 0 à 5
        'specialite': np.random.choice(SPECIALITES, 137)
    }
    return pd.DataFrame(data)

# Générer des données synthétiques par bootstrapping
def generate_synthetic_data(base_data, n_samples=1000):
    # Utiliser resample pour créer des échantillons avec remplacement
    synthetic_data = resample(base_data, replace=True, n_samples=n_samples)
    synthetic_data = synthetic_data.reset_index(drop=True)
    
    # Ajouter de la variation réaliste aux données
    for i in range(len(synthetic_data)):
        synthetic_data.loc[i, 'Nationale'] = min(20, max(0, synthetic_data.loc[i, 'Nationale'] + np.random.normal(0, 1)))
        synthetic_data.loc[i, 'performance'] = min(10, max(0, int(synthetic_data.loc[i, 'performance'] + np.random.normal(0, 1))))
        synthetic_data.loc[i, 'satisfation'] = min(5, max(0, int(synthetic_data.loc[i, 'satisfation'] + np.random.normal(0, 0.8))))
    
    return synthetic_data

# Appliquer des contraintes pour respecter les relations logiques
def apply_realistic_constraints(df):
    for i in range(len(df)):
        bac = df.loc[i, 'specialite_BAC']
        specialite = df.loc[i, 'specialite']
        
        # Exemple de contrainte : ajuster la performance selon la spécialité BAC et la filière
        if bac in ['SM', 'SP', 'STE'] and specialite in ['Informatique', 'Génie électrique']:
            df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + np.random.uniform(0.5, 1.5))
        elif bac in ['SE', 'SGC'] and specialite in ['Gestion des ressources humaines', 'Gestion logistique']:
            df.loc[i, 'performance'] = min(10, df.loc[i, 'performance'] + np.random.uniform(0.5, 1))
        
        # Arrondir les valeurs pour plus de réalisme
        df.loc[i, 'performance'] = int(round(df.loc[i, 'performance']))
        df.loc[i, 'satisfation'] = int(round(df.loc[i, 'satisfation']))
    
    return df

# Fonction principale pour générer les données synthétiques
def generate_dataset(n_samples=1000):
    # Charger les données de base
    base_data = load_existing_data()
    
    # Générer des données synthétiques
    synthetic_data = generate_synthetic_data(base_data, n_samples)
    
    # Appliquer des contraintes réalistes
    synthetic_data = apply_realistic_constraints(synthetic_data)
    
    # Afficher un aperçu (pour illustration)
    print("Exemple de données synthétiques :")
    print(synthetic_data.head())
    
    return synthetic_data

# Générer les données
synthetic_data = generate_dataset(1000)