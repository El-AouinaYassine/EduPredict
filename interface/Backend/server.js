
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const fs = require('fs');

const app = express();
const port = 5000;
const CSV_FILE_PATH = 'user_data.csv';

// Data mappings
const SPECIALITE_MAP = {
  '1': 'Sciences Mathématiques',
  '2': 'Sciences de la Vie et de la Terre',
  '3': 'Sciences Agronomiques',
  '4': 'Sciences Physiques',
  '5': 'Sciences et Technologies Électriques',
  '6': 'Sciences et Technologies Mécaniques',
  '7': 'Sciences Économiques',
  '8': 'Sciences de Gestion Comptable',
  '9': 'Lettres',
  '10': 'Sciences Humaines'
};

const SEXE_MAP = {
  '0': 'Homme',
  '1': 'Femme'
};

const VILLES = [
  "Casablanca", "Rabat", "Fes", "Marrakech", "Tangier", "Agadir", "Meknes",
  "Oujda", "Kenitra", "Tetouan", "Safi", "Mohammedia", "El Jadida", "Nador",
  "Beni Mellal", "Taza", "Laayoune", "Dakhla", "Essaouira", "Al Hoceima",
  "Settat", "Ksar El Kebir", "Tiznit", "Errachidia", "Guercif", "Sidi Kacem",
  "Taourirt", "Sidi Slimane", "Azrou", "Ouarzazate", "Tan-Tan", "Guelmim",
  "Smara", "Larache", "Midelt", "Zagora", "Chefchaouen", "Khouribga",
  "El Kelaa des Sraghna", "Berkane", "Ifrane", "Martil", "Fnideq", "Temara",
  "Ait Melloul", "Ouazzane", "Imzouren", "Sefrou", "Boujdour", "Chichaoua",
  "Azemmour", "Aourir", "Bir Jdid", "Taroudant", "Ait Ourir", "Demnate",
  "Oulad Teima", "Skhirat", "Tinghir", "Bouarfa", "Khémisset", "Jorf El Melha",
  "Laayoune-Plage"
];

const NIVEAU_LANGUE_MAP = {
  '1': 'Débutant',
  '2': 'Intermédiaire',
  '3': 'Avancé',
  '4': 'Fluent'
};

const MATIERE_MAP = {
  '0': 'None',
  '1': 'Mathématiques',
  '2': 'Physique',
  '3': 'Chimie',
  '4': 'Littérature',
  '5': 'Histoire',
  '6': 'Langues',
  '7': 'Informatique',
  '8': 'Biologie'
};

const LOISIRS_MAP = {
  '1': 'Lecture',
  '2': 'Sport',
  '3': 'Musique',
  '4': 'Voyage',
  '5': 'Cinéma',
  '6': 'Jeux vidéo',
  '7': 'Arts plastiques',
  '8': 'Bénévolat',
  '9': 'Technologie',
  '10': 'Ecriture',
  '11': 'Photographie'
};

const SOFT_SKILLS_MAP = {
  '1': 'Adaptabilité',
  '2': 'Créativité',
  '3': 'Résolution de problèmes',
  '4': 'Autonomie',
  '5': 'Esprit critique',
  '6': 'Leadership',
  '7': 'Empathie',
  '8': 'Écoute active',
  '9': 'Gestion du stress',
  '10': 'Communication',
  '11': 'Gestion du temps',
  '12': 'Travail en équipe'
};

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Function to create CSV writer
function createWriter(append = false) {
  return createCsvWriter({
    path: CSV_FILE_PATH,
    header: [
      { id: 'age', title: 'Age' },
      { id: 'specialite', title: 'Specialite' },
      { id: 'sexe', title: 'Sexe' },
      { id: 'ville', title: 'Ville' },
      { id: 'niveau_anglais', title: 'Niveau_anglais' },
      { id: 'niveau_francais', title: 'Niveau_francais' },
      { id: 'note_nat', title: 'Nationale' },
      { id: 'note_reg', title: 'Regionale' },
      { id: 'note_gen', title: 'Generale' },
      { id: 'matiere_detestee', title: 'Matiere_detestee' },
      { id: 'loisirs', title: 'Loisirs' },
      { id: 'matiere_preferee', title: 'Matiere_preferee' },
      { id: 'soft_skills', title: 'Soft_skills' }
    ],
    append: append
  });
}

// Transform numerical data to text
function transformData(userData) {
  return {
    age: userData.age,
    specialite: SPECIALITE_MAP[userData.specialite] || '',
    sexe: SEXE_MAP[userData.sexe] || '',
    ville: VILLES[userData.ville] || '',
    niveau_anglais: NIVEAU_LANGUE_MAP[userData.niveau_anglais] || '',
    niveau_francais: NIVEAU_LANGUE_MAP[userData.niveau_francais] || '',
    note_nat: userData.note_nat,
    note_reg: userData.note_reg,
    note_gen: userData.note_gen,
    matiere_detestee: MATIERE_MAP[userData.matiere_detestee] || '',
    loisirs: userData.loisirs.map(id => LOISIRS_MAP[id]).filter(Boolean).join(', '),
    matiere_preferee: MATIERE_MAP[userData.matiere_preferee] || '',
    soft_skills: userData.soft_skills.map(id => SOFT_SKILLS_MAP[id]).filter(Boolean).join(', ')
  };
}

// Handle POST request
app.post('/submit', async (req, res) => {
  try {
    const userData = req.body;
    const formattedData = transformData(userData);
    
    // Check if file exists
    const fileExists = fs.existsSync(CSV_FILE_PATH);
    
    // Create CSV writer with appropriate append setting
    const csvWriter = createWriter(fileExists);

    // Write the data
    await csvWriter.writeRecords([formattedData]);
    
    res.json({ message: 'Data submitted and saved to CSV' });
  } catch (error) {
    console.error('Error writing to CSV:', error);
    res.status(500).json({ message: 'Error saving data to CSV' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
