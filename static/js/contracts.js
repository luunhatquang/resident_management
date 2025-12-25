/**
 * CONTRACT MANAGEMENT - JavaScript
 * Data được render từ Django Backend
 */

/**
 * Apply filters - Redirect với query params
 */
function applyFilters() {
    const typeFilter = document.getElementById('filter-type').value;
    const statusFilter = document.getElementById('filter-status').value;
    const searchText = document.getElementById('search-input').value.trim();
    
    // Build URL với query params
    const params = new URLSearchParams();
    
    if (typeFilter) params.set('type', typeFilter);
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
 * View contract detail - Redirect đến trang chi tiết
 */
function viewContract(id) {
    window.location.href = `/contracts/${id}/`;
}

/**
 * Open Add Contract Page
 */
function openAddModal() {
    window.location.href = '/contracts/add/';
}

/**
 * Edit Contract - Redirect đến trang sửa
 */
function editContract(id) {
    window.location.href = `/contracts/${id}/edit/`;
}

/**
 * Delete Contract - Redirect đến trang xóa
 */
function deleteContract(id) {
    if (confirm('Bạn có chắc muốn xóa hợp đồng này?\n\nLưu ý: Hành động này không thể hoàn tác!')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/contracts/${id}/delete/`;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = getCookie('csrftoken');
        form.appendChild(csrfInput);
        document.body.appendChild(form);
        form.submit();
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
        'pending': 'Chờ duyệt',
        'active': 'Đang hiệu lực',
        'expired': 'Đã hết hạn',
        'terminated': 'Đã chấm dứt',
        'rejected': 'Từ chối'
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

// Close modal when click outside
window.onclick = (event) => {
    const modal = document.getElementById('contract-modal');
    if (event.target == modal) {
        closeModal();
    }
}

