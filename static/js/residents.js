/**
 * RESIDENTS MANAGEMENT - JavaScript
 * Data được render từ Django Backend
 */

/**
 * Toggle Advanced Filters
 */
function toggleFilters() {
    const filterDiv = document.getElementById('advanced-filters');
    filterDiv.style.display = filterDiv.style.display === 'none' ? 'block' : 'none';
}

/**
 * Apply filters - Redirect với query params
 */
function applyFilters() {
    const searchText = document.getElementById('search-input').value.trim();
    const statusFilter = document.getElementById('status-filter').value.trim();
    
    // Build URL với query params
    const params = new URLSearchParams();
    
    if (searchText) params.set('search', searchText);
    if (statusFilter) params.set('status', statusFilter);
    
    // Redirect
    const url = params.toString() ? `?${params.toString()}` : window.location.pathname;
    window.location.href = url;
}

/**
 * Apply Advanced Filters
 */
function applyAdvancedFilters() {
    const params = new URLSearchParams();
    
    const search = document.getElementById('search-input').value.trim();
    const address = document.getElementById('address-filter').value.trim();
    const relationship = document.getElementById('relationship-filter').value.trim();
    const room = document.getElementById('room-filter').value.trim();
    const signDateFrom = document.getElementById('sign-date-from').value.trim();
    const signDateTo = document.getElementById('sign-date-to').value.trim();
    
    if (search) params.set('search', search);
    if (address) params.set('address', address);
    if (relationship) params.set('relationship', relationship);
    if (room) params.set('room', room);
    if (signDateFrom) params.set('sign_date_from', signDateFrom);
    if (signDateTo) params.set('sign_date_to', signDateTo);
    
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
 * Clear Advanced Filters
 */
function clearAdvancedFilters() {
    document.getElementById('address-filter').value = '';
    document.getElementById('relationship-filter').value = '';
    document.getElementById('room-filter').value = '';
    document.getElementById('sign-date-from').value = '';
    document.getElementById('sign-date-to').value = '';
    window.location.href = window.location.pathname;
}

/**
 * View resident detail - Redirect đến trang chi tiết
 */
function viewResident(id) {
    window.location.href = `/residents/${id}/`;
}

/**
 * Open Add Resident Page
 */
function openAddModal() {
    window.location.href = '/residents/add/';
}

/**
 * Edit Resident - Redirect đến trang sửa
 */
function editResident(id) {
    window.location.href = `/residents/${id}/edit/`;
}

/**
 * Delete Resident - Chuyển trạng thái thành "Đã chuyển đi"
 */
function deleteResident(id) {
    if (confirm('Bạn có chắc muốn đánh dấu cư dân này là đã chuyển đi?')) {
        fetch(`/residents/${id}/update-status/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ status: 'moved_out' })
        })
        .then(response => {
            if (response.ok) {
                alert('Cập nhật trạng thái thành công!');
                location.reload();
            } else {
                alert('Có lỗi xảy ra. Vui lòng thử lại!');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra. Vui lòng thử lại!');
        });
    }
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
 * Get status display text
 */
function getStatusText(status) {
    const statusMap = {
        'living': 'Đang sống',
        'moved_out': 'Đã chuyển đi'
    };
    return statusMap[status] || status;
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
 * Close modal
 */
function closeModal() {
    document.getElementById('resident-modal').style.display = 'none';
}

// Close modal when click outside
window.onclick = (event) => {
    const modal = document.getElementById('resident-modal');
    if (event.target == modal) {
        closeModal();
    }
}
