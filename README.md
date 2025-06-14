# Système de Recommandation de Filières pour l'EST

Ce projet utilise l'apprentissage automatique pour recommander aux bacheliers marocains la filière la plus adaptée à leur profil au sein de l’École Supérieure de Technologie (EST).  
Il se base sur des données personnelles et académiques pour suggérer une orientation vers des filières comme : Génie Informatique, Génie Électrique, Techniques de Management, etc.

Ce dépôt est également conçu pour servir de ressource éducative aux débutants souhaitant apprendre à développer un projet de machine learning complet, depuis la collecte des données jusqu'à la prédiction finale.

---
![Screenshot from 2025-06-14 07-30-39](https://github.com/user-attachments/assets/c6d4541b-d2d4-4dcf-90e4-228407104255)
![Screenshot from 2025-06-14 07-30-11](https://github.com/user-attachments/assets/6fa2840c-092f-461e-a8d9-9272f5d9c17b)
![Screenshot from 2025-06-14 07-30-24](https://github.com/user-attachments/assets/e77191c0-b6bd-4af7-809f-4d1105d2a386)

## Stack technique

- **Backend** : Node.js + Express.js (API pour interagir avec le modèle)
- **Machine Learning** : Python (Pandas, Scikit-learn, NumPy, Matplotlib)
- **Manipulation des données** : CSV contenant plus de 10000 profils d'étudiants
---

## Fonctionnement du projet

1. **Collecte et traitement des données**  
   Le dataset contient des informations sur les étudiants, notamment :
   - Ville, spécialité du baccalauréat  
   - Moyennes : nationale, régionale, générale  
   - Niveaux en langues (français, anglais)  
   - Matières préférées et détestées  
   - Compétences personnelles et loisirs

2. **Prétraitement**  
   - Nettoyage des données  
   - Encodage des variables catégorielles  
   - Normalisation des variables numériques

3. **Entraînement du modèle**  
   - Plusieurs modèles testés : arbre de décision, forêt aléatoire, etc.  
   - Sélection du meilleur modèle selon les performances (accuracy, f1-score...)

4. **Prédiction**  
   - Entrée : profil complet d’un étudiant  
   - Sortie : filière recommandée au sein de l’EST

---

## Objectifs pédagogiques

- Montrer comment construire un pipeline ML complet  
- Offrir un exemple clair et commenté pour les débutants  
- Encourager l'utilisation de la data science dans l'aide à l'orientation scolaire

---

## Installation et exécution

> Cette section est à compléter avec les étapes précises pour installer les dépendances et exécuter le projet localement.

```bash
# Exemple
git clone https://github.com/El-AouinaYassine/EduPredict.git
cd EduPredict
pip install -r requirements.txt
node interface/Backend/server.js 
(open interface/index.html)

