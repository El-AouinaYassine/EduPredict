let ville_select = document.getElementById('ville')
let submit_btn = document.getElementById('submit')
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
]



villes.forEach((ville , n)=>{
    add_ville_option(ville , n)
})

submit_btn.addEventListener('click' , ()=>{

    submit_data()
})

function add_ville_option(villeNom , value){
    let ville_option = document.createElement("option")
    ville_option.textContent = villeNom
    ville_option.setAttribute("value" , value)
    ville_select.appendChild(ville_option)
}
function submit_data() {
    let responses = Array.from(document.getElementsByTagName("select"));
    let user = {};

    responses.forEach(res => {
        user[res.id] = res.value;
    });

    // Send the user data to the backend
    fetch("http://localhost:5000/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(user),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Notify the user
    })
    .catch(error => console.error("Error:", error));
}