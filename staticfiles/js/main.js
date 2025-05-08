document.addEventListener('DOMContentLoaded', function() {
    // ===== MOBILE MENU FUNCTIONALITY =====
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuButton && navLinks) {
        mobileMenuButton.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!navLinks.contains(event.target) && !mobileMenuButton.contains(event.target)) {
                navLinks.classList.remove('active');
            }
        });

        // Close menu when window is resized to desktop view
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                navLinks.classList.remove('active');
            }
        });
    }
    
    // ===== BABURNOMA TOOLTIP FUNCTIONALITY =====
    // Only initialize tooltip functionality if we're on the Baburnoma page
    if (document.querySelector('.baburnoma-text')) {
        // Cache for definitions to avoid repeated AJAX requests
        const definitionCache = {};
        
        // Create tooltip element
        const tooltip = document.createElement('div');
        tooltip.className = 'word-tooltip';
        tooltip.style.display = 'none';
        document.body.appendChild(tooltip);
        
        // Add event listeners to all dictionary words
        document.querySelectorAll('.dictionary-word').forEach(word => {
            word.addEventListener('mouseenter', showTooltip);
            word.addEventListener('mouseleave', hideTooltip);
            
            // For mobile support, add touch events
            word.addEventListener('touchstart', handleTouch);
        });
        
        // Handle touch events for mobile devices
        function handleTouch(event) {
            event.preventDefault();
            
            // If tooltip is already visible for this word, hide it (toggle behavior)
            if (tooltip.style.display === 'block' && 
                event.target.dataset.word === tooltip.dataset.currentWord) {
                hideTooltip();
                return;
            }
            
            // Otherwise show the tooltip
            showTooltip(event);
            
            // Hide tooltip when touching elsewhere
            const currentWord = event.target;
            const touchEndHandler = function(e) {
                if (!currentWord.contains(e.target) && !tooltip.contains(e.target)) {
                    hideTooltip();
                    document.removeEventListener('touchstart', touchEndHandler);
                }
            };
            
            document.addEventListener('touchstart', touchEndHandler);
        }
        
        // Show tooltip with definition
        function showTooltip(event) {
            const word = event.target.dataset.word;
            tooltip.dataset.currentWord = word;
            
            // Position tooltip near the word
            positionTooltip(event);
            
            // If definition is already cached, show it immediately
            if (definitionCache[word]) {
                tooltip.innerHTML = definitionCache[word];
                tooltip.style.display = 'block';
                return;
            }
            
            // Otherwise, show loading state and fetch definition
            tooltip.innerHTML = 'Yuklanyapti...';
            tooltip.style.display = 'block';
            
            // Fetch definition via AJAX
            fetch(`/get-word-definition/?word=${encodeURIComponent(word)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Word not found');
                    }
                    return response.json();
                })
                .then(data => {
                    // Cache and display the definition
                    const definitionHTML = `<strong>${data.word}</strong>: ${data.definition}`;
                    definitionCache[word] = definitionHTML;
                    
                    // Only update if mouse is still over the word
                    if (tooltip.style.display === 'block') {
                        tooltip.innerHTML = definitionHTML;
                    }
                })
                .catch(error => {
                    tooltip.innerHTML = 'Izohi topilmadi.';
                });
        }
        
        // Hide tooltip
        function hideTooltip() {
            tooltip.style.display = 'none';
        }
        
        // Position tooltip near word
        function positionTooltip(event) {
            const rect = event.target.getBoundingClientRect();
            const scrollTop = window.scrollY || document.documentElement.scrollTop;
            
            // Calculate position for tooltip (above the word)
            let tooltipTop = rect.top - tooltip.offsetHeight + scrollTop - 10;
            const tooltipLeft = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2);
            
            // Ensure tooltip stays within viewport
            if (tooltipTop < scrollTop) {
                // If not enough space above, place it below the word
                tooltipTop = rect.bottom + scrollTop + 10;
                tooltip.classList.add('tooltip-below');
            } else {
                tooltip.classList.remove('tooltip-below');
            }
            
            tooltip.style.top = tooltipTop + 'px';
            tooltip.style.left = tooltipLeft + 'px';
            
            // Ensure tooltip doesn't go off-screen horizontally
            const rightEdge = tooltipLeft + tooltip.offsetWidth;
            const viewportWidth = window.innerWidth;
            
            if (rightEdge > viewportWidth) {
                tooltip.style.left = (viewportWidth - tooltip.offsetWidth - 10) + 'px';
            } else if (tooltipLeft < 0) {
                tooltip.style.left = '10px';
            }
        }
    }
});