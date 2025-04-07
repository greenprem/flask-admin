$(document).ready(function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-close alerts after 5 seconds
    $('.alert').not('.alert-permanent').delay(5000).fadeOut(500);
    
    // Add confirmation for delete buttons
    $('.btn-delete').click(function(e) {
        if (!confirm('Are you sure you want to delete this record?')) {
            e.preventDefault();
            return false;
        }
    });
    
    // Make table rows clickable to view details
    $('.table-clickable tbody tr').click(function() {
        window.location = $(this).data('url');
    });
    
    // Handle search form in the list view
    $('#search-form').submit(function(e) {
        e.preventDefault();
        const searchQuery = $('#search-input').val();
        window.location.href = $(this).attr('action') + '?search=' + encodeURIComponent(searchQuery);
    });
    
    // Toggle filter panel
    $('#toggle-filters').click(function() {
        $('#filter-panel').toggleClass('d-none');
    });
    
    // Enhance select controls with searchable options
    $('.select-searchable').select2({
        theme: 'bootstrap-5',
        dropdownParent: $('body')
    });
    
    // Handle related model lookups
    $('.model-lookup').click(function() {
        const target = $(this).data('target');
        const url = $(this).data('url');
        // Open modal with AJAX content
        $('#modal-lookup .modal-body').load(url, function() {
            $('#modal-lookup').modal('show');
        });
    });
    
    // Enhance date/time inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (input.type !== 'date') {
            // Fallback for browsers not supporting date input
            $(input).datepicker({
                format: 'yyyy-mm-dd',
                autoclose: true
            });
        }
    });
    
    // Enhance datetime inputs
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    datetimeInputs.forEach(input => {
        if (input.type !== 'datetime-local') {
            // Fallback for browsers not supporting datetime-local input
            $(input).datetimepicker({
                format: 'YYYY-MM-DD HH:mm',
                icons: {
                    time: 'fas fa-clock',
                    date: 'fas fa-calendar',
                    up: 'fas fa-chevron-up',
                    down: 'fas fa-chevron-down',
                    previous: 'fas fa-chevron-left',
                    next: 'fas fa-chevron-right',
                    today: 'fas fa-calendar-check',
                    clear: 'fas fa-trash',
                    close: 'fas fa-times'
                }
            });
        }
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});
