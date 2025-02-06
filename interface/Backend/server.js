const express = require("express");
const fs = require("fs");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = 5000;

// Middleware
app.use(cors()); 
app.use(bodyParser.json()); // kadmen anaho  server ghayfhem data li t sunmitat
const CSV_FILE = "data.csv";

const CSV_HEADERS = [
    "specialite",
    "sexe",
    "ville",
    "niveau_anglais",
    "niveau_francais",
    "matiere_detestee",
    "loisirs",
    "matiere_preferee",
    "soft_skills"
];

const MAPPINGS = {
    sexe: { "0": "Homme", "1": "Femme" },
    niveau_anglais: { "1": "Débutant", "2": "Intermédiaire", "3": "Avancé", "4": "Fluent" },
    niveau_francais: { "1": "Débutant", "2": "Intermédiaire", "3": "Avancé", "4": "Fluent" },
    matiere_detestee: { "0": "None", "1": "Mathématiques", "2": "Physique", "3": "Chimie", "4": "Littérature", "5": "Histoire", "6": "Langues", "7": "Informatique", "8": "Biologie" },
    loisirs: { "1": "Lecture", "2": "Sport", "3": "Musique", "4": "Voyage", "5": "Cinéma", "6": "Jeux vidéo", "7": "Arts plastiques", "8": "Bénévolat", "9": "Technologie", "10": "Ecriture", "11": "Photographie" },
    matiere_preferee: { "1": "Mathématiques", "2": "Physique", "3": "Chimie", "4": "Littérature", "5": "Histoire", "6": "Langues", "7": "Informatique", "8": "Biologie" },
    soft_skills: { "1": "Adaptabilité", "2": "Créativité", "3": "Résolution de problèmes", "4": "Autonomie", "5": "Esprit critique", "6": "Leadership", "7": "Empathie", "8": "Écoute active", "9": "Gestion du stress", "10": "Communication", "11": "Gestion du temps", "12": "Travail en équipe" },
    specialite: { "1": "Sciences Mathématiques", "2": "Sciences de la Vie et de la Terre", "3": "Sciences Agronomiques", "4": "Sciences Physiques", "5": "Sciences et Technologies Électriques", "6": "Sciences et Technologies Mécaniques", "7": "Sciences Économiques", "8": "Sciences de Gestion Comptable", "9": "Lettres", "10": "Sciences Humaines" },
    ville: { 
        "0": "Casablanca", "1": "Rabat", "2": "Fes", "3": "Marrakech", "4": "Tangier", "5": "Agadir", "6": "Meknes", "7": "Oujda", "8": "Kenitra", "9": "Tetouan", "10": "Safi", 
        "11": "Mohammedia", "12": "El Jadida", "13": "Nador", "14": "Beni Mellal", "15": "Taza", "16": "Laayoune", "17": "Dakhla", "18": "Essaouira", "19": "Al Hoceima", 
        "20": "Settat", "21": "Ksar El Kebir", "22": "Tiznit", "23": "Errachidia", "24": "Guercif", "25": "Sidi Kacem", "26": "Taourirt", "27": "Sidi Slimane", 
        "28": "Azrou", "29": "Ouarzazate", "30": "Tan-Tan", "31": "Guelmim", "32": "Smara", "33": "Larache", "34": "Midelt", "35": "Zagora", "36": "Chefchaouen", 
        "37": "Khouribga", "38": "El Kelaa des Sraghna", "39": "Berkane", "40": "Ifrane", "41": "Martil", "42": "Fnideq", "43": "Temara", "44": "Ait Melloul", 
        "45": "Ouazzane", "46": "Imzouren", "47": "Sefrou", "48": "Boujdour", "49": "Chichaoua", "50": "Azemmour", "51": "Aourir", "52": "Bir Jdid", 
        "53": "Taroudant", "54": "Ait Ourir", "55": "Demnate", "56": "Oulad Teima", "57": "Skhirat", "58": "Tinghir", "59": "Bouarfa", "60": "Khémisset", 
        "61": "Jorf El Melha", "62": "Laayoune-Plage"
    }
};


function initializeCSV() {
    if (!fs.existsSync(CSV_FILE)) {
        const headerRow = CSV_HEADERS.join(",") + "\n";
        fs.writeFileSync(CSV_FILE, headerRow, (err) => {
            if (err) console.error("Error creating CSV file:", err);
        });
    }
}

// map numeric values to their corresponding readable values
function mapValues(data) {
    const mappedData = { ...data };

    CSV_HEADERS.forEach(header => {
        if (MAPPINGS[header] && mappedData[header]) {
            mappedData[header] = MAPPINGS[header][mappedData[header]] || mappedData[header];
        }
    });

    return mappedData;
}

// Function to write data to CSV
function writeToCSV(data) {
    const mappedData = mapValues(data); // Convert numeric values to readable strings
    const csvRow = CSV_HEADERS.map(header => mappedData[header] || "").join(",") + "\n";
    
    // Append data to the CSV file
    fs.appendFile(CSV_FILE, csvRow, (err) => {
        if (err) {
            console.error("Error writing to CSV:", err);
        } else {
            console.log("Data saved successfully!");
        }
    });
}

initializeCSV();

app.post("/submit", (req, res) => {
    const userData = req.body;
    writeToCSV(userData);
    res.json({ message: "Data received and saved" });
});


app.listen(PORT, () => {
    console.log(`Server khedam f http://localhost:${PORT}`);
});
