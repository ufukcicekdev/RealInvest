// Real Estate Website Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // ===================================
    // Smooth Scrolling for Anchor Links
    // ===================================
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ===================================
    // Navbar Scroll Effect
    // ===================================
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // ===================================
    // Image Lazy Loading Fallback
    // ===================================
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // ===================================
    // Form Validation Enhancement
    // ===================================
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // ===================================
    // Auto-hide Alerts
    // ===================================
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // Auto-hide after 5 seconds
    });
    
    // ===================================
    // Property Card Favorite Toggle
    // ===================================
    const favoriteButtons = document.querySelectorAll('.btn-favorite');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const icon = this.querySelector('i');
            icon.classList.toggle('bi-heart');
            icon.classList.toggle('bi-heart-fill');
            
            // You can add AJAX call here to save to backend
            const propertyId = this.dataset.propertyId;
            console.log('Toggled favorite for property:', propertyId);
        });
    });
    
    // ===================================
    // Search Form Auto-submit on Filter Change
    // ===================================
    const filterSelects = document.querySelectorAll('select[name="type"], select[name="status"]');
    
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            // Optional: auto-submit form when filter changes
            // Uncomment below line if you want instant filtering
            // this.form.submit();
        });
    });
    
    // ===================================
    // Image Gallery Modal
    // ===================================
    const galleryImages = document.querySelectorAll('.gallery-item img');
    
    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            // You can implement a custom lightbox here
            console.log('Gallery image clicked:', this.src);
        });
    });
    
    // ===================================
    // Back to Top Button
    // ===================================
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary btn-back-to-top';
    backToTopButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        display: none;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        padding: 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    document.body.appendChild(backToTopButton);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // ===================================
    // Price Formatting
    // ===================================
    const priceElements = document.querySelectorAll('.price-format');
    
    priceElements.forEach(element => {
        const price = parseFloat(element.textContent.replace(/[^0-9.-]+/g, ''));
        if (!isNaN(price)) {
            element.textContent = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(price);
        }
    });
    
    // ===================================
    // Tooltip Initialization
    // ===================================
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // ===================================
    // Popover Initialization
    // ===================================
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // ===================================
    // Loading Spinner for AJAX Requests
    // ===================================
    function showLoadingSpinner() {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `;
        spinner.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 9999;
        `;
        document.body.appendChild(spinner);
    }
    
    function hideLoadingSpinner() {
        const spinner = document.querySelector('.loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    }
    
    // ===================================
    // Share Functionality
    // ===================================
    const shareButtons = document.querySelectorAll('.share-button');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            
            if (navigator.share) {
                try {
                    await navigator.share({
                        title: document.title,
                        url: window.location.href
                    });
                } catch (err) {
                    console.log('Error sharing:', err);
                }
            } else {
                // Fallback: copy to clipboard
                navigator.clipboard.writeText(window.location.href);
                alert('Link copied to clipboard!');
            }
        });
    });
    
    // ===================================
    // Custom Dropdown Functionality
    // ===================================
    const dropdowns = document.querySelectorAll('.dropdown-container');

    // Log the number of dropdowns found
    console.log('Found ' + dropdowns.length + ' dropdown containers');

    dropdowns.forEach((dropdown, index) => {
        const selected = dropdown.querySelector('.dropdown-selected');
        const options = dropdown.querySelectorAll('.dropdown-options li');
        const hiddenInput = dropdown.querySelector('input[type="hidden"]');
        const form = dropdown.closest('form'); // Get the parent form
        
        // Log dropdown information for debugging
        console.log('Initializing dropdown ' + (index + 1) + ':', dropdown);
        
        // Set initial selected value if exists
        const selectedOption = dropdown.querySelector('li[data-selected="true"]');
        if (selectedOption) {
            selected.textContent = selectedOption.textContent;
            hiddenInput.value = selectedOption.getAttribute('data-value');
            console.log('Set initial value for dropdown ' + (index + 1) + ':', selectedOption.textContent);
        }
        
        selected.addEventListener('click', () => {
            // Close all other dropdowns
            dropdowns.forEach(d => {
                if (d !== dropdown) {
                    d.classList.remove('active');
                }
            });
            
            // Toggle current dropdown
            dropdown.classList.toggle('active');
            console.log('Toggled dropdown ' + (index + 1) + ' active state');
        });
        
        options.forEach(option => {
            option.addEventListener('click', () => {
                selected.textContent = option.textContent;
                hiddenInput.value = option.getAttribute('data-value');
                dropdown.classList.remove('active');
                console.log('Selected option in dropdown ' + (index + 1) + ':', option.textContent);
                
                // Submit form automatically if it's a filter form
                if (form && form.id && (form.id.includes('filter') || form.id.includes('construction'))) {
                    console.log('Submitting filter form');
                    // Add a small delay to ensure the hidden input value is set before submitting
                    setTimeout(() => {
                        form.submit();
                    }, 100);
                }
            });
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown-container')) {
            dropdowns.forEach(dropdown => {
                if (dropdown.classList.contains('active')) {
                    dropdown.classList.remove('active');
                    console.log('Closed dropdown due to outside click');
                }
            });
        }
    });
    
    // ===================================
    // Simple Map Responsiveness Fix
    // ===================================
    function simpleMapFix() {
        const maps = document.querySelectorAll('.map-container iframe');
        maps.forEach(map => {
            map.style.width = '100%';
            map.style.height = '100%';
        });
    }
    
    // Apply on load and resize
    window.addEventListener('load', simpleMapFix);
    window.addEventListener('resize', simpleMapFix);
    
    // ===================================
    // Initialize Bootstrap Carousel for Banner
    // ===================================
    function initializeBannerCarousel() {
        const bannerCarousels = [
            'bannerCarousel1',
            'bannerCarousel2', 
            'bannerCarousel3',
            'bannerCarousel4'
        ];
        
        bannerCarousels.forEach(carouselId => {
            const bannerCarousel = document.getElementById(carouselId);
            if (bannerCarousel) {
                // Destroy existing carousel instance if it exists
                const carouselInstance = bootstrap.Carousel.getInstance(bannerCarousel);
                if (carouselInstance) {
                    carouselInstance.dispose();
                }
                
                // Initialize carousel with Bootstrap
                const carousel = new bootstrap.Carousel(bannerCarousel, {
                    interval: 5000,
                    pause: 'hover',
                    wrap: true
                });
                console.log('Banner carousel initialized:', carouselId);
            }
        });
    }

    // ===================================
    // Responsive Carousel Handling
    // ===================================
    function handleResponsiveCarousel() {
        const bannerCarousels = [
            'bannerCarousel1',
            'bannerCarousel2', 
            'bannerCarousel3',
            'bannerCarousel4'
        ];
        
        bannerCarousels.forEach(carouselId => {
            const bannerCarousel = document.getElementById(carouselId);
            if (bannerCarousel) {
                // Get current window width
                const windowWidth = window.innerWidth;
                
                // Adjust carousel settings based on screen size
                let interval = 5000;
                if (windowWidth < 768) {
                    interval = 7000; // Slower on mobile
                }
                
                // Reinitialize carousel with appropriate settings
                const carouselInstance = bootstrap.Carousel.getInstance(bannerCarousel);
                if (carouselInstance) {
                    carouselInstance.dispose();
                }
                
                const carousel = new bootstrap.Carousel(bannerCarousel, {
                    interval: interval,
                    pause: 'hover',
                    wrap: true
                });
                
                // Force image recalculation
                forceImageRecalculation(bannerCarousel);
            }
        });
    }

    // ===================================
    // Force Image Recalculation
    // ===================================
    function forceImageRecalculation(bannerCarousel) {
        if (bannerCarousel) {
            // Ensure images maintain proper aspect ratio
            const images = bannerCarousel.querySelectorAll('.hero-carousel-image');
            console.log('Found', images.length, 'hero carousel images in', bannerCarousel.id);
            images.forEach((img, index) => {
                console.log('Setting styles for image', index, img);
                img.style.objectFit = 'cover';
                img.style.objectPosition = 'center';
                img.style.width = '100%';
                img.style.height = '100vh';
                console.log('Applied styles to image', index, ':', img.style);
            });
        } else {
            console.log('No banner carousel provided to forceImageRecalculation');
        }
    }

    // ===================================
    // Force Carousel Recalculation
    // ===================================
    function forceCarouselRecalculation() {
        const bannerCarousels = [
            'bannerCarousel1',
            'bannerCarousel2', 
            'bannerCarousel3',
            'bannerCarousel4'
        ];
        
        bannerCarousels.forEach(carouselId => {
            const bannerCarousel = document.getElementById(carouselId);
            if (bannerCarousel) {
                console.log('Processing carousel:', carouselId);
                // Trigger a resize event to force recalculation
                const resizeEvent = new Event('resize');
                window.dispatchEvent(resizeEvent);
                
                // Also manually set the width and height
                const items = bannerCarousel.querySelectorAll('.carousel-item');
                console.log('Found', items.length, 'carousel items in', carouselId);
                items.forEach(item => {
                    item.style.width = '100%';
                    item.style.height = '100vh';
                });
                
                // Update the active item
                const activeItem = bannerCarousel.querySelector('.carousel-item.active');
                if (activeItem) {
                    activeItem.style.width = '100%';
                    activeItem.style.height = '100vh';
                }
                
                // Force image recalculation
                forceImageRecalculation(bannerCarousel);
            } else {
                console.log('Carousel not found:', carouselId);
            }
        });
    }

    // ===================================
    // Console Welcome Message
    // ===================================
    console.log('%c Real Estate Website ', 'background: #0d6efd; color: white; font-size: 20px; padding: 10px;');
    console.log('%c Built with Django & Bootstrap 5 ', 'color: #6c757d; font-size: 14px;');

    // Initialize components when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize banner carousel
        handleResponsiveCarousel();
        
        // Force recalculation after a short delay
        setTimeout(forceCarouselRecalculation, 100);
        
        // Reinitialize carousel on window resize
        let resizeTimeout;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(function() {
                handleResponsiveCarousel();
                forceCarouselRecalculation();
            }, 250); // Debounce resize events
        });
    });
    
    // Also initialize when window loads
    window.addEventListener('load', function() {
        handleResponsiveCarousel();
        forceCarouselRecalculation();
    });
});

// ===================================
// Utility Functions
// ===================================

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}