document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("global-search");
    const results = document.getElementById("search-results");

    if (searchInput && results) {
        searchInput.addEventListener("input", async () => {
            const query = searchInput.value.trim();

            if (query.length < 2) {
                results.innerHTML = "";
                return;
            }

            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                const data = await response.json();

                results.innerHTML = data.length
                    ? data.map(c => `
                        <a href="/characters/${c.id}" class="search-result">
                            <strong>${escapeHtml(c.name)}</strong>
                            <span>${escapeHtml(c.alias)}</span>
                        </a>
                    `).join("")
                    : `<div class="no-results">Nessun personaggio trovato.</div>`;
            } catch {
                results.innerHTML = `<div class="no-results">Errore nella ricerca.</div>`;
            }
        });
    }

    const filter = document.getElementById("character-filter");
    const cards = document.querySelectorAll("#character-grid .character-card");

    if (filter) {
        filter.addEventListener("input", () => {
            const query = filter.value.toLowerCase().trim();

            cards.forEach(card => {
                card.style.display = card.innerText.toLowerCase().includes(query)
                    ? ""
                    : "none";
            });
        });
    }
});

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
}
