"""
Script để khởi tạo dữ liệu ban đầu cho database (khoa, bằng cấp)
"""
import os
import sqlite3
from datetime import datetime

def setup_initial_data():
    """Tạo và cài đặt dữ liệu ban đầu cho database"""
    
    # Đường dẫn database
    current_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(current_dir, 'instance')
    database_path = os.path.join(instance_dir, 'teacher_attendance.db')
    
    # Kiểm tra database
    if not os.path.exists(database_path):
        print("Database chưa tồn tại. Tạo instance directory...")
        os.makedirs(instance_dir, exist_ok=True)
    
    # Kết nối database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        print("Bắt đầu cài đặt dữ liệu ban đầu...")
        
        # Tạo bảng degrees
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
        
        # Tạo bảng departments
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
        
        # Thêm dữ liệu mẫu cho degrees
        degrees = [
            ('Đại học', 'ĐH', 1.3, 'Bằng cử nhân'),
            ('Thạc sĩ', 'ThS', 1.5, 'Bằng thạc sĩ'),
            ('Tiến sĩ', 'TS', 1.7, 'Bằng tiến sĩ'),
            ('Phó giáo sư', 'PGS', 2.0, 'Học hàm phó giáo sư'),
            ('Giáo sư', 'GS', 2.5, 'Học hàm giáo sư')
        ]
        
        for name, abbr, coeff, desc in degrees:
            cursor.execute('''
                INSERT OR IGNORE INTO degrees (name, abbreviation, coefficient, description)
                VALUES (?, ?, ?, ?)
            ''', (name, abbr, coeff, desc))
        
        # Thêm dữ liệu mẫu cho departments
        departments = [
            ('CNTT', 'Công nghệ thông tin', 'CNTT', 'Khoa Công nghệ thông tin'),
            ('DTVT', 'Điện tử viễn thông', 'ĐTVT', 'Khoa Điện tử viễn thông'),
            ('KTCN', 'Kỹ thuật cơ năng', 'KTCN', 'Khoa Kỹ thuật cơ năng'),
            ('KHCB', 'Khoa học cơ bản', 'KHCB', 'Khoa Khoa học cơ bản'),
            ('QLKT', 'Quản lý kinh tế', 'QLKT', 'Khoa Quản lý kinh tế')
        ]
        
        for code, name, abbr, desc in departments:
            cursor.execute('''
                INSERT OR IGNORE INTO departments (code, name, abbreviation, description)
                VALUES (?, ?, ?, ?)
            ''', (code, name, abbr, desc))
        
        # Lưu thay đổi
        conn.commit()
        
        # Kiểm tra kết quả
        cursor.execute("SELECT COUNT(*) FROM degrees")
        degree_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM departments")
        dept_count = cursor.fetchone()[0]
        
        print(f"Cài đặt thành công! Đã tạo {degree_count} bằng cấp và {dept_count} khoa.")
        
    except Exception as e:
        conn.rollback()
        print(f"Lỗi cài đặt: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_initial_data()
