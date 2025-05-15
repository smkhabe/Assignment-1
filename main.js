// Enable smooth scrolling for anchor links (e.g., "#section1")
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Prompt a confirmation dialog before any form is submitted
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!confirm('Are you sure you want to submit this form?')) {
            e.preventDefault();
        }
    });
});

// Initialize Bootstrap tooltips for elements that use the data-bs-toggle attribute
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Add a fade-in animation to .card elements when they enter the viewport
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1 // Trigger when 10% of the element is visible
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate__animated', 'animate__fadeIn');
            observer.unobserve(entry.target); // Remove observer after animation is applied
        }
    });
}, observerOptions);

// Apply the observer to all elements with the .card class
document.querySelectorAll('.card').forEach(card => {
    observer.observe(card);
});

// Automatically format number inputs (with step="0.01") to 2 decimal places
document.querySelectorAll('input[type="number"][step="0.01"]').forEach(input => {
    input.addEventListener('input', function(e) {
        let value = e.target.value;
        if (value) {
            value = parseFloat(value).toFixed(2);
            e.target.value = value;
        }
    });
});

// Add basic form validation: mark empty required fields and block submission
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        let isValid = true;
        form.querySelectorAll('input[required], select[required], textarea[required]').forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid'); // Highlight invalid field
            } else {
                input.classList.remove('is-invalid');
            }
        });

        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });
});
