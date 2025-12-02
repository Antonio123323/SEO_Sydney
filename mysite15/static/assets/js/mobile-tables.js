// Mobile Tables JavaScript - Enhanced scrolling functionality

document.addEventListener('DOMContentLoaded', function() {
    // Find all scrollable table containers
    const tableContainers = document.querySelectorAll('.overflow-x-auto');
    
    // Function to handle scroll indicator visibility
    function updateScrollIndicator(container) {
        const isAtEnd = container.scrollLeft >= (container.scrollWidth - container.clientWidth - 10);
        
        if (isAtEnd) {
            container.classList.add('scrolled-right');
        } else {
            container.classList.remove('scrolled-right');
        }
    }
    
    // Function to add touch-friendly scroll behavior
    function addTouchScrolling(container) {
        let isScrolling = false;
        let startX = 0;
        let scrollLeft = 0;
        
        // Touch start
        container.addEventListener('touchstart', function(e) {
            isScrolling = true;
            startX = e.touches[0].pageX - container.offsetLeft;
            scrollLeft = container.scrollLeft;
            container.style.cursor = 'grabbing';
        });
        
        // Touch move
        container.addEventListener('touchmove', function(e) {
            if (!isScrolling) return;
            e.preventDefault();
            
            const x = e.touches[0].pageX - container.offsetLeft;
            const walk = (x - startX) * 2; // Multiply for faster scrolling
            container.scrollLeft = scrollLeft - walk;
        });
        
        // Touch end
        container.addEventListener('touchend', function() {
            isScrolling = false;
            container.style.cursor = 'grab';
        });
        
        // Mouse events for desktop
        container.addEventListener('mousedown', function(e) {
            isScrolling = true;
            startX = e.pageX - container.offsetLeft;
            scrollLeft = container.scrollLeft;
            container.style.cursor = 'grabbing';
        });
        
        container.addEventListener('mouseleave', function() {
            isScrolling = false;
            container.style.cursor = 'grab';
        });
        
        container.addEventListener('mouseup', function() {
            isScrolling = false;
            container.style.cursor = 'grab';
        });
        
        container.addEventListener('mousemove', function(e) {
            if (!isScrolling) return;
            e.preventDefault();
            
            const x = e.pageX - container.offsetLeft;
            const walk = (x - startX) * 2;
            container.scrollLeft = scrollLeft - walk;
        });
    }
    
    // Initialize all table containers
    tableContainers.forEach(function(container) {
        // Set initial cursor style
        container.style.cursor = 'grab';
        
        // Add scroll event listener for indicator
        container.addEventListener('scroll', function() {
            updateScrollIndicator(container);
        });
        
        // Add touch scrolling
        addTouchScrolling(container);
        
        // Initial check for scroll indicator
        updateScrollIndicator(container);
        
        // Make container focusable for keyboard navigation
        if (!container.hasAttribute('tabindex')) {
            container.setAttribute('tabindex', '0');
        }
        
        // Add keyboard scroll support
        container.addEventListener('keydown', function(e) {
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    container.scrollLeft -= 50;
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    container.scrollLeft += 50;
                    break;
                case 'Home':
                    e.preventDefault();
                    container.scrollLeft = 0;
                    break;
                case 'End':
                    e.preventDefault();
                    container.scrollLeft = container.scrollWidth;
                    break;
            }
        });
    });
    
    // Add scroll buttons for better UX on mobile
    function addScrollButtons(container) {
        // Only add if container is actually scrollable
        if (container.scrollWidth <= container.clientWidth) return;
        
        const wrapper = document.createElement('div');
        wrapper.className = 'table-scroll-wrapper relative';
        
        // Left scroll button
        const leftBtn = document.createElement('button');
        leftBtn.innerHTML = '‹';
        leftBtn.className = 'table-scroll-btn table-scroll-left absolute left-2 top-1/2 transform -translate-y-1/2 bg-[#66A9D9] text-white w-8 h-8 rounded-full z-10 flex items-center justify-center text-lg font-bold opacity-70 hover:opacity-100 transition-opacity';
        leftBtn.style.display = 'none';
        
        // Right scroll button
        const rightBtn = document.createElement('button');
        rightBtn.innerHTML = '›';
        rightBtn.className = 'table-scroll-btn table-scroll-right absolute right-2 top-1/2 transform -translate-y-1/2 bg-[#66A9D9] text-white w-8 h-8 rounded-full z-10 flex items-center justify-center text-lg font-bold opacity-70 hover:opacity-100 transition-opacity';
        
        // Wrap container
        container.parentNode.insertBefore(wrapper, container);
        wrapper.appendChild(container);
        wrapper.appendChild(leftBtn);
        wrapper.appendChild(rightBtn);
        
        // Button functionality
        leftBtn.addEventListener('click', function(e) {
            e.preventDefault();
            container.scrollLeft -= 150;
        });
        
        rightBtn.addEventListener('click', function(e) {
            e.preventDefault();
            container.scrollLeft += 150;
        });
        
        // Update button visibility
        function updateButtons() {
            const isAtStart = container.scrollLeft <= 10;
            const isAtEnd = container.scrollLeft >= (container.scrollWidth - container.clientWidth - 10);
            
            leftBtn.style.display = isAtStart ? 'none' : 'flex';
            rightBtn.style.display = isAtEnd ? 'none' : 'flex';
        }
        
        container.addEventListener('scroll', updateButtons);
        updateButtons(); // Initial check
    }
    
    // Add scroll buttons on mobile only
    if (window.innerWidth <= 768) {
        tableContainers.forEach(addScrollButtons);
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        tableContainers.forEach(function(container) {
            updateScrollIndicator(container);
        });
    });
});
