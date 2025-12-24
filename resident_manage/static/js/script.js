/**
 * MOCK API CONFIGURATION
 * Đội Backend sẽ thay thế các URL này bằng endpoint thực tế của Django
 */
const API_CONFIG = {
    BUILDINGS: '/api/buildings/', 
    // Ví dụ: /api/buildings/1/apartments/
};

// Dữ liệu giả lập (Mock Data) để test Frontend khi chưa có Backend
const MOCK_DATA = {
    stats: {
        totalApartments: 120,
        occupied: 98,
        vacant: 15,
        maintenance: 7
    },
    floors: [
        {
            id: 1,
            name: "Tầng 1",
            apartments: [
                { id: 101, number: "101", status: "occupied", contract_expiring: false, area: 80, owner: "Nguyễn Văn A" },
                { id: 102, number: "102", status: "occupied", contract_expiring: true, area: 100, owner: "Trần Thị B" }, // Sắp hết hạn
                { id: 103, number: "103", status: "empty", contract_expiring: false, area: 80, owner: null },
                { id: 104, number: "104", status: "maintenance", contract_expiring: false, area: 120, owner: null },
            ]
        },
        {
            id: 2,
            name: "Tầng 2",
            apartments: [
                { id: 201, number: "201", status: "occupied", contract_expiring: false, area: 85, owner: "Lê Văn C" },
                { id: 202, number: "202", status: "occupied", contract_expiring: false, area: 85, owner: "Phạm Thị D" },
                { id: 203, number: "203", status: "empty", contract_expiring: false, area: 85, owner: null },
                { id: 204, number: "204", status: "occupied", contract_expiring: false, area: 110, owner: "Hoàng Văn E" },
            ]
        },
        // Thêm tầng giả lập
        ...Array.from({ length: 3 }, (_, i) => ({
            id: i + 3,
            name: `Tầng ${i + 3}`,
            apartments: Array.from({ length: 6 }, (_, j) => ({
                id: (i + 3) * 100 + j + 1,
                number: `${i + 3}0${j + 1}`,
                status: Math.random() > 0.7 ? 'empty' : (Math.random() > 0.9 ? 'maintenance' : 'occupied'),
                contract_expiring: Math.random() > 0.9,
                area: 90,
                owner: "Cư dân mẫu"
            }))
        }))
    ],
    residents_mock: {
        101: [
            { name: "Nguyễn Văn A", role: "Chủ hộ", phone: "0901234567" },
            { name: "Nguyễn Thị X", role: "Vợ", phone: "0901234568" }
        ],
        102: [
            { name: "Trần Thị B", role: "Chủ hộ", phone: "0912345678" }
        ]
    }
};

document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
});

function initDashboard() {
    renderStats();
    renderBuildingMap();
    setupModalEvents();
}

function renderStats() {
    document.getElementById('stat-total').innerText = MOCK_DATA.stats.totalApartments;
    document.getElementById('stat-occupied').innerText = MOCK_DATA.stats.occupied;
    document.getElementById('stat-empty').innerText = MOCK_DATA.stats.vacant;
}

/**
 * TASK 5: Hiển thị sơ đồ căn hộ trực quan
 */
function renderBuildingMap() {
    const container = document.getElementById('building-map');
    container.innerHTML = ''; // Clear loading state

    MOCK_DATA.floors.forEach(floor => {
        const floorRow = document.createElement('div');
        floorRow.className = 'floor-row';

        // Label Tầng
        const label = document.createElement('div');
        label.className = 'floor-label';
        label.innerText = floor.name;
        floorRow.appendChild(label);

        // Danh sách căn hộ
        const aptList = document.createElement('div');
        aptList.className = 'apartments-list';

        floor.apartments.forEach(apt => {
            const aptBox = document.createElement('div');
            aptBox.className = `apartment-box status-${apt.status}`;
            
            // Nội dung căn hộ
            let content = `
                <div class="apt-number">${apt.number}</div>
                <div class="apt-status-text">${getStatusText(apt.status)}</div>
            `;

            // TASK 3: Icon cảnh báo hết hạn hợp đồng
            if (apt.contract_expiring) {
                content += `<div class="warning-icon" title="Sắp hết hạn hợp đồng">!</div>`;
            }

            aptBox.innerHTML = content;

            // Sự kiện Click để xem chi tiết (Task 4)
            aptBox.addEventListener('click', () => openApartmentModal(apt));

            aptList.appendChild(aptBox);
        });

        floorRow.appendChild(aptList);
        container.appendChild(floorRow);
    });
}

function getStatusText(status) {
    switch(status) {
        case 'occupied': return 'Đã thuê';
        case 'empty': return 'Trống';
        case 'maintenance': return 'Bảo trì';
        default: return '';
    }
}

/**
 * TASK 4: Modal chi tiết cư dân
 */
function openApartmentModal(apt) {
    const modal = document.getElementById('resident-modal');
    document.getElementById('modal-apt-number').innerText = `Căn hộ ${apt.number}`;
    document.getElementById('modal-apt-status').innerText = getStatusText(apt.status);
    document.getElementById('modal-apt-area').innerText = `${apt.area} m²`;

    // Load residents (giả lập lấy từ API)
    const residentsList = document.getElementById('modal-residents-list');
    residentsList.innerHTML = '';

    const residents = MOCK_DATA.residents_mock[apt.id] || [];
    
    if (residents.length === 0 && apt.status === 'occupied') {
        residentsList.innerHTML = '<div style="color:#999">Đang tải dữ liệu cư dân...</div>';
    } else if (residents.length === 0) {
        residentsList.innerHTML = '<div style="color:#999">Chưa có cư dân</div>';
    } else {
        residents.forEach(res => {
            const item = document.createElement('div');
            item.className = 'resident-item';
            item.innerHTML = `
                <div class="avatar">${res.name.charAt(0)}</div>
                <div>
                    <div style="font-weight:bold">${res.name} <span style="font-size:12px; color:#666">(${res.role})</span></div>
                    <div style="font-size:12px; color:#666">${res.phone}</div>
                </div>
            `;
            residentsList.appendChild(item);
        });
    }

    modal.classList.add('active');
}

function setupModalEvents() {
    const modal = document.getElementById('resident-modal');
    const closeBtn = document.querySelector('.close-btn');

    closeBtn.onclick = () => {
        modal.classList.remove('active');
    }

    window.onclick = (event) => {
        if (event.target == modal) {
            modal.classList.remove('active');
        }
    }
}

