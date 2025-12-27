/* ==================== NOTIFICATIONS SCRIPTS ==================== */

// Navigate to create notification page (when implemented)
function openAddModal() {
    // TODO: Implement create notification page
    // window.location.href = '/notifications/create/';
    alert('Chức năng tạo thông báo sẽ được triển khai sau.');
}

// Mark notification as read
function markAsRead(notificationId) {
    // TODO: Implement mark as read API
    console.log('Mark as read:', notificationId);
    alert('Chức năng đánh dấu đã đọc sẽ được triển khai sau.');
}

// Delete notification
function deleteNotification(notificationId) {
    if (confirm('Bạn có chắc muốn xóa thông báo này?')) {
        // TODO: Implement delete API
        console.log('Delete notification:', notificationId);
        alert('Chức năng xóa thông báo sẽ được triển khai sau.');
    }
}
