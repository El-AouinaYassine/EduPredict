let ville_select = document.getElementById('ville');
let submit_btn = document.getElementById('submit');
const villes = [ 
    "Casablanca",
    "Rabat",
    "Fes",
    "Marrakech",
    "Tangier",
    "Agadir",
    "Meknes",
    "Oujda",
    "Kenitra",
    "Tetouan",
    "Safi",
    "Mohammedia",
    "El Jadida",
    "Nador",
    "Beni Mellal",
    "Taza",
    "Laayoune",
    "Dakhla",
    "Essaouira",
    "Al Hoceima",
    "Settat",
    "Ksar El Kebir",
    "Tiznit",
    "Errachidia",
    "Guercif",
    "Sidi Kacem",
    "Taourirt",
    "Sidi Slimane",
    "Azrou",
    "Ouarzazate",
    "Tan-Tan",
    "Guelmim",
    "Smara",
    "Larache",
    "Midelt",
    "Zagora",
    "Chefchaouen",
    "Khouribga",
    "El Kelaa des Sraghna",
    "Berkane",
    "Ifrane",
    "Martil",
    "Fnideq",
    "Temara",
    "Ait Melloul",
    "Ouazzane",
    "Imzouren",
    "Sefrou",
    "Boujdour",
    "Chichaoua",
    "Azemmour",
    "Aourir",
    "Bir Jdid",
    "Taroudant",
    "Ait Ourir",
    "Demnate",
    "Oulad Teima",
    "Skhirat",
    "Tinghir",
    "Bouarfa",
    "Khémisset",
    "Jorf El Melha",
    "Laayoune-Plage"
];

// Populate the villes dropdown
villes.forEach((ville, n) => {
    add_ville_option(ville, n);
});

// Listen for click on submit button
submit_btn.addEventListener('click', () => {
    submit_data();
});

function add_ville_option(villeNom, value) {
    let ville_option = document.createElement("option");
    ville_option.textContent = villeNom;
    ville_option.setAttribute("value", value);
    ville_select.appendChild(ville_option);
}

function submit_data() {
    // Collect data from the form
    const userData = {
        specialite: document.getElementById('specialite').value,
        sexe: document.getElementById('sexe').value,
        ville: document.getElementById('ville').value,
        niveau_anglais: document.getElementById('niveau_anglais').value,
        niveau_francais: document.getElementById('niveau_francais').value,
        matiere_detestee: document.getElementById('matiere_detestee').value,
        loisirs: Array.from(document.querySelectorAll('input[name="loisirs"]:checked')).map(el => el.value),
        matiere_preferee: document.getElementById('matiere_preferee').value,
        soft_skills: Array.from(document.querySelectorAll('input[name="soft_skills"]:checked')).map(el => el.value),
    };

    // Send POST request to backend
    fetch('http://localhost:5000/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())
    .then(data => alert(data.message)) // Alert with response message
    .catch(error => console.error('Error:', error)); // Catch any errors
}
