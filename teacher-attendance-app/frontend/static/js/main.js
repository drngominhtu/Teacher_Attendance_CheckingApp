document.addEventListener('DOMContentLoaded', function() {
    console.log('Teacher Attendance App loaded successfully!');
    
    // Set active navigation item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            // Open parent dropdown if this is a dropdown item
            const parentDropdown = link.closest('.has-dropdown');
            if (parentDropdown) {
                parentDropdown.classList.add('open');
            }
        }
    });
    
    // Handle dropdown menu clicks
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const parentLi = this.closest('.has-dropdown');
            const isOpen = parentLi.classList.contains('open');
            
            // Close all other dropdowns
            document.querySelectorAll('.has-dropdown').forEach(dropdown => {
                dropdown.classList.remove('open');
            });
            
            // Toggle current dropdown
            if (!isOpen) {
                parentLi.classList.add('open');
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.sidebar-nav')) {
            document.querySelectorAll('.has-dropdown').forEach(dropdown => {
                dropdown.classList.remove('open');
            });
        }
    });
});

// Global helper functions
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        z-index: 9999;
        max-width: 400px;
        color: white;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    `;
    
    if (type === 'success') {
        alertDiv.style.backgroundColor = '#27ae60';
    } else if (type === 'error') {
        alertDiv.style.backgroundColor = '#e74c3c';
    } else {
        alertDiv.style.backgroundColor = '#3498db';
    }
    
    alertDiv.textContent = message;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        if (document.body.contains(alertDiv)) {
            alertDiv.style.opacity = '0';
            setTimeout(() => {
                if (document.body.contains(alertDiv)) {
                    document.body.removeChild(alertDiv);
                }
            }, 300);
        }
    }, 3000);
}

function confirmDelete(message) {
    return confirm(message || 'Bạn có chắc chắn muốn xóa?');
}

// Modal functions
function closeEditModal() {
    const modal = document.getElementById('edit-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    const modal = document.getElementById('edit-modal');
    if (modal && event.target === modal) {
        closeEditModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeEditModal();
    }
});