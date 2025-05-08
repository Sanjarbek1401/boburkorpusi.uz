document.addEventListener('DOMContentLoaded', function() {
    const tooltipElements = document.querySelectorAll('.dictionary-word');
    let activeTooltip = null;
    
    function createTooltip(element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = element.getAttribute('data-definition');
        document.body.appendChild(tooltip);
        return tooltip;
    }
    
    function positionTooltip(tooltip, element) {
        const rect = element.getBoundingClientRect();
        const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Position tooltip
        tooltip.style.left = (rect.left + scrollLeft) + 'px';
        tooltip.style.top = (rect.bottom + scrollTop + 5) + 'px';
        
        // Check if tooltip would go off screen
        const tooltipRect = tooltip.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        
        // Adjust horizontal position if needed
        if (tooltipRect.right > viewportWidth) {
            tooltip.style.left = (viewportWidth - tooltipRect.width - 10) + 'px';
        }
        
        // Adjust vertical position if needed
        if (tooltipRect.bottom > viewportHeight) {
            tooltip.style.top = (rect.top + scrollTop - tooltipRect.height - 5) + 'px';
            tooltip.style.transform = 'translateY(0)';
        }
    }
    
    function showTooltip(element) {
        if (activeTooltip) {
            activeTooltip.remove();
        }
        
        const tooltip = createTooltip(element);
        positionTooltip(tooltip, element);
        
        // Show tooltip with animation
        requestAnimationFrame(() => {
            tooltip.style.display = 'block';
            requestAnimationFrame(() => {
                tooltip.classList.add('visible');
            });
        });
        
        activeTooltip = tooltip;
    }
    
    function hideTooltip() {
        if (activeTooltip) {
            activeTooltip.classList.remove('visible');
            setTimeout(() => {
                if (activeTooltip && activeTooltip.parentNode) {
                    activeTooltip.remove();
                }
                activeTooltip = null;
            }, 200); // Match this with CSS transition duration
        }
    }
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', () => showTooltip(element));
        element.addEventListener('mouseleave', hideTooltip);
    });
    
    // Handle window resize and scroll
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            if (activeTooltip) {
                const element = document.querySelector('.dictionary-word:hover');
                if (element) {
                    positionTooltip(activeTooltip, element);
                }
            }
        }, 100);
    });
    
    window.addEventListener('scroll', () => {
        if (activeTooltip) {
            const element = document.querySelector('.dictionary-word:hover');
            if (element) {
                positionTooltip(activeTooltip, element);
            }
        }
    });
}); 