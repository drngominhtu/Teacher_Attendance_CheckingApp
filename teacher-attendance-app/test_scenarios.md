# KỊCH BẢN KIỂM THỬ HỆ THỐNG QUẢN LÝ GIẢNG DẠY

## 📋 TỔNG QUAN

**Mục tiêu**: Kiểm thử toàn diện hệ thống quản lý giảng dạy và tính lương
**Phạm vi**: API endpoints, CRUD operations, UI pages, error handling
**Công cụ**: Python script `test_application.py`
**Thời gian dự kiến**: 5-10 phút

---

## 🎯 CÁC KỊCH BẢN KIỂM THỬ

### 1. KIỂM THỬ KẾT NỐI & TRANG CHỦ

#### Scenario 1.1: Kiểm tra kết nối server
- **Mục tiêu**: Đảm bảo server Flask đang chạy
- **Test case**: GET `/`
- **Kết quả mong đợi**: Status 200, trang chủ load thành công
- **Lý do thất bại**: Server chưa chạy hoặc port đã bị chiếm

#### Scenario 1.2: Kiểm tra tất cả trang chính
- **Mục tiêu**: Đảm bảo routing hoạt động đúng
- **Test cases**:
  - `/` - Homepage
  - `/teachers` - Quản lý giảng viên
  - `/subjects` - Quản lý học phần
  - `/departments` - Quản lý khoa
  - `/degrees` - Quản lý bằng cấp
  - `/semesters` - Quản lý kỳ học
  - `/teaching-assignments` - Phân công giảng dạy
  - `/class-sections` - Quản lý lớp học phần
  - `/salary-settings` - Cài đặt lương
  - `/salary-calculations` - Tính lương
  - `/salary-history` - Lịch sử lương
  - `/teacher-statistics` - Thống kê giảng viên
  - `/subject-statistics` - Thống kê học phần
  - `/reports` - Báo cáo
- **Kết quả mong đợi**: Tất cả trang load với status 200

---

### 2. KIỂM THỬ CRUD - KHOA (DEPARTMENTS)

#### Scenario 2.1: Lấy danh sách khoa
- **Test case**: GET `/api/departments/list`
- **Kết quả mong đợi**: JSON với `success: true` và danh sách khoa
- **Dữ liệu kiểm tra**: Số lượng khoa hiện có

#### Scenario 2.2: Tạo khoa mới
- **Test case**: POST `/api/departments`
- **Dữ liệu test**:
  ```json
  {
    "code": "TEST123",
    "name": "Khoa Test 456",
    "abbreviation": "TEST",
    "description": "Khoa test được tạo bởi script kiểm thử"
  }
  ```
- **Kết quả mong đợi**: `success: true`, khoa được tạo thành công
- **Validation**: Code và name phải unique

---

### 3. KIỂM THỬ CRUD - BẰNG CẤP (DEGREES)

#### Scenario 3.1: Lấy danh sách bằng cấp
- **Test case**: GET `/api/degrees/list`
- **Kết quả mong đợi**: Danh sách các bằng cấp với coefficient

#### Scenario 3.2: Tạo bằng cấp mới
- **Test case**: POST `/api/degrees`
- **Dữ liệu test**:
  ```json
  {
    "name": "Bằng Test 789",
    "abbreviation": "BT12",
    "coefficient": 1.5,
    "description": "Bằng cấp test"
  }
  ```
- **Validation**: Name và abbreviation phải unique

---

### 4. KIỂM THỬ CRUD - GIẢNG VIÊN (TEACHERS)

#### Scenario 4.1: Lấy danh sách giảng viên
- **Test case**: GET `/api/teachers/list`
- **Kết quả mong đợi**: Danh sách giảng viên với thông tin đầy đủ

#### Scenario 4.2: Tạo giảng viên mới
- **Test case**: POST `/api/teachers`
- **Dữ liệu test**:
  ```json
  {
    "name": "Giảng viên Test 123",
    "employee_code": "GV1234",
    "email": "test123@university.edu.vn",
    "phone": "0901234567",
    "department_id": 1,
    "degree_id": 1,
    "position": "Giảng viên",
    "birth_date": "1985-01-01",
    "base_salary": 15000000,
    "hourly_rate": 150000
  }
  ```
- **Validation**: employee_code và email phải unique

---

### 5. KIỂM THỬ CRUD - HỌC PHẦN (SUBJECTS)

#### Scenario 5.1: Kiểm tra trang quản lý học phần
- **Test case**: GET `/subjects`
- **Kết quả mong đợi**: Trang load thành công với form và table

#### Scenario 5.2: Tạo học phần mới
- **Test case**: POST `/api/subjects`
- **Dữ liệu test**:
  ```json
  {
    "name": "Học phần Test 456",
    "code": "HP456",
    "department_id": 1,
    "credits": 3,
    "theory_hours": 45,
    "practice_hours": 0,
    "subject_coefficient": 1.2,
    "difficulty_level": "normal",
    "description": "Học phần test"
  }
  ```

---

### 6. KIỂM THỬ CHI TIẾT - KỲ HỌC (SEMESTERS)

#### Scenario 6.1: CRUD hoàn chỉnh cho Semester
**Đây là test case chi tiết nhất, bao gồm 5 bước:**

##### Bước 1: GET danh sách kỳ học
- **Test case**: GET `/api/semesters/list`
- **Kiểm tra**: Response format, số lượng kỳ học
- **Debug**: Log chi tiết 3 kỳ học đầu tiên

##### Bước 2: CREATE kỳ học mới
- **Test case**: POST `/api/semesters`
- **Dữ liệu test**:
  ```json
  {
    "name": "Kỳ Test 789",
    "year": 2024,
    "start_date": "2024-09-01",
    "end_date": "2024-12-31",
    "is_current": false,
    "description": "Kỳ học test được tạo lúc 14:30:25"
  }
  ```
- **Verification**: Kiểm tra lại bằng GET list để confirm

##### Bước 3: GET thông tin kỳ học vừa tạo
- **Test case**: GET `/api/semesters/{id}`
- **Kiểm tra**: Dữ liệu trả về đúng với dữ liệu đã tạo

##### Bước 4: UPDATE kỳ học
- **Test case**: PUT `/api/semesters/{id}`
- **Dữ liệu update**:
  ```json
  {
    "name": "Kỳ Updated 999",
    "year": 2024,
    "start_date": "2024-01-15",
    "end_date": "2024-05-31",
    "is_current": false,
    "description": "Updated at 14:31:10"
  }
  ```
- **Verification**: GET lại để kiểm tra update thành công

##### Bước 5: DELETE kỳ học
- **Test case**: DELETE `/api/semesters/{id}`
- **Verification**: GET lại để confirm đã bị xóa

#### Scenario 6.2: Error Handling cho Semester
##### Test case 6.2.1: Dữ liệu thiếu
- **Test**: POST với data thiếu start_date, end_date
- **Kết quả mong đợi**: `success: false` với message lỗi validation

##### Test case 6.2.2: ID không tồn tại
- **Test**: GET `/api/semesters/99999`
- **Kết quả mong đợi**: `success: false` hoặc HTTP 404

---

### 7. KIỂM THỬ THỐNG KÊ (STATISTICS)

#### Scenario 7.1: Thống kê giảng viên
- **Test case**: GET `/api/statistics/teacher`
- **Kết quả mong đợi**: 
  ```json
  {
    "success": true,
    "statistics": {
      "total_teachers": 10,
      "active_teachers": 8,
      "phd_teachers": 3,
      "avg_age": 35.5
    }
  }
  ```

#### Scenario 7.2: Thống kê học phần
- **Test case**: GET `/api/statistics/subject`
- **Kết quả mong đợi**: Thống kê số lượng, tín chỉ, độ khó

---

### 8. KIỂM THỬ CLEANUP

#### Scenario 8.1: Dọn dẹp dữ liệu test
- **Mục tiêu**: Xóa tất cả dữ liệu test đã tạo
- **Quy trình**: 
  1. Track các ID đã tạo trong quá trình test
  2. DELETE từng item
  3. Confirm đã xóa thành công
- **Lưu ý**: Cleanup chạy trong finally block để đảm bảo luôn thực hiện

---

## 📊 METRICS & KẾT QUẢ

### Thông số đo lường:
- **Tổng số test cases**: ~30-40 tests
- **Thời gian chạy**: 30-60 giây
- **Tỷ lệ thành công mong đợi**: >80%
- **Coverage**: Tất cả main endpoints

### Kết quả report:
- **Console output**: Real-time với emoji status
- **JSON file**: Chi tiết timestamp, duration, results
- **Summary**: Pass/fail count, success rate, failed tests list

---

## 🚨 CÁC TRƯỜNG HỢP LỖI THƯỜNG GẶP

### Lỗi kết nối:
- **Triệu chứng**: "Connection refused" hoặc timeout
- **Nguyên nhân**: Server chưa chạy hoặc sai port
- **Giải pháp**: Chạy `python backend/app.py` trước

### Lỗi database:
- **Triệu chứng**: "Table doesn't exist" hoặc migration errors
- **Nguyên nhân**: Database chưa được setup
- **Giải pháp**: Chạy migration hoặc tạo database mới

### Lỗi validation:
- **Triệu chứng**: "Field không được để trống"
- **Nguyên nhân**: API validation chặt
- **Đánh giá**: Đây là behavior đúng

### Lỗi foreign key:
- **Triệu chứng**: "Department không tồn tại"
- **Nguyên nhân**: Test data phụ thuộc vào existing records
- **Giải pháp**: Tạo department/degree trước khi test teacher

---

## 🎯 CÁCH CHẠY TEST

### Preparation:
```bash
cd d:\Code_Progress\APP_CHAM_CONG_2\teacher-attendance-app
```

### Start server:
```bash
python backend/app.py
```

### Run tests (trong terminal khác):
```bash
python test_application.py
```

### Đọc kết quả:
- Console: Real-time progress
- File JSON: Chi tiết từng test case
- Summary: Tổng kết cuối chương trình

---

## 📝 CUSTOMIZATION

### Thay đổi server URL:
```python
tester = TeacherAttendanceSystemTester("http://localhost:8000")
```

### Chạy test riêng lẻ:
```python
tester.test_semester_crud_detailed()  # Chỉ test semester
```

### Thêm test case mới:
```python
def test_new_feature(self):
    # Implementation here
    pass
```

---

## 🎉 ĐÁNH GIÁ THÀNH CÔNG

**Test được coi là thành công khi:**
- ✅ Tỷ lệ pass >= 80%
- ✅ Không có lỗi kết nối
- ✅ CRUD cơ bản hoạt động
- ✅ Error handling đúng cách
- ✅ Cleanup hoàn tất

**Báo cáo cuối:** File JSON chi tiết + console summary cho phép debug và track progress theo thời gian.
