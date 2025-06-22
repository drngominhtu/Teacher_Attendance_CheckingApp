"""
Test script để kiểm thử toàn bộ hệ thống quản lý giảng dạy
Tập trung vào các chức năng CRUD và API endpoints với test chi tiết
"""

import requests
import json
import time
from datetime import datetime, date
import random

class TeacherAttendanceSystemTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.created_semester_ids = []  # Track created semesters for cleanup
        
    def log_test(self, test_name, success, message="", data=None):
        """Ghi log kết quả test"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
    def test_homepage(self):
        """Test trang chủ"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log_test("Homepage", True, "Trang chủ load thành công")
                return True
            else:
                self.log_test("Homepage", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Homepage", False, f"Lỗi kết nối: {str(e)}")
            return False
    
    def test_department_crud(self):
        """Test CRUD operations cho Department"""
        print("\n🏢 Testing Department CRUD...")
        
        # Test GET departments list
        try:
            response = self.session.get(f"{self.base_url}/api/departments/list")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Get Departments", True, f"Tìm thấy {len(data.get('departments', []))} khoa")
                else:
                    self.log_test("Get Departments", False, data.get('message', 'Unknown error'))
            else:
                self.log_test("Get Departments", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get Departments", False, str(e))
        
        # Test CREATE department
        test_department = {
            "code": f"TEST{random.randint(100, 999)}",
            "name": f"Khoa Test {random.randint(100, 999)}",
            "abbreviation": "TEST",
            "description": "Khoa test được tạo bởi script kiểm thử"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/departments",
                json=test_department,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Create Department", True, "Tạo khoa thành công")
                    return test_department
                else:
                    self.log_test("Create Department", False, data.get('message', 'Unknown error'))
            else:
                self.log_test("Create Department", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Create Department", False, str(e))
        
        return None
    
    def test_degree_crud(self):
        """Test CRUD operations cho Degree"""
        print("\n🎓 Testing Degree CRUD...")
        
        # Test GET degrees list
        try:
            response = self.session.get(f"{self.base_url}/api/degrees/list")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Get Degrees", True, f"Tìm thấy {len(data.get('degrees', []))} bằng cấp")
                else:
                    self.log_test("Get Degrees", False, data.get('message', 'Unknown error'))
            else:
                self.log_test("Get Degrees", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get Degrees", False, str(e))
        
        # Test CREATE degree
        test_degree = {
            "name": f"Bằng Test {random.randint(100, 999)}",
            "abbreviation": f"BT{random.randint(10, 99)}",
            "coefficient": round(random.uniform(1.0, 2.5), 1),
            "description": "Bằng cấp test được tạo bởi script kiểm thử"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/degrees",
                json=test_degree,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Create Degree", True, "Tạo bằng cấp thành công")
                    return test_degree
                else:
                    self.log_test("Create Degree", False, data.get('message', 'Unknown error'))
            else:
                self.log_test("Create Degree", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Create Degree", False, str(e))
        
        return None
    
    def test_teacher_crud(self):
        """Test CRUD operations cho Teacher"""
        print("\n👨‍🏫 Testing Teacher CRUD...")
        
        # Test GET teachers list
        try:
            response = self.session.get(f"{self.base_url}/api/teachers/list")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Get Teachers", True, f"Tìm thấy {len(data.get('teachers', []))} giảng viên")
                else:
                    self.log_test("Get Teachers", False, data.get('message', 'Unknown error'))
            else:
                self.log_test("Get Teachers", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get Teachers", False, str(e))
        
        # Test CREATE teacher
        test_teacher = {
            "name": f"Giảng viên Test {random.randint(100, 999)}",
            "employee_code": f"GV{random.randint(1000, 9999)}",
            "email": f"test{random.randint(100, 999)}@university.edu.vn",
            "phone": f"090{random.randint(1000000, 9999999)}",
            "department_id": 1,  # Assuming department with ID 1 exists
            "degree_id": 1,      # Assuming degree with ID 1 exists
            "position": "Giảng viên",
            "birth_date": "1985-01-01",
            "base_salary": 15000000,
            "hourly_rate": 150000
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/teachers",
                json=test_teacher,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Create Teacher", True, "Tạo giảng viên thành công")
                    return data.get('teacher')
                else:
                    self.log_test("Create Teacher", False, data.get('message', 'Unknown error'))
            else:
                self.log_test("Create Teacher", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Create Teacher", False, str(e))
        
        return None
    
    def test_subject_crud(self):
        """Test CRUD operations cho Subject"""
        print("\n📚 Testing Subject CRUD...")
        
        # Test GET subjects page
        try:
            response = self.session.get(f"{self.base_url}/subjects")
            if response.status_code == 200:
                self.log_test("Get Subjects Page", True, "Trang quản lý học phần load thành công")
            else:
                self.log_test("Get Subjects Page", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Get Subjects Page", False, str(e))
        
        # Test CREATE subject
        test_subject = {
            "name": f"Học phần Test {random.randint(100, 999)}",
            "code": f"HP{random.randint(100, 999)}",
            "department_id": 1,  # Assuming department with ID 1 exists
            "credits": random.randint(2, 4),
            "theory_hours": random.randint(30, 45),
            "practice_hours": random.randint(0, 15),
            "subject_coefficient": round(random.uniform(1.0, 1.5), 1),
            "difficulty_level": random.choice(["normal", "hard", "very_hard"]),
            "description": "Học phần test được tạo bởi script kiểm thử"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/subjects",
                json=test_subject,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Create Subject", True, "Tạo học phần thành công")
                    return test_subject
                else:
                    self.log_test("Create Subject", False, data.get('message', 'Unknown error'))
            else:
                self.log_test("Create Subject", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Create Subject", False, str(e))
        
        return None
    
    def test_semester_crud_detailed(self):
        """Test CRUD operations cho Semester - chi tiết"""
        print("\n📅 Testing Semester CRUD (Detailed)...")
        
        # Test 1: GET semesters list
        try:
            print("1️⃣ Testing GET /api/semesters/list...")
            response = self.session.get(f"{self.base_url}/api/semesters/list")
            print(f"   Response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        semesters = data.get('semesters', [])
                        self.log_test("Get Semesters List", True, f"Tìm thấy {len(semesters)} kỳ học")
                        
                        # Log chi tiết từng semester
                        for sem in semesters[:3]:  # Chỉ log 3 đầu
                            print(f"   - Semester: {sem.get('name')} {sem.get('year')}")
                        
                    else:
                        self.log_test("Get Semesters List", False, data.get('message', 'Unknown error'))
                except json.JSONDecodeError as e:
                    self.log_test("Get Semesters List", False, f"JSON decode error: {str(e)}")
                    print(f"   Response text: {response.text[:500]}")
            else:
                self.log_test("Get Semesters List", False, f"HTTP {response.status_code}")
                print(f"   Response text: {response.text[:500]}")
        except Exception as e:
            self.log_test("Get Semesters List", False, str(e))
        
        # Test 2: CREATE semester
        current_year = datetime.now().year
        test_semester = {
            "name": f"Kỳ Test {random.randint(1, 999)}",
            "year": current_year,
            "start_date": f"{current_year}-09-01",
            "end_date": f"{current_year}-12-31",
            "is_current": False,
            "description": f"Kỳ học test được tạo lúc {datetime.now().strftime('%H:%M:%S')}"
        }
        
        created_semester = None
        try:
            print("\n2️⃣ Testing POST /api/semesters...")
            print(f"   Creating semester: {test_semester}")
            
            response = self.session.post(
                f"{self.base_url}/api/semesters",
                json=test_semester,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"   Create response status: {response.status_code}")
            print(f"   Create response text: {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        self.log_test("CREATE Semester", True, "Tạo kỳ học thành công")
                        
                        # Verify bằng cách get list lại
                        time.sleep(0.5)  # Wait a bit
                        verify_response = self.session.get(f"{self.base_url}/api/semesters/list")
                        if verify_response.status_code == 200:
                            verify_data = verify_response.json()
                            if verify_data.get('success'):
                                verify_list = verify_data.get('semesters', [])
                                
                                for sem in verify_list:
                                    if sem.get('name') == test_semester['name'] and sem.get('year') == test_semester['year']:
                                        created_semester = sem
                                        self.created_semester_ids.append(sem.get('id'))
                                        break
                                
                                if created_semester:
                                    self.log_test("CREATE Semester Verification", True, f"Semester đã được tạo với ID: {created_semester.get('id')}")
                                else:
                                    self.log_test("CREATE Semester Verification", False, "Không tìm thấy semester vừa tạo trong danh sách")
                    else:
                        self.log_test("CREATE Semester", False, data.get('message', 'Unknown error'))
                except json.JSONDecodeError as e:
                    self.log_test("CREATE Semester", False, f"JSON decode error: {str(e)}")
            else:
                self.log_test("CREATE Semester", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("CREATE Semester", False, str(e))
        
        # Test 3: GET single semester (if created successfully)
        if created_semester:
            semester_id = created_semester.get('id')
            try:
                print(f"\n3️⃣ Testing GET /api/semesters/{semester_id}...")
                
                response = self.session.get(f"{self.base_url}/api/semesters/{semester_id}")
                print(f"   Get single response status: {response.status_code}")
                print(f"   Get single response text: {response.text}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('success'):
                            semester = data.get('semester')
                            self.log_test("GET Single Semester", True, f"Lấy thông tin semester ID {semester_id} thành công")
                            print(f"   Semester data: {semester}")
                        else:
                            self.log_test("GET Single Semester", False, data.get('message', 'Unknown error'))
                    except json.JSONDecodeError as e:
                        self.log_test("GET Single Semester", False, f"JSON decode error: {str(e)}")
                else:
                    self.log_test("GET Single Semester", False, f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test("GET Single Semester", False, str(e))
            
            # Test 4: UPDATE semester
            try:
                print(f"\n4️⃣ Testing PUT /api/semesters/{semester_id}...")
                
                update_data = {
                    "name": f"Kỳ Updated {random.randint(1, 999)}",
                    "year": current_year,
                    "start_date": f"{current_year}-01-15",
                    "end_date": f"{current_year}-05-31",
                    "is_current": False,
                    "description": f"Updated at {datetime.now().strftime('%H:%M:%S')}"
                }
                
                print(f"   Update data: {update_data}")
                
                response = self.session.put(
                    f"{self.base_url}/api/semesters/{semester_id}",
                    json=update_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                print(f"   Update response status: {response.status_code}")
                print(f"   Update response text: {response.text}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('success'):
                            self.log_test("UPDATE Semester", True, f"Cập nhật semester ID {semester_id} thành công")
                            
                            # Verify bằng cách get lại
                            time.sleep(0.5)
                            verify_response = self.session.get(f"{self.base_url}/api/semesters/{semester_id}")
                            if verify_response.status_code == 200:
                                verify_data = verify_response.json()
                                if verify_data.get('success'):
                                    updated_semester = verify_data.get('semester')
                                    if updated_semester and updated_semester.get('name') == update_data['name']:
                                        self.log_test("UPDATE Semester Verification", True, "Dữ liệu đã được cập nhật đúng")
                                    else:
                                        self.log_test("UPDATE Semester Verification", False, "Dữ liệu không được cập nhật đúng")
                        else:
                            self.log_test("UPDATE Semester", False, data.get('message', 'Unknown error'))
                    except json.JSONDecodeError as e:
                        self.log_test("UPDATE Semester", False, f"JSON decode error: {str(e)}")
                else:
                    self.log_test("UPDATE Semester", False, f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test("UPDATE Semester", False, str(e))
            
            # Test 5: DELETE semester
            try:
                print(f"\n5️⃣ Testing DELETE /api/semesters/{semester_id}...")
                
                response = self.session.delete(f"{self.base_url}/api/semesters/{semester_id}")
                print(f"   Delete response status: {response.status_code}")
                print(f"   Delete response text: {response.text}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('success'):
                            self.log_test("DELETE Semester", True, f"Xóa semester ID {semester_id} thành công")
                            
                            # Verify bằng cách try get lại
                            time.sleep(0.5)
                            verify_response = self.session.get(f"{self.base_url}/api/semesters/{semester_id}")
                            if verify_response.status_code == 404 or (verify_response.status_code == 200 and not verify_response.json().get('success')):
                                self.log_test("DELETE Semester Verification", True, "Semester đã được xóa khỏi database")
                            else:
                                self.log_test("DELETE Semester Verification", False, "Semester vẫn còn trong database")
                        else:
                            self.log_test("DELETE Semester", False, data.get('message', 'Unknown error'))
                    except json.JSONDecodeError as e:
                        self.log_test("DELETE Semester", False, f"JSON decode error: {str(e)}")
                else:
                    self.log_test("DELETE Semester", False, f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test("DELETE Semester", False, str(e))
        
        # Test 6: Error scenarios
        self.test_semester_error_scenarios()
        
        return created_semester
    
    def test_semester_error_scenarios(self):
        """Test các trường hợp lỗi cho Semester"""
        print("\n⚠️ Testing Semester Error Scenarios...")
        
        # Test create với dữ liệu thiếu
        try:
            print("6️⃣ Testing invalid data scenarios...")
            invalid_data = {"name": "Test", "year": 2024}  # Thiếu start_date, end_date
            
            response = self.session.post(
                f"{self.base_url}/api/semesters",
                json=invalid_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data.get('success'):
                    self.log_test("Error Handling - Invalid Data", True, "Server xử lý lỗi dữ liệu thiếu đúng cách")
                else:
                    self.log_test("Error Handling - Invalid Data", False, "Server không validate dữ liệu thiếu")
            else:
                self.log_test("Error Handling - Invalid Data", True, f"Server trả về HTTP error: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling - Invalid Data", False, str(e))
        
        # Test get semester không tồn tại
        try:
            fake_id = 99999
            response = self.session.get(f"{self.base_url}/api/semesters/{fake_id}")
            
            if response.status_code == 200:
                data = response.json()
                if not data.get('success'):
                    self.log_test("Error Handling - Not Found", True, "Server xử lý ID không tồn tại đúng cách")
                else:
                    self.log_test("Error Handling - Not Found", False, "Server trả về success cho ID không tồn tại")
            else:
                self.log_test("Error Handling - Not Found", True, f"Server trả về HTTP error cho ID không tồn tại: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling - Not Found", False, str(e))
    
    def test_statistics_apis(self):
        """Test Statistics APIs"""
        print("\n📊 Testing Statistics APIs...")
        
        # Test teacher statistics
        try:
            response = self.session.get(f"{self.base_url}/api/statistics/teacher")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    stats = data.get('statistics', {})
                    self.log_test("Teacher Statistics", True, 
                                f"Thống kê GV: {stats.get('total_teachers', 0)} tổng, "
                                f"{stats.get('active_teachers', 0)} hoạt động")
                else:
                    self.log_test("Teacher Statistics", False, data.get('message', 'Unknown error'))
            else:
                self.log_test("Teacher Statistics", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Teacher Statistics", False, str(e))
        
        # Test subject statistics
        try:
            response = self.session.get(f"{self.base_url}/api/statistics/subject")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    stats = data.get('statistics', {})
                    self.log_test("Subject Statistics", True, 
                                f"Thống kê HP: {stats.get('total_subjects', 0)} tổng, "
                                f"{stats.get('active_subjects', 0)} hoạt động")
                else:
                    self.log_test("Subject Statistics", False, data.get('message', 'Unknown error'))
            else:
                self.log_test("Subject Statistics", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Subject Statistics", False, str(e))
    
    def test_all_pages(self):
        """Test tất cả các trang chính"""
        print("\n🌐 Testing All Main Pages...")
        
        pages = [
            ("/", "Homepage"),
            ("/teachers", "Teachers Page"),
            ("/subjects", "Subjects Page"),
            ("/departments", "Departments Page"),
            ("/degrees", "Degrees Page"),
            ("/semesters", "Semesters Page"),
            ("/teaching-assignments", "Teaching Assignments Page"),
            ("/class-sections", "Class Sections Page"),
            ("/salary-settings", "Salary Settings Page"),
            ("/salary-calculations", "Salary Calculations Page"),
            ("/salary-history", "Salary History Page"),
            ("/teacher-statistics", "Teacher Statistics Page"),
            ("/subject-statistics", "Subject Statistics Page"),
            ("/reports", "Reports Page")
        ]
        
        for url, name in pages:
            try:
                response = self.session.get(f"{self.base_url}{url}")
                if response.status_code == 200:
                    self.log_test(f"Page: {name}", True, f"Load thành công")
                else:
                    self.log_test(f"Page: {name}", False, f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test(f"Page: {name}", False, str(e))
            
            # Small delay between requests
            time.sleep(0.1)
    
    def cleanup_created_data(self):
        """Cleanup dữ liệu test đã tạo"""
        print("\n🧹 Cleaning up test data...")
        
        # Clean up created semesters
        for semester_id in self.created_semester_ids:
            try:
                response = self.session.delete(f"{self.base_url}/api/semesters/{semester_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        print(f"   ✅ Cleaned up semester ID: {semester_id}")
                    else:
                        print(f"   ❌ Failed to cleanup semester ID: {semester_id} - {data.get('message')}")
                else:
                    print(f"   ❌ Failed to cleanup semester ID: {semester_id} - HTTP {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error cleaning up semester ID: {semester_id} - {str(e)}")
    
    def run_all_tests(self):
        """Chạy tất cả các test"""
        print("🚀 Bắt đầu kiểm thử hệ thống quản lý giảng dạy...")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test connection first
        if not self.test_homepage():
            print("❌ Không thể kết nối đến server. Vui lòng kiểm tra server đã chạy chưa.")
            return False
        
        try:
            # Run all tests
            self.test_all_pages()
            self.test_department_crud()
            self.test_degree_crud()
            self.test_teacher_crud()
            self.test_subject_crud()
            self.test_semester_crud_detailed()  # Detailed semester testing
            self.test_statistics_apis()
            
        except KeyboardInterrupt:
            print("\n⚠️ Test bị ngắt bởi người dùng")
        except Exception as e:
            print(f"\n❌ Lỗi trong quá trình test: {str(e)}")
        finally:
            # Always cleanup
            self.cleanup_created_data()
        
        # Summary
        end_time = time.time()
        duration = end_time - start_time
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['success']])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 60)
        print("📊 KẾT QUẢ KIỂM THỬ")
        print("=" * 60)
        print(f"⏱️  Thời gian: {duration:.2f} giây")
        print(f"📝 Tổng số test: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📊 Tỷ lệ thành công: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ CÁC TEST THẤT BẠI:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['test']}: {result['message']}")
        
        # Show detailed semester test results
        semester_tests = [r for r in self.test_results if 'Semester' in r['test']]
        if semester_tests:
            print(f"\n📅 SEMESTER TEST DETAILS:")
            for result in semester_tests:
                status = "✅" if result['success'] else "❌"
                print(f"   {status} {result['test']}: {result['message']}")
        
        # Save detailed results to file
        self.save_test_results()
        
        return success_rate > 80  # Consider successful if >80% pass rate
    
    def save_test_results(self):
        """Lưu kết quả test ra file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'base_url': self.base_url,
                    'total_tests': len(self.test_results),
                    'passed': len([r for r in self.test_results if r['success']]),
                    'failed': len([r for r in self.test_results if not r['success']]),
                    'results': self.test_results
                }, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Chi tiết kết quả đã được lưu vào: {filename}")
        except Exception as e:
            print(f"❌ Không thể lưu kết quả test: {str(e)}")

def main():
    """Hàm main để chạy test"""
    print("🎯 KIỂM THỬ HỆ THỐNG QUẢN LÝ GIẢNG DẠY")
    print("=====================================")
    
    # Kiểm tra server có đang chạy không
    base_url = "http://127.0.0.1:5000"
    
    print(f"🔍 Kiểm tra server tại: {base_url}")
    
    # Tạo instance tester và chạy test
    tester = TeacherAttendanceSystemTester(base_url)
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 KIỂM THỬ HOÀN THÀNH THÀNH CÔNG!")
    else:
        print("\n⚠️  KIỂM THỬ HOÀN THÀNH VỚI MỘT SỐ LỖI!")
    
    print("\n💡 Hướng dẫn:")
    print("   - Đảm bảo server Flask đang chạy trước khi test")
    print("   - Kiểm tra file log chi tiết được tạo ra")
    print("   - Nếu có lỗi, kiểm tra database và models")
    print("   - Semester CRUD được test chi tiết nhất")

if __name__ == "__main__":
    main()
