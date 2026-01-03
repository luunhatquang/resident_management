/* ==================== INVOICES SCRIPTS ==================== */

// Apply filters - Redirect với query params
function applyFilters() {
    const status = document.getElementById('filter-status').value;
    const service = document.getElementById('filter-service').value;
    const building = document.getElementById('filter-building').value;
    const dateFrom = document.getElementById('date-from').value;
    const dateTo = document.getElementById('date-to').value;
    const search = document.getElementById('search-input').value.trim();
    
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (service) params.append('service', service);
    if (building) params.append('building', building);
    if (dateFrom) params.append('date_from', dateFrom);
    if (dateTo) params.append('date_to', dateTo);
    if (search) params.append('search', search);
    
    window.location.href = `/invoices/?${params.toString()}`;
}

// Clear all filters
function clearFilters() {
    window.location.href = '/invoices/';
}

// Navigate to add invoice page
function openAddModal() {
    window.location.href = '/invoices/create/';
}

// View invoice details
function viewInvoice(invoiceId) {
    window.location.href = `/invoices/${invoiceId}/`;
}

// Edit invoice
function editInvoice(invoiceId) {
    window.location.href = `/invoices/${invoiceId}/update/`;
}

// Mark invoice as paid
function markAsPaid(invoiceId) {
    if (confirm('Xác nhận đánh dấu hóa đơn này đã thanh toán?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/invoices/${invoiceId}/pay/`;
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        
        form.appendChild(csrfInput);
        document.body.appendChild(form);
        form.submit();
    }
}

// Delete invoice
function deleteInvoice(invoiceId) {
    if (confirm('Bạn có chắc muốn xóa hóa đơn này?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/invoices/${invoiceId}/delete/`;
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        
        form.appendChild(csrfInput);
        document.body.appendChild(form);
        form.submit();
    }
}

// ==================== FORM AUTO-CALCULATION ====================
document.addEventListener('DOMContentLoaded', function() {
    const serviceField = document.getElementById('id_service');
    const contractField = document.getElementById('id_contract');
    const roomField = document.getElementById('id_room');
    const residentField = document.getElementById('id_resident');
    const countUnitField = document.getElementById('id_count_unit');
    const unitPriceField = document.getElementById('id_unit_price');
    const totalPriceField = document.getElementById('id_total_price');
    const contractGroup = document.getElementById('contract-group');

    function calculateTotalPrice() {
        const count = parseFloat(countUnitField.value) || 0;
        const price = parseFloat(unitPriceField.value) || 0;
        totalPriceField.value = (count * price).toFixed(2);
    }

    function setupContractAutoFill() {
        if (serviceField.value === 'rent') {
            contractGroup.style.display = 'block';
            contractField.required = true;
            unitPriceField.readOnly = true;
        } else {
            contractGroup.style.display = 'none';
            contractField.required = false;
            contractField.value = '';
            unitPriceField.readOnly = false;
            if (serviceField.dataset.prevValue === 'rent') {
                roomField.value = '';
                residentField.value = '';
                unitPriceField.value = '';
            }
        }
        serviceField.dataset.prevValue = serviceField.value;
        calculateTotalPrice();
    }

    if (serviceField) {
        serviceField.addEventListener('change', setupContractAutoFill);
        setupContractAutoFill();
    }

    if (contractField) {
        contractField.addEventListener('change', function() {
            const contractId = this.value;
            if (contractId && serviceField.value === 'rent') {
                fetch(`/api/contract/${contractId}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            roomField.value = data.room_id;
                            residentField.value = data.resident_id;
                            unitPriceField.value = data.price_per_month;
                            unitPriceField.readOnly = true;
                            calculateTotalPrice();
                        }
                    })
                    .catch(error => console.error('Error fetching contract details:', error));
            } else if (!contractId && serviceField.value === 'rent') {
                roomField.value = '';
                residentField.value = '';
                unitPriceField.value = '';
                unitPriceField.readOnly = false;
                calculateTotalPrice();
            }
        });
    }

    if (countUnitField) {
        countUnitField.addEventListener('input', calculateTotalPrice);
    }
    if (unitPriceField) {
        unitPriceField.addEventListener('input', calculateTotalPrice);
    }

    calculateTotalPrice();
});
