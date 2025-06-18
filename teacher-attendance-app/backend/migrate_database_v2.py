"""
Migration script v2 - Tạo bảng degrees và departments nếu chưa tồn tại
"""
import sqlite3
import os
import sys

def migrate_database_v2():
    """Tạo và khởi tạo bảng degrees và departments"""
    
    # Lấy đường dẫn đến database
    current_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(current_dir, 'instance')
    database_path = os.path.join(instance_dir, 'teacher_attendance.db')
    
    # Kiểm tra nếu database không tồn tại
    if not os.path.exists(database_path):
        print("Database chưa tồn tại, sẽ tạo mới khi chạy app")
        return
    
    # Kết nối với database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        print("Bắt đầu migration database v2...")
        
        # 1. Tạo bảng degrees nếu chưa tồn tại
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS degrees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                abbreviation VARCHAR(20) NOT NULL,
                coefficient DECIMAL(3,2) NOT NULL DEFAULT 1.0,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 2. Tạo bảng departments nếu chưa tồn tại
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code VARCHAR(20) NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL UNIQUE,
                abbreviation VARCHAR(20) NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 3. Thêm dữ liệu mẫu cho degrees
        default_degrees = [
            ('Đại học', 'ĐH', 1.3, 'Bằng cử nhân'),
            ('Thạc sĩ', 'ThS', 1.5, 'Bằng thạc sĩ'),
            ('Tiến sĩ', 'TS', 1.7, 'Bằng tiến sĩ'),
            ('Phó giáo sư', 'PGS', 2.0, 'Học hàm phó giáo sư'),
            ('Giáo sư', 'GS', 2.5, 'Học hàm giáo sư')
        ]
        
        for degree in default_degrees:
            cursor.execute('''
                INSERT OR IGNORE INTO degrees (name, abbreviation, coefficient, description)
                VALUES (?, ?, ?, ?)
            ''', degree)
        
        # 4. Thêm dữ liệu mẫu cho departments
        default_departments = [
            ('CNTT', 'Công nghệ thông tin', 'CNTT', 'Khoa Công nghệ thông tin'),
            ('DTVT', 'Điện tử viễn thông', 'ĐTVT', 'Khoa Điện tử viễn thông'),
            ('KTCN', 'Kỹ thuật cơ năng', 'KTCN', 'Khoa Kỹ thuật cơ năng'),
            ('KHCB', 'Khoa học cơ bản', 'KHCB', 'Khoa Khoa học cơ bản'),
            ('QLKT', 'Quản lý kinh tế', 'QLKT', 'Khoa Quản lý kinh tế')
        ]
        
        for dept in default_departments:
            cursor.execute('''
                INSERT OR IGNORE INTO departments (code, name, abbreviation, description)
                VALUES (?, ?, ?, ?)
            ''', dept)
        
        # 5. Lưu thay đổi
        conn.commit()
        print("Migration v2 hoàn thành thành công!")
        
    except Exception as e:
        # Rollback nếu có lỗi
        conn.rollback()
        print(f"Lỗi migration: {e}")
    finally:
        # Đóng kết nối
        conn.close()

# Chạy migration nếu file được chạy trực tiếp
if __name__ == "__main__":
    migrate_database_v2()
        
    except Exception as e:
    conn.rollback()
    print(f"Lỗi migration v2: {e}")
    finally:
    conn.close()

if __name__ == "__main__":
    migrate_database_v2()
    SELECT d.id FROM departments d 
    WHERE d.name = teachers.department
    LIMIT 1
    ) WHERE department IS NOT NULL AND department != ''
    ''')
        
        # 3. Update subjects with department_id
        print("Updating subjects with department_id...")
        cursor.execute('''
    UPDATE subjects SET department_id = (
                SELECT d.id FROM departments d 
                WHERE d.name = subjects.department
                LIMIT 1
            ) WHERE department IS NOT NULL AND department != ''
    ''')
        
        # 4. Update teachers with degree_id based on degree_level
        print("Updating teachers with degree_id...")
        cursor.execute('''
    UPDATE teachers SET degree_id = (
                CASE 
                    WHEN degree_level = 'thac_si' THEN 2
                    WHEN degree_level = 'tien_si' THEN 3
                    WHEN degree_level = 'pho_giao_su' THEN 4
                    WHEN degree_level = 'giao_su' THEN 5
                    ELSE 1
                END
            ) WHERE degree_level IS NOT NULL
        ''')
conn.commit()
        print("Migration v2 hoàn thành! Đã sync dữ liệu existing.")
        
    except Exception as e:
        conn.rollback()
        print(f"Lỗi migration v2: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database_v2()
