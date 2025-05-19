/**
 * Main JavaScript file containing UI enhancements and interactions
 * @module main
 */

// Configuration constants
const CONFIG = {
    SCROLL: {
        BEHAVIOR: 'smooth',
        THRESHOLD: 0.1,
        ROOT_MARGIN: '0px'
    },
    ANIMATION: {
        CLASSES: ['animate__animated', 'animate__fadeIn']
    }
};

/**
 * Initialize smooth scrolling for anchor links
 */
const initSmoothScroll = () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = anchor.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: CONFIG.SCROLL.BEHAVIOR
                });
            }
        });
    });
};

/**
 * Initialize form submission confirmation
 */
const initFormConfirmation = () => {
    document.addEventListener('submit', (e) => {
        if (e.target.tagName === 'FORM') {
            if (!confirm('Are you sure you want to submit this form?')) {
                e.preventDefault();
            }
        }
    }, true);
};

/**
 * Initialize Bootstrap tooltips
 */
const initTooltips = () => {
    try {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        [...tooltipTriggerList].forEach(tooltipTriggerEl => {
            new bootstrap.Tooltip(tooltipTriggerEl);
        });
    } catch (error) {
        console.warn('Bootstrap tooltips initialization failed:', error);
    }
};

/**
 * Initialize intersection observer for card animations
 */
const initCardAnimations = () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add(...CONFIG.ANIMATION.CLASSES);
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: CONFIG.SCROLL.ROOT_MARGIN,
        threshold: CONFIG.SCROLL.THRESHOLD
    });

    document.querySelectorAll('.card').forEach(card => observer.observe(card));
};

/**
 * Initialize number input formatting
 */
const initNumberInputFormatting = () => {
    document.addEventListener('input', (e) => {
        if (e.target.matches('input[type="number"][step="0.01"]')) {
            const value = e.target.value;
            if (value) {
                try {
                    e.target.value = Number(value).toFixed(2);
                } catch (error) {
                    console.warn('Number formatting failed:', error);
                }
            }
        }
    });
};

/**
 * Initialize all UI enhancements
 */
const initUI = () => {
    initSmoothScroll();
    initFormConfirmation();
    initTooltips();
    initCardAnimations();
    initNumberInputFormatting();
};

// Initialize everything when the DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUI);
} else {
    initUI();
}
