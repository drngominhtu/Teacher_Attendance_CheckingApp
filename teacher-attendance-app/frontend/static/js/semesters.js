let isSubmitting = false;

document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    document.getElementById('semester-form').addEventListener('submit', handleFormSubmit);
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    if (isSubmitting) return;
    isSubmitting = true;
    
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang thêm...';
    
    const formData = {
        name: document.getElementById('semester-name').value,
        year: parseInt(document.getElementById('semester-year').value),
        academic_year: document.getElementById('semester-academic-year').value,
        is_current: document.getElementById('semester-is-current').checked
    };

    fetch('/api/semesters', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Kỳ học đã được tạo thành công!', 'success');
            document.getElementById('semester-form').reset();
            refreshSemestersList();
        } else {
            showAlert('Lỗi: ' + data.message, 'error');
        }
    })
    .catch(error => {
        showAlert('Có lỗi xảy ra: ' + error.message, 'error');
    })
    .finally(() => {
        isSubmitting = false;
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-plus"></i> Thêm kỳ học';
    });
}

function refreshSemestersList() {
    fetch('/api/semesters/list')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateSemestersTable(data.semesters);
        }
    })
    .catch(error => console.error('Error refreshing semesters:', error));
}

function updateSemestersTable(semesters) {
    const tbody = document.getElementById('semesters-tbody');
    tbody.innerHTML = '';
    
    if (semesters.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted py-4">
                    <i class="fas fa-inbox fa-2x mb-2"></i>
                    <br>Chưa có kỳ học nào
                </td>
            </tr>
        `;
        return;
    }
    
    semesters.forEach(semester => {
        const row = document.createElement('tr');
        row.setAttribute('data-semester-id', semester.id);
        row.innerHTML = `
            <td><strong>${semester.name}</strong></td>
            <td><span class="badge badge-info">${semester.year}</span></td>
            <td>${semester.academic_year || '-'}</td>
            <td>
                <span class="badge badge-${semester.is_current ? 'success' : 'secondary'}">
                    ${semester.is_current ? 'Hiện tại' : 'Không hoạt động'}
                </span>
            </td>
            <td>
                <button class="btn btn-outline-warning btn-sm" onclick="editSemester(${semester.id})" title="Chỉnh sửa">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-outline-danger btn-sm" onclick="deleteSemester(${semester.id})" title="Xóa">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function editSemester(id) {
    showAlert('Chức năng chỉnh sửa đang được phát triển', 'info');
}

function deleteSemester(id) {
    if (confirm('Bạn có chắc chắn muốn xóa kỳ học này?')) {
        fetch(`/api/semesters/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Kỳ học đã được xóa thành công!', 'success');
                refreshSemestersList();
            } else {
                showAlert('Lỗi: ' + data.message, 'error');
            }
        })
        .catch(error => showAlert('Có lỗi xảy ra: ' + error.message, 'error'));
    }
}

// Make functions globally available
window.refreshSemestersList = refreshSemestersList;
window.editSemester = editSemester;
window.deleteSemester = deleteSemester;
