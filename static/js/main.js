document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recommend-form');
    const input = document.getElementById('movie-input');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.spinner');
    const searchBtn = document.getElementById('search-btn');
    
    const resultsWrapper = document.getElementById('results-wrapper');
    const grid = document.getElementById('recommendations-grid');
    const errorMsg = document.getElementById('error-message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const movie = input.value.trim();
        if(!movie) return;

        // UI Loading State
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        searchBtn.disabled = true;
        
        resultsWrapper.classList.add('hidden');
        errorMsg.classList.add('hidden');
        grid.innerHTML = '';

        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ movie })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch recommendations');
            }

            // Restore UI
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            searchBtn.disabled = false;

            renderRecommendations(data.recommendations);
            
        } catch (error) {
            console.error('Error:', error);
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            searchBtn.disabled = false;
            
            errorMsg.classList.remove('hidden');
        }
    });

    function renderRecommendations(movies) {
        movies.forEach((movie, index) => {
            const delay = index * 0.05; // Staggered animation delay
            
            const card = document.createElement('div');
            card.className = 'movie-card';
            card.style.animationDelay = `${delay}s`;

            card.innerHTML = `
                <div class="poster-wrapper">
                    <img src="${movie.poster}" alt="${movie.title} poster" loading="lazy">
                </div>
                <div class="card-content">
                    <h3 class="card-title">${movie.title}</h3>
                </div>
            `;
            grid.appendChild(card);
        });

        resultsWrapper.classList.remove('hidden');
    }
});
