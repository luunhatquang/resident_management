/**
 * BUILDING MANAGEMENT - JavaScript
 */

/**
 * Apply filters - Redirect with query params
 */
function applyFilters() {
    const statusFilter = document.getElementById('filter-status').value;
    const searchText = document.getElementById('search-input').value.trim();
    
    // Build URL with query params
    const params = new URLSearchParams();
    
    if (statusFilter) params.set('status', statusFilter);
    if (searchText) params.set('search', searchText);


    
    // Redirect
    const url = params.toString() ? `?${params.toString()}` : window.location.pathname;
    window.location.href = url;
}

/**
 * Clear all filters
 */
function clearFilters() {
    window.location.href = window.location.pathname;
}

/**
 * View building detail
 */
function viewBuilding(buildingId) {
    window.location.href = `/buildings/detail/${buildingId}/`;
}

/**
 * Edit Building
 */
function editBuilding(buildingId) {
    window.location.href = `/buildings/${buildingId}/update/`;
}

/**
 * Open Add Building Modal/Page
 */
function openAddModal() {
    window.location.href = '/buildings/create';
}

/**
 * View room detail
 */
function viewRoom(roomId) {
    window.location.href = `/rooms/detail/${roomId}/`;
}

/**
 * Edit Room
 */
function editRoom(roomId) {
    window.location.href = `/rooms/${roomId}/update/`;
}

/**
 * Filter rooms by status in building detail page
 */
function filterRooms(status) {
    const rows = document.querySelectorAll('.room-row');
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    // Update active button
    filterBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Filter rows
    rows.forEach(row => {
        if (status === 'all') {
            row.style.display = '';
        } else {
            const rowStatus = row.getAttribute('data-status');
            row.style.display = rowStatus === status ? '' : 'none';
        }
    });
}

// ========== UTILITY FUNCTIONS ==========

/**
 * Format date to Vietnamese format
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN');
}

/**
 * Format currency to Vietnamese format
 */
function formatCurrency(amount) {
    if (!amount) return '0 ₫';
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

/**
 * Get CSRF token for Django
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Initialize form controls
 * Add form-control class to all form fields
 */
function initFormControls() {
    const inputs = document.querySelectorAll('input[type="text"], input[type="number"], textarea, select');
    inputs.forEach(input => {
        input.classList.add('form-control');
    });
}

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', initFormControls);

