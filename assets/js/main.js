/**
 * NeonX Website Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS (Animate On Scroll)
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });

    // Navbar scroll behavior
    const navbar = document.querySelector('.navbar');
    const backToTop = document.querySelector('.back-to-top');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
            backToTop.classList.add('active');
        } else {
            navbar.classList.remove('scrolled');
            backToTop.classList.remove('active');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            if (this.getAttribute('href') !== '#') {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    const navbarHeight = document.querySelector('.navbar').offsetHeight;
                    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                    
                    // Update active nav link
                    document.querySelectorAll('.navbar .nav-link').forEach(link => {
                        link.classList.remove('active');
                    });
                    this.classList.add('active');
                    
                    // Close mobile menu if open
                    const navbarCollapse = document.querySelector('.navbar-collapse');
                    if (navbarCollapse.classList.contains('show')) {
                        document.querySelector('.navbar-toggler').click();
                    }
                }
            }
        });
    });

    // Update active nav link on scroll
    window.addEventListener('scroll', function() {
        let current = '';
        const sections = document.querySelectorAll('section');
        const navHeight = document.querySelector('.navbar').offsetHeight;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - navHeight - 100;
            const sectionHeight = section.offsetHeight;
            
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        document.querySelectorAll('.navbar .nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    // Mobile menu behavior
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navbarLinks.forEach(link => {
        link.addEventListener('click', () => {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });

    // Initialize Tokenomics Chart
    const tokenomicsChart = document.getElementById('tokenomicsChart');
    if (tokenomicsChart) {
        new Chart(tokenomicsChart, {
            type: 'doughnut',
            data: {
                labels: ['Public Sale', 'Liquidity Pool', 'Marketing', 'Team', 'Ecosystem Growth'],
                datasets: [{
                    data: [50, 20, 15, 10, 5],
                    backgroundColor: [
                        '#ff00ff', // Neon Pink
                        '#00ffff', // Neon Cyan
                        '#ffff00', // Neon Yellow
                        '#00ff00', // Neon Green
                        '#ff0099'  // Neon Magenta
                    ],
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.formattedValue || '';
                                return `${label}: ${value}% (${(context.raw * 10).toLocaleString()} million NEONX)`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }

    // Copy token address to clipboard
    document.querySelectorAll('.token-address').forEach(element => {
        element.addEventListener('click', function() {
            const textToCopy = this.textContent;
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Create and show tooltip
                const tooltip = document.createElement('div');
                tooltip.className = 'copy-tooltip';
                tooltip.textContent = 'Copied!';
                tooltip.style.position = 'absolute';
                tooltip.style.backgroundColor = '#ff00ff';
                tooltip.style.color = 'white';
                tooltip.style.padding = '5px 10px';
                tooltip.style.borderRadius = '4px';
                tooltip.style.fontSize = '12px';
                tooltip.style.zIndex = '1000';
                tooltip.style.opacity = '0';
                tooltip.style.transition = 'opacity 0.3s ease';
                
                // Position the tooltip
                const rect = this.getBoundingClientRect();
                tooltip.style.top = `${rect.top - 30 + window.scrollY}px`;
                tooltip.style.left = `${rect.left + rect.width / 2}px`;
                tooltip.style.transform = 'translateX(-50%)';
                
                // Add to DOM and animate
                document.body.appendChild(tooltip);
                setTimeout(() => {
                    tooltip.style.opacity = '1';
                }, 10);
                
                // Remove after delay
                setTimeout(() => {
                    tooltip.style.opacity = '0';
                    setTimeout(() => {
                        document.body.removeChild(tooltip);
                    }, 300);
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
            });
        });
    });

    // Neon glow effect on hover for buttons and cards
    const glowElements = document.querySelectorAll('.btn, .feature-card, .community-link');
    
    glowElements.forEach(element => {
        element.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            this.style.setProperty('--x-pos', `${x}px`);
            this.style.setProperty('--y-pos', `${y}px`);
        });
    });

    // Preload images for better performance
    function preloadImages() {
        const images = [
            'assets/images/neonx-logo.svg',
            'assets/images/neonx-hero.png',
            'assets/images/neonx-about.png',
            'assets/images/phantom-logo.png',
            'assets/images/solflare-logo.png',
            'assets/images/raydium-logo.png',
            'assets/images/jupiter-logo.png'
        ];
        
        images.forEach(src => {
            const img = new Image();
            img.src = src;
        });
    }
    
    preloadImages();
});
