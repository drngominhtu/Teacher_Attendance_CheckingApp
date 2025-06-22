"""
Script tạo dữ liệu mẫu cho hệ thống quản lý giảng dạy
Tạo nhiều data để test và demo hệ thống
"""

import requests
import json
import random
from datetime import datetime, date, timedelta
import time

class SampleDataCreator:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.created_data = {
            'departments': [],
            'degrees': [],
            'teachers': [],
            'subjects': [],
            'semesters': [],
            'teaching_assignments': [],
            'class_sections': []
        }
        
    def log(self, message):
        """Log với timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def test_connection(self):
        """Kiểm tra kết nối server"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log("✅ Kết nối server thành công")
                return True
            else:
                self.log(f"❌ Server trả về status {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ Lỗi kết nối: {str(e)}")
            return False
    
    def create_departments(self, count=10):
        """Tạo dữ liệu khoa"""
        self.log(f"🏢 Tạo {count} khoa...")
        
        department_names = [
            "Khoa Công nghệ Thông tin",
            "Khoa Toán - Thống kê", 
            "Khoa Vật lý",
            "Khoa Hóa học",
            "Khoa Sinh học",
            "Khoa Kinh tế",
            "Khoa Quản trị Kinh doanh",
            "Khoa Ngôn ngữ Anh",
            "Khoa Văn học",
            "Khoa Lịch sử",
            "Khoa Địa lý",
            "Khoa Giáo dục",
            "Khoa Tâm lý",
            "Khoa Xã hội học",
            "Khoa Triết học"
        ]
        
        created_count = 0
        for i in range(min(count, len(department_names))):
            dept_data = {
                "code": f"DEPT{i+1:03d}",
                "name": department_names[i],
                "abbreviation": department_names[i].split()[1][:4].upper() if len(department_names[i].split()) > 1 else department_names[i][:4].upper(),
                "description": f"Mô tả cho {department_names[i]}"
            }
            
            try:
                response = self.session.post(
                    f"{self.base_url}/api/departments",
                    json=dept_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.created_data['departments'].append(dept_data)
                        created_count += 1
                        self.log(f"   ✅ Tạo khoa: {dept_data['name']}")
                    else:
                        self.log(f"   ⚠️  Khoa đã tồn tại: {dept_data['name']}")
                else:
                    self.log(f"   ❌ Lỗi tạo khoa: {dept_data['name']}")
                    
            except Exception as e:
                self.log(f"   ❌ Exception: {str(e)}")
            
            time.sleep(0.1)  # Delay nhỏ
        
        self.log(f"🏢 Hoàn thành tạo {created_count} khoa")
        return created_count
    
    def create_degrees(self, count=8):
        """Tạo dữ liệu bằng cấp"""
        self.log(f"🎓 Tạo {count} bằng cấp...")
        
        degrees_data = [
            {"name": "Cử nhân", "abbreviation": "CN", "coefficient": 1.0},
            {"name": "Kỹ sư", "abbreviation": "KS", "coefficient": 1.1},
            {"name": "Thạc sĩ", "abbreviation": "ThS", "coefficient": 1.3},
            {"name": "Tiến sĩ", "abbreviation": "TS", "coefficient": 1.6},
            {"name": "Phó Giáo sư", "abbreviation": "PGS", "coefficient": 1.9},
            {"name": "Giáo sư", "abbreviation": "GS", "coefficient": 2.2},
            {"name": "Thạc sĩ Khoa học", "abbreviation": "MSc", "coefficient": 1.35},
            {"name": "Tiến sĩ Khoa học", "abbreviation": "PhD", "coefficient": 1.65}
        ]
        
        created_count = 0
        for i in range(min(count, len(degrees_data))):
            degree_data = degrees_data[i]
            degree_data["description"] = f"Bằng {degree_data['name']} với hệ số {degree_data['coefficient']}"
            
            try:
                response = self.session.post(
                    f"{self.base_url}/api/degrees",
                    json=degree_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.created_data['degrees'].append(degree_data)
                        created_count += 1
                        self.log(f"   ✅ Tạo bằng cấp: {degree_data['name']}")
                    else:
                        self.log(f"   ⚠️  Bằng cấp đã tồn tại: {degree_data['name']}")
                else:
                    self.log(f"   ❌ Lỗi tạo bằng cấp: {degree_data['name']}")
                    
            except Exception as e:
                self.log(f"   ❌ Exception: {str(e)}")
            
            time.sleep(0.1)
        
        self.log(f"🎓 Hoàn thành tạo {created_count} bằng cấp")
        return created_count
    
    def get_existing_data(self):
        """Lấy dữ liệu đã có trong database"""
        self.log("📊 Lấy dữ liệu hiện có...")
        
        # Get departments
        try:
            response = self.session.get(f"{self.base_url}/api/departments/list")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    departments = data.get('departments', [])
                    self.log(f"   📁 Tìm thấy {len(departments)} khoa")
                    return departments
        except Exception as e:
            self.log(f"   ❌ Lỗi lấy danh sách khoa: {str(e)}")
        
        return []
    
    def get_existing_degrees(self):
        """Lấy bằng cấp đã có"""
        try:
            response = self.session.get(f"{self.base_url}/api/degrees/list")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    degrees = data.get('degrees', [])
                    self.log(f"   🎓 Tìm thấy {len(degrees)} bằng cấp")
                    return degrees
        except Exception as e:
            self.log(f"   ❌ Lỗi lấy danh sách bằng cấp: {str(e)}")
        return []
    
    def create_teachers(self, count=50):
        """Tạo nhiều giảng viên"""
        self.log(f"👨‍🏫 Tạo {count} giảng viên...")
        
        # Get departments and degrees
        departments = self.get_existing_data()
        degrees = self.get_existing_degrees()
        
        if not departments or not degrees:
            self.log("❌ Cần có khoa và bằng cấp trước khi tạo giảng viên")
            return 0
        
        # Vietnamese names
        first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương"]
        middle_names = ["Văn", "Thị", "Minh", "Quang", "Hữu", "Đức", "Anh", "Thanh", "Tuấn", "Hoàng", "Phương", "Thu", "Lan", "Mai"]
        last_names = ["An", "Bình", "Cường", "Dũng", "Hải", "Hùng", "Khang", "Long", "Nam", "Phong", "Quang", "Sơn", "Tâm", "Tuấn", "Vinh", "Yên", "Linh", "Nga", "Hương", "Trang"]
        
        positions = ["Giảng viên", "Giảng viên chính", "Phó Giáo sư", "Giáo sư", "Trợ giảng"]
        
        created_count = 0
        for i in range(count):
            # Generate name
            first = random.choice(first_names)
            middle = random.choice(middle_names)
            last = random.choice(last_names)
            full_name = f"{first} {middle} {last}"
            
            # Generate employee code
            employee_code = f"GV{2024}{i+1:04d}"
            
            # Generate email
            email = f"{first.lower()}.{last.lower()}{i+1}@university.edu.vn"
            
            # Random department and degree
            department = random.choice(departments)
            degree = random.choice(degrees)
            
            # Generate birth date (30-60 years old)
            birth_year = random.randint(1964, 1994)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            birth_date = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
            
            teacher_data = {
                "name": full_name,
                "employee_code": employee_code,
                "email": email,
                "phone": f"09{random.randint(10000000, 99999999)}",
                "department_id": department['id'],
                "degree_id": degree['id'],
                "position": random.choice(positions),
                "birth_date": birth_date,
                "base_salary": random.randint(8000000, 25000000),
                "hourly_rate": random.randint(100000, 300000),
                "qualifications": f"Chuyên ngành {random.choice(['Tin học', 'Toán', 'Vật lý', 'Hóa học', 'Sinh học', 'Kinh tế'])}"
            }
            
            try:
                response = self.session.post(
                    f"{self.base_url}/api/teachers",
                    json=teacher_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.created_data['teachers'].append(teacher_data)
                        created_count += 1
                        if created_count % 10 == 0:  # Log every 10 teachers
                            self.log(f"   ✅ Đã tạo {created_count} giảng viên...")
                    else:
                        self.log(f"   ⚠️  Lỗi tạo giảng viên {full_name}: {data.get('message', 'Unknown error')}")
                else:
                    self.log(f"   ❌ HTTP {response.status_code} cho {full_name}")
                    
            except Exception as e:
                self.log(f"   ❌ Exception tạo {full_name}: {str(e)}")
            
            time.sleep(0.05)  # Delay nhỏ hơn cho teachers
        
        self.log(f"👨‍🏫 Hoàn thành tạo {created_count} giảng viên")
        return created_count
    
    def create_subjects(self, count=100):
        """Tạo nhiều học phần"""
        self.log(f"📚 Tạo {count} học phần...")
        
        departments = self.get_existing_data()
        if not departments:
            self.log("❌ Cần có khoa trước khi tạo học phần")
            return 0
        
        # Subject prefixes by department type
        subject_prefixes = {
            "Công nghệ": ["Lập trình", "Cơ sở dữ liệu", "Mạng máy tính", "Hệ điều hành", "Trí tuệ nhân tạo", "Phát triển web", "Mobile"],
            "Toán": ["Giải tích", "Đại số", "Hình học", "Xác suất", "Thống kê", "Toán rời rạc", "Phương trình"],
            "Vật lý": ["Cơ học", "Điện từ", "Quang học", "Nhiệt học", "Vật lý hiện đại", "Thí nghiệm"],
            "Hóa": ["Hóa vô cơ", "Hóa hữu cơ", "Hóa phân tích", "Hóa lý", "Hóa sinh", "Thí nghiệm"],
            "Sinh": ["Di truyền", "Sinh thái", "Sinh lý", "Vi sinh", "Phân tử", "Tế bào"],
            "Kinh tế": ["Kinh tế vi mô", "Kinh tế vĩ mô", "Tài chính", "Marketing", "Quản lý", "Kế toán"],
            "Ngôn ngữ": ["Ngữ pháp", "Từ vựng", "Giao tiếp", "Văn học", "Dịch thuật", "Ngôn ngữ học"]
        }
        
        difficulty_levels = ["normal", "hard", "very_hard"]
        credits_options = [1, 2, 3, 4, 5]
        
        created_count = 0
        for i in range(count):
            # Pick random department
            department = random.choice(departments)
            dept_name = department['name']
            
            # Find matching subject category
            category = "Kinh tế"  # default
            for key in subject_prefixes.keys():
                if key in dept_name:
                    category = key
                    break
            
            # Generate subject name
            prefix = random.choice(subject_prefixes[category])
            level = random.choice(["cơ bản", "nâng cao", "ứng dụng", "chuyên sâu", "thực hành"])
            roman_num = random.choice(["I", "II", "III", "IV"])
            
            subject_name = f"{prefix} {level} {roman_num}"
            subject_code = f"{category[:2].upper()}{i+1:03d}"
            
            credits = random.choice(credits_options)
            theory_hours = credits * 15
            practice_hours = random.randint(0, credits * 5)
            
            subject_data = {
                "name": subject_name,
                "code": subject_code,
                "department_id": department['id'],
                "credits": credits,
                "theory_hours": theory_hours,
                "practice_hours": practice_hours,
                "subject_coefficient": round(random.uniform(1.0, 1.5), 1),
                "difficulty_level": random.choice(difficulty_levels),
                "description": f"Học phần {subject_name} thuộc {dept_name}"
            }
            
            try:
                response = self.session.post(
                    f"{self.base_url}/api/subjects",
                    json=subject_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.created_data['subjects'].append(subject_data)
                        created_count += 1
                        if created_count % 20 == 0:  # Log every 20 subjects
                            self.log(f"   ✅ Đã tạo {created_count} học phần...")
                    else:
                        self.log(f"   ⚠️  Lỗi tạo học phần {subject_name}: {data.get('message', 'Unknown error')}")
                else:
                    self.log(f"   ❌ HTTP {response.status_code} cho {subject_name}")
                    
            except Exception as e:
                self.log(f"   ❌ Exception tạo {subject_name}: {str(e)}")
            
            time.sleep(0.02)
        
        self.log(f"📚 Hoàn thành tạo {created_count} học phần")
        return created_count
    
    def create_semesters(self, count=10):
        """Tạo kỳ học cho nhiều năm"""
        self.log(f"📅 Tạo {count} kỳ học...")
        
        current_year = datetime.now().year
        semester_names = ["Kỳ 1", "Kỳ 2", "Kỳ hè"]
        
        created_count = 0
        year_start = current_year - 3  # Tạo từ 3 năm trước
        
        for year in range(year_start, current_year + 2):
            for semester_name in semester_names:
                if created_count >= count:
                    break
                
                # Set dates based on semester
                if semester_name == "Kỳ 1":
                    start_date = f"{year}-09-01"
                    end_date = f"{year+1 if year < current_year else year}-01-31"
                elif semester_name == "Kỳ 2":
                    start_date = f"{year}-02-01"
                    end_date = f"{year}-06-30"
                else:  # Kỳ hè
                    start_date = f"{year}-07-01"
                    end_date = f"{year}-08-31"
                
                is_current = (year == current_year and semester_name == "Kỳ 1")
                
                semester_data = {
                    "name": semester_name,
                    "year": year,
                    "start_date": start_date,
                    "end_date": end_date,
                    "is_current": is_current,
                    "description": f"{semester_name} năm học {year}-{year+1}"
                }
                
                try:
                    response = self.session.post(
                        f"{self.base_url}/api/semesters",
                        json=semester_data,
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success'):
                            self.created_data['semesters'].append(semester_data)
                            created_count += 1
                            self.log(f"   ✅ Tạo kỳ học: {semester_name} {year}")
                        else:
                            self.log(f"   ⚠️  Kỳ học đã tồn tại: {semester_name} {year}")
                    else:
                        self.log(f"   ❌ HTTP {response.status_code} cho {semester_name} {year}")
                        
                except Exception as e:
                    self.log(f"   ❌ Exception tạo {semester_name} {year}: {str(e)}")
                
                time.sleep(0.1)
            
            if created_count >= count:
                break
        
        self.log(f"📅 Hoàn thành tạo {created_count} kỳ học")
        return created_count
    
    def run_full_data_creation(self):
        """Chạy tạo toàn bộ dữ liệu mẫu"""
        self.log("🚀 BẮT ĐẦU TẠO DỮ LIỆU MẪU")
        self.log("=" * 50)
        
        start_time = time.time()
        
        # Check connection
        if not self.test_connection():
            self.log("❌ Không thể kết nối server. Thoát chương trình.")
            return False
        
        # Create data in order (dependencies)
        departments_count = self.create_departments(12)
        degrees_count = self.create_degrees(8)
        teachers_count = self.create_teachers(80)
        subjects_count = self.create_subjects(150)
        semesters_count = self.create_semesters(15)
        
        # Summary
        end_time = time.time()
        duration = end_time - start_time
        
        total_created = departments_count + degrees_count + teachers_count + subjects_count + semesters_count
        
        self.log("\n" + "=" * 50)
        self.log("📊 KẾT QUẢ TẠO DỮ LIỆU")
        self.log("=" * 50)
        self.log(f"⏱️  Thời gian: {duration:.2f} giây")
        self.log(f"🏢 Khoa: {departments_count}")
        self.log(f"🎓 Bằng cấp: {degrees_count}")
        self.log(f"👨‍🏫 Giảng viên: {teachers_count}")
        self.log(f"📚 Học phần: {subjects_count}")
        self.log(f"📅 Kỳ học: {semesters_count}")
        self.log(f"📝 Tổng cộng: {total_created} records")
        
        if total_created > 0:
            self.log("🎉 TẠO DỮ LIỆU THÀNH CÔNG!")
            self.log("\n💡 Bây giờ bạn có thể:")
            self.log("   - Chạy test_application.py để kiểm thử")
            self.log("   - Truy cập http://127.0.0.1:5000 để xem giao diện")
            self.log("   - Kiểm tra các trang thống kê")
        else:
            self.log("⚠️  Không tạo được dữ liệu nào!")
        
        return total_created > 0

def main():
    """Hàm main"""
    print("🎯 TẠO DỮ LIỆU MẪU CHO HỆ THỐNG QUẢN LÝ GIẢNG DẠY")
    print("=" * 55)
    
    creator = SampleDataCreator()
    success = creator.run_full_data_creation()
    
    if success:
        print("\n✅ HOÀN THÀNH!")
    else:
        print("\n❌ THẤT BẠI!")
    
    print("\n💡 Hướng dẫn:")
    print("   1. Đảm bảo server Flask đang chạy (python backend/app.py)")
    print("   2. Script này tạo dữ liệu thực tế, không phải test data")
    print("   3. Dữ liệu sẽ được lưu vào database thật")

if __name__ == "__main__":
    main()
