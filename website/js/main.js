// Navigation Menu Toggle
function showMenu() {
    document.getElementById('navLinks').classList.add('active');
}

function hideMenu() {
    document.getElementById('navLinks').classList.remove('active');
}

// Copy Token Address
function copyAddress() {
    const tokenAddress = document.getElementById('tokenAddress').textContent;
    navigator.clipboard.writeText(tokenAddress).then(() => {
        // Show a tooltip or notification
        alert('Token address copied to clipboard!');
    }).catch(err => {
        console.error('Could not copy text: ', err);
    });
}

// Scroll Animation
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Price Chart
    initPriceChart();

    // Setup chart timeframe buttons
    setupChartButtons();

    // Initialize Countdown Timer
    initCountdown();

    // Add smooth scrolling to all links
    const links = document.querySelectorAll('a[href^="#"]');

    for (const link of links) {
        link.addEventListener('click', function(e) {
            if (this.hash !== '') {
                e.preventDefault();

                const hash = this.hash;

                // Smooth scroll to the target
                document.querySelector(hash).scrollIntoView({
                    behavior: 'smooth'
                });

                // Close mobile menu if open
                if (document.getElementById('navLinks').classList.contains('active')) {
                    hideMenu();
                }
            }
        });
    }

    // Navbar background change on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.padding = '15px 0';
            navbar.style.backgroundColor = 'rgba(18, 18, 18, 0.95)';
        } else {
            navbar.style.padding = '20px 0';
            navbar.style.backgroundColor = 'rgba(18, 18, 18, 0.9)';
        }
    });
});

// Initialize Price Chart
function initPriceChart() {
    const ctx = document.getElementById('priceChart').getContext('2d');

    // Sample data - in a real implementation, this would come from an API
    const labels = generateDateLabels(24);
    const data = generateRandomPriceData(24, 0.00011, 0.00013);

    // Create gradient for chart background
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(0, 255, 255, 0.5)');
    gradient.addColorStop(1, 'rgba(0, 255, 255, 0)');

    // Create the chart
    window.priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'NeonX Price',
                data: data,
                borderColor: '#00ffff',
                borderWidth: 2,
                pointBackgroundColor: '#00ffff',
                pointBorderColor: '#00ffff',
                pointRadius: 0,
                pointHoverRadius: 4,
                tension: 0.4,
                fill: true,
                backgroundColor: gradient
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    titleColor: '#00ffff',
                    bodyColor: '#ffffff',
                    borderColor: '#00ffff',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            return `Price: $${context.raw.toFixed(8)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        maxRotation: 0,
                        maxTicksLimit: 8
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        callback: function(value) {
                            return '$' + value.toFixed(8);
                        }
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            hover: {
                mode: 'index',
                intersect: false
            }
        }
    });
}

// Setup Chart Timeframe Buttons
function setupChartButtons() {
    const buttons = document.querySelectorAll('.chart-btn');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            buttons.forEach(btn => btn.classList.remove('active'));

            // Add active class to clicked button
            this.classList.add('active');

            // Get timeframe from data attribute
            const timeframe = this.getAttribute('data-timeframe');

            // Update chart data based on timeframe
            updateChartData(timeframe);
        });
    });
}

// Update Chart Data based on timeframe
function updateChartData(timeframe) {
    let points;
    let minPrice;
    let maxPrice;

    // Set data points and price range based on timeframe
    switch(timeframe) {
        case '24h':
            points = 24;
            minPrice = 0.00011;
            maxPrice = 0.00013;
            break;
        case '7d':
            points = 7 * 24;
            minPrice = 0.00010;
            maxPrice = 0.00014;
            break;
        case '30d':
            points = 30 * 24;
            minPrice = 0.00009;
            maxPrice = 0.00015;
            break;
        case 'all':
            points = 90 * 24;
            minPrice = 0.00005;
            maxPrice = 0.00015;
            break;
        default:
            points = 24;
            minPrice = 0.00011;
            maxPrice = 0.00013;
    }

    // Generate new data
    const labels = generateDateLabels(points);
    const data = generateRandomPriceData(points, minPrice, maxPrice);

    // Update chart data
    window.priceChart.data.labels = labels;
    window.priceChart.data.datasets[0].data = data;
    window.priceChart.update();

    // Update price info
    updatePriceInfo(data);
}

// Generate date labels for chart
function generateDateLabels(count) {
    const labels = [];
    const now = new Date();

    for (let i = count - 1; i >= 0; i--) {
        const date = new Date(now.getTime() - i * 3600000); // 1 hour intervals
        let label;

        if (count <= 24) {
            // For 24h view, show hours
            label = date.getHours() + ':00';
        } else if (count <= 7 * 24) {
            // For 7d view, show days and hours
            label = (date.getMonth() + 1) + '/' + date.getDate() + ' ' + date.getHours() + ':00';
        } else {
            // For longer periods, show only days
            if (date.getHours() === 0) {
                label = (date.getMonth() + 1) + '/' + date.getDate();
            } else {
                label = '';
            }
        }

        labels.push(label);
    }

    return labels;
}

// Generate random price data for chart
function generateRandomPriceData(count, min, max) {
    const data = [];
    let price = (min + max) / 2; // Start at middle price

    for (let i = 0; i < count; i++) {
        // Random walk with trend
        const change = (Math.random() - 0.5) * 0.00001;
        price += change;

        // Keep price within bounds
        if (price < min) price = min + Math.random() * 0.000005;
        if (price > max) price = max - Math.random() * 0.000005;

        data.push(price);
    }

    // Update price info with the generated data
    updatePriceInfo(data);

    return data;
}

// Update price information display
function updatePriceInfo(data) {
    const currentPrice = data[data.length - 1];
    const previousPrice = data[data.length - 2];
    const priceChange = ((currentPrice - previousPrice) / previousPrice) * 100;

    // Find high and low
    const high = Math.max(...data);
    const low = Math.min(...data);

    // Update DOM elements
    document.getElementById('live-price').textContent = '$' + currentPrice.toFixed(8);

    const priceChangeElement = document.getElementById('price-change');
    priceChangeElement.textContent = (priceChange >= 0 ? '+' : '') + priceChange.toFixed(2) + '%';

    if (priceChange >= 0) {
        priceChangeElement.className = 'price-up';
    } else {
        priceChangeElement.className = 'price-down';
    }

    document.getElementById('price-high').textContent = '$' + high.toFixed(8);
    document.getElementById('price-low').textContent = '$' + low.toFixed(8);

    // Update the stats bar as well
    document.getElementById('currentPrice').textContent = '$' + currentPrice.toFixed(8);
}

// Initialize Countdown Timer
function initCountdown() {
    // Set the target date (30 days from now for example)
    const now = new Date();
    const targetDate = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000); // 30 days from now

    // Update the countdown every second
    updateCountdown(targetDate);
    setInterval(function() {
        updateCountdown(targetDate);
    }, 1000);
}

// Update Countdown Timer
function updateCountdown(targetDate) {
    const now = new Date();
    const difference = targetDate - now;

    // If the countdown is over
    if (difference <= 0) {
        document.getElementById('countdown-days').textContent = '00';
        document.getElementById('countdown-hours').textContent = '00';
        document.getElementById('countdown-minutes').textContent = '00';
        document.getElementById('countdown-seconds').textContent = '00';
        return;
    }

    // Calculate time units
    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);

    // Add leading zeros if needed
    const formatNumber = (num) => num < 10 ? `0${num}` : num;

    // Update the DOM elements
    document.getElementById('countdown-days').textContent = formatNumber(days);
    document.getElementById('countdown-hours').textContent = formatNumber(hours);
    document.getElementById('countdown-minutes').textContent = formatNumber(minutes);
    document.getElementById('countdown-seconds').textContent = formatNumber(seconds);
}