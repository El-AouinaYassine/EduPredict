const inject_reco_card = (title , per_n , sat_n)=>{
    const cardHTML = `
                    <div class="recommendation-card">
                        <h4 class="recommendation-name">${specialty}</h4>
                        <div class="progress-item">
                            <span class="progress-text">Performance</span>
                            <span class="progress-value">${performance}/10</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-bar-fill blue-fill" style="width: ${performance * 10}%"></div>
                        </div>
                        <div class="progress-item">
                            <span class="progress-text">Satisfaction</span>
                            <span class="progress-value">${satisfaction}/10</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-bar-fill green-fill" style="width: ${satisfaction * 10}%"></div>
                        </div>
                    </div>
                `;
}
document.addEventListener('DOMContentLoaded', function() {
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Tab navigation logic
    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            tabLinks.forEach(l => l.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Mobile menu toggle
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuBtn) {
        menuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('show');
        });
    }

    // Populate ville select dropdown
    const villeSelect = document.getElementById('ville');
    if (villeSelect) {
        const villes = [ 
            "Casablanca", "Rabat", "Fes", "Marrakech", "Tangier", "Agadir", "Meknes", "Oujda", 
            "Kenitra", "Tetouan", "Safi", "Mohammedia", "El Jadida", "Nador", "Beni Mellal", 
            "Taza", "Laayoune", "Dakhla", "Essaouira", "Al Hoceima", "Settat", "Ksar El Kebir", 
            "Tiznit", "Errachidia", "Guercif", "Sidi Kacem", "Taourirt", "Sidi Slimane", "Azrou", 
            "Ouarzazate", "Tan-Tan", "Guelmim", "Smara", "Larache", "Midelt", "Zagora", 
            "Chefchaouen", "Khouribga", "El Kelaa des Sraghna", "Berkane", "Ifrane", "Martil", 
            "Fnideq", "Temara", "Ait Melloul", "Ouazzane", "Imzouren", "Sefrou", "Boujdour", 
            "Chichaoua", "Azemmour", "Aourir", "Bir Jdid", "Taroudant", "Ait Ourir", "Demnate", 
            "Oulad Teima", "Skhirat", "Tinghir", "Bouarfa", "Khémisset", "Jorf El Melha", 
            "Laayoune-Plage"
        ];
        
        villes.forEach((ville, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = ville;
            villeSelect.appendChild(option);
        });
    }
    
    const submitBtn = document.getElementById('submit');
    if (submitBtn) {
        submitBtn.addEventListener('click', function(e) {
            e.preventDefault(); 
            const formData = {
                age: document.getElementById('age').value,
                sexe: document.getElementById('sexe').value,
                ville: document.getElementById('ville').value,
                specialite: document.getElementById('specialite').value,
                note_nat: document.getElementById('note_nat').value,
                note_reg: document.getElementById('note_reg').value,
                note_gen: document.getElementById('note_gen').value,
                niveau_francais: document.getElementById('niveau_francais').value,
                niveau_anglais: document.getElementById('niveau_anglais').value,
                matiere_preferee: document.getElementById('matiere_preferee').value,
                matiere_detestee: document.getElementById('matiere_detestee').value,
                specialite1: document.getElementById('specialite1').value,
                loisirs: Array.from(document.querySelectorAll('input[name="loisirs"]:checked')).map(el => el.value),
                soft_skills: Array.from(document.querySelectorAll('input[name="soft_skills"]:checked')).map(el => el.value)
            };
            
            fetch('http://localhost:5000/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                
                setTimeout(() => {
                    fetch('http://localhost:5000/result')
                    .then(response => response.json())
                    .then(resultData => {
                        console.log('Prediction results:', resultData);
                        
                        if (resultData && resultData.result && resultData.result.length >= 2) {
                            const performanceElement = document.getElementById('performance_res');
                            const satisfactionElement = document.getElementById('satisfaction_res');
                            
                            if (performanceElement) {
                                performanceElement.textContent = parseFloat(resultData.result[0]).toFixed(2);
                                const progressBarFill = performanceElement.parentElement.querySelector('.progress-bar-fill');
                                if (progressBarFill) {
                                    progressBarFill.style.width = `${resultData.result[0] * 10}%`;
                                }
                                
                                const progressText = performanceElement.parentElement.querySelector('.progress-label .progress-text:last-child');
                                if (progressText) {
                                    progressText.textContent = `${(resultData.result[0])}/10`;
                                }
                            }
                            
                            if (satisfactionElement) {
                                satisfactionElement.textContent = parseFloat(resultData.result[1]*2).toFixed(2);
                                const progressBarFill = satisfactionElement.parentElement.querySelector('.progress-bar-fill');
                                if (progressBarFill) {
                                    progressBarFill.style.width = `${resultData.result[1]*2 * 10}%`;
                                }
                                
                                const progressText = satisfactionElement.parentElement.querySelector('.progress-label .progress-text:last-child');
                                if (progressText) {
                                    progressText.textContent = `${(resultData.result[1]*2).toFixed(2)}/10`;
                                }
                            }
                            
                            const resultsTabLink = document.querySelector('.tab-link[data-tab="results"]');
                            if (resultsTabLink) {
                                resultsTabLink.click();
                            } else {
                                tabContents.forEach(c => c.classList.remove('active'));
                                const resultsTab = document.getElementById('results');
                                if (resultsTab) {
                                    resultsTab.classList.add('active');
                                }
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching results:', error);
                        alert('Erreur lors de la récupération des résultats. Veuillez réessayer.');
                    });
                }, 1000); 
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erreur lors de l\'envoi des données. Veuillez réessayer.');
            });
        });
    }
});