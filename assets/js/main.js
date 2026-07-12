document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const toggleBtn = document.getElementById('mobileMenuToggle');
    const nav = document.getElementById('main-nav');
    
    if (toggleBtn && nav) {
        toggleBtn.addEventListener('click', () => {
            nav.classList.toggle('active');
        });
    }

    // Cookie Consent Banner
    const cookieBanner = document.getElementById('cookieConsent');
    const acceptBtn = document.getElementById('acceptCookies');
    
    if (cookieBanner && acceptBtn) {
        if (!localStorage.getItem('cookieConsent')) {
            // Slight delay before showing
            setTimeout(() => {
                cookieBanner.classList.add('show');
            }, 1000);
        }
        
        acceptBtn.addEventListener('click', () => {
            localStorage.setItem('cookieConsent', 'true');
            cookieBanner.classList.remove('show');
        });
    }

    // Client-side Search functionality
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (searchInput && searchResults) {
        let searchIndex = null;
        
        // Fetch index on focus
        searchInput.addEventListener('focus', () => {
            if (!searchIndex) {
                fetch('/search_index.json')
                    .then(response => response.json())
                    .then(data => { searchIndex = data; })
                    .catch(err => console.error("Error loading search index", err));
            }
        });

        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            searchResults.innerHTML = '';
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            if (!searchIndex) return;
            
            const results = searchIndex.filter(item => 
                item.title.toLowerCase().includes(query) || 
                item.description.toLowerCase().includes(query)
            ).slice(0, 5); // top 5
            
            if (results.length > 0) {
                results.forEach(result => {
                    const a = document.createElement('a');
                    a.href = result.url;
                    a.innerHTML = `<strong>${result.title}</strong><br><small>${result.category}</small>`;
                    searchResults.appendChild(a);
                });
                searchResults.style.display = 'block';
            } else {
                searchResults.innerHTML = '<div style="padding: 10px; color: #666;">No results found</div>';
                searchResults.style.display = 'block';
            }
        });
        
        // Hide search results when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.header-search')) {
                searchResults.style.display = 'none';
            }
        });
    }
});
