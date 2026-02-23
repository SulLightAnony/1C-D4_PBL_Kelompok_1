// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize card animations
    initCardAnimations();
    
    // Add interactive effects
    initHoverEffects();
});

// Animate cards on scroll/load
function initCardAnimations() {
    const cards = document.querySelectorAll('.member-card');
    
    // Use Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add delay based on card index
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    cards.forEach(card => {
        observer.observe(card);
    });
}

// Add hover effects and interactivity
function initHoverEffects() {
    const cards = document.querySelectorAll('.member-card');
    
    cards.forEach(card => {
        // Mouse move parallax effect on cards
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px) scale(1.02)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0) scale(1)';
        });
    });
}

// Emoji click effect (fun easter egg)
document.querySelectorAll('.floating-emoji').forEach(emoji => {
    emoji.addEventListener('click', () => {
        emoji.style.transform = 'scale(2)';
        emoji.style.opacity = '1';
        setTimeout(() => {
            emoji.style.transform = '';
            emoji.style.opacity = '';
        }, 300);
    });
});

// Console easter egg
console.log('%c🔥 Meet The Squad! 🔥', 'font-size: 24px; color: #ff6b35; font-weight: bold;');
console.log('%cBuilt with 💜 by the team', 'font-size: 14px; color: #1e90ff;');
