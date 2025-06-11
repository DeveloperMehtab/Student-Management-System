// Custom JavaScript for Student Management System

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Password strength meter
    const passwordField = document.querySelector('#id_password1');
    if (passwordField) {
        const strengthMeter = document.createElement('div');
        strengthMeter.className = 'progress mt-2';
        strengthMeter.innerHTML = '<div class="progress-bar" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>';
        
        const strengthText = document.createElement('small');
        strengthText.className = 'form-text text-muted mt-1';
        strengthText.textContent = 'Password strength: Too weak';
        
        passwordField.parentNode.insertBefore(strengthMeter, passwordField.nextSibling);
        passwordField.parentNode.insertBefore(strengthText, strengthMeter.nextSibling);
        
        passwordField.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            if (password.length >= 8) strength += 25;
            if (password.match(/[a-z]+/)) strength += 25;
            if (password.match(/[A-Z]+/)) strength += 25;
            if (password.match(/[0-9]+/)) strength += 25;
            
            const progressBar = strengthMeter.querySelector('.progress-bar');
            progressBar.style.width = strength + '%';
            progressBar.setAttribute('aria-valuenow', strength);
            
            if (strength < 25) {
                progressBar.className = 'progress-bar bg-danger';
                strengthText.textContent = 'Password strength: Too weak';
            } else if (strength < 50) {
                progressBar.className = 'progress-bar bg-warning';
                strengthText.textContent = 'Password strength: Weak';
            } else if (strength < 75) {
                progressBar.className = 'progress-bar bg-info';
                strengthText.textContent = 'Password strength: Medium';
            } else {
                progressBar.className = 'progress-bar bg-success';
                strengthText.textContent = 'Password strength: Strong';
            }
        });
    }
}); 