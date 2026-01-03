/**
 * DASHBOARD SCRIPTS
 */

document.addEventListener('DOMContentLoaded', () => {
    setupModalEvents();
});

/**
 * Hiển thị Modal chi tiết căn hộ bằng cách gọi API
 */
function openRoomDetail(roomId) {
    const modal = document.getElementById('resident-modal');
    const residentsList = document.getElementById('modal-residents-list');
    
    // Reset modal content & show loading
    document.getElementById('modal-apt-number').innerText = `Đang tải...`;
    residentsList.innerHTML = '<div style="text-align:center; padding:20px;"><i class="fa-solid fa-spinner fa-spin"></i> Đang lấy dữ liệu...</div>';
    modal.classList.add('active');

    // Gọi API từ Backend
    fetch(`/api/room-detail/${roomId}/`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            // Cập nhật thông tin cơ bản
            document.getElementById('modal-apt-number').innerText = `Căn hộ ${data.room_number}`;
            document.getElementById('modal-building-name').innerText = data.building_name || '--';
            document.getElementById('modal-floor-number').innerText = data.floor_number || '--';
            document.getElementById('modal-apt-status').innerText = data.status;
            document.getElementById('modal-apt-area').innerText = `${data.area} m²`;

            // Cập nhật các nút hành động
            const viewDetailBtn = document.getElementById('btn-view-detail');
            const editRoomBtn = document.getElementById('btn-edit-room');
            
            if (data.room_id) {
                viewDetailBtn.href = `/rooms/detail/${data.room_id}/`;
                editRoomBtn.href = `/rooms/${data.room_id}/update/`;
                viewDetailBtn.style.display = 'inline-flex';
                editRoomBtn.style.display = 'inline-flex';
            } else {
                console.error('Room ID not found in API response');
                viewDetailBtn.style.display = 'none';
                editRoomBtn.style.display = 'none';
            }

            // Cập nhật danh sách cư dân
            residentsList.innerHTML = '';
            if (data.residents && data.residents.length > 0) {
                data.residents.forEach(res => {
                    const item = document.createElement('div');
                    item.className = 'resident-item';
                    item.innerHTML = `
                        <div class="avatar" style="background:#e2e8f0; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#2563eb;">
                            ${res.name.charAt(0)}
                        </div>
                        <div style="flex:1">
                            <div style="font-weight:bold; color:#1e293b">${res.name} <span style="font-size:12px; color:#64748b; font-weight:normal">(${res.role})</span></div>
                            <div style="font-size:13px; color:#64748b; margin-top:2px;">
                                <i class="fa-solid fa-phone" style="font-size:10px"></i> ${res.phone_number}
                            </div>
                        </div>
                    `;
                    residentsList.appendChild(item);
                });
            } else {
                residentsList.innerHTML = `
                    <div style="text-align:center; padding:30px; color:#94a3b8; border: 2px dashed #e2e8f0; border-radius:12px;">
                        <i class="fa-solid fa-user-slash" style="font-size:24px; margin-bottom:10px; display:block;"></i>
                        Chưa có cư dân đăng ký
                    </div>`;
            }
        })
        .catch(error => {
            console.error('Error fetching room detail:', error);
            document.getElementById('modal-apt-number').innerText = `Lỗi!`;
            residentsList.innerHTML = '<div style="color:#ef4444; text-align:center; padding:20px;">Không thể tải dữ liệu. Vui lòng thử lại.</div>';
        });
}

/**
 * Xử lý đóng Modal
 */
function setupModalEvents() {
    const modal = document.getElementById('resident-modal');
    const closeBtn = document.querySelector('.close-btn');

    if (closeBtn) {
        closeBtn.onclick = () => {
            modal.classList.remove('active');
        }
    }

    window.onclick = (event) => {
        if (event.target == modal) {
            modal.classList.remove('active');
        }
    }
}
