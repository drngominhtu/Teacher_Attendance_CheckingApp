"""
Script to recreate database from scratch with proper structure
"""
import os
import sqlite3
from datetime import datetime

def recreate_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(current_dir, 'instance')
    database_path = os.path.join(instance_dir, 'teacher_attendance.db')
    
    # Remove old database
    if os.path.exists(database_path):
        os.remove(database_path)
        print("✓ Removed old database")
    
    # Ensure instance directory exists
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    
    # Create new database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        print("Creating fresh database with all tables...")
        
        # Create degrees table
        cursor.execute('''
            CREATE TABLE degrees (
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
        
        # Create departments table
        cursor.execute('''
            CREATE TABLE departments (
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
        
        # Create teachers table with all columns
        cursor.execute('''
            CREATE TABLE teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_code VARCHAR(20) UNIQUE,
                name VARCHAR(100) NOT NULL,
                birth_date DATE,
                phone VARCHAR(15),
                email VARCHAR(100) UNIQUE,
                department VARCHAR(100),
                degree_level VARCHAR(20) DEFAULT 'dai_hoc',
                department_id INTEGER DEFAULT 1,
                degree_id INTEGER DEFAULT 1,
                position VARCHAR(100),
                qualifications VARCHAR(200),
                academic_rank VARCHAR(50),
                employee_type VARCHAR(20) DEFAULT 'lecturer',
                base_salary DECIMAL(12,2) DEFAULT 0,
                hourly_rate DECIMAL(10,2) DEFAULT 100000,
                teacher_coefficient DECIMAL(3,2) DEFAULT 1.3,
                teacher_coefficient_override DECIMAL(3,2),
                is_active BOOLEAN DEFAULT 1,
                hire_date DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id),
                FOREIGN KEY (degree_id) REFERENCES degrees(id)
            )
        ''')
        
        # Create subjects table
        cursor.execute('''
            CREATE TABLE subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(20),
                subject_code VARCHAR(20),
                department VARCHAR(100),
                department_id INTEGER DEFAULT 1,
                credits INTEGER DEFAULT 3,
                theory_hours INTEGER DEFAULT 0,
                practice_hours INTEGER DEFAULT 0,
                total_hours INTEGER DEFAULT 0,
                subject_coefficient DECIMAL(3,2) DEFAULT 1.0,
                difficulty_level VARCHAR(20) DEFAULT 'normal',
                description TEXT,
                prerequisites TEXT,
                student_count INTEGER DEFAULT 0,
                standard_rate DECIMAL(10,2) DEFAULT 100000,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
        ''')
        
        # Create semesters table
        cursor.execute('''
            CREATE TABLE semesters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                year INTEGER NOT NULL,
                academic_year VARCHAR(20),
                start_date DATE,
                end_date DATE,
                is_current BOOLEAN DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create assignments table
        cursor.execute('''
            CREATE TABLE assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                semester_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id),
                FOREIGN KEY (subject_id) REFERENCES subjects(id),
                FOREIGN KEY (semester_id) REFERENCES semesters(id)
            )
        ''')
        
        # Insert default degrees
        default_degrees = [
            ('Đại học', 'ĐH', 1.3, 'Bằng cử nhân'),
            ('Thạc sĩ', 'ThS', 1.5, 'Bằng thạc sĩ'),
            ('Tiến sĩ', 'TS', 1.7, 'Bằng tiến sĩ'),
            ('Phó giáo sư', 'PGS', 2.0, 'Học hàm phó giáo sư'),
            ('Giáo sư', 'GS', 2.5, 'Học hàm giáo sư')
        ]
        
        for name, abbr, coeff, desc in default_degrees:
            cursor.execute('''
                INSERT INTO degrees (name, abbreviation, coefficient, description)
                VALUES (?, ?, ?, ?)
            ''', (name, abbr, coeff, desc))
        
        # Insert default departments
        default_departments = [
            ('CNTT', 'Công nghệ thông tin', 'CNTT', 'Khoa Công nghệ thông tin'),
            ('DTVT', 'Điện tử viễn thông', 'ĐTVT', 'Khoa Điện tử viễn thông'),
            ('KTCN', 'Kỹ thuật cơ năng', 'KTCN', 'Khoa Kỹ thuật cơ năng'),
            ('KHCB', 'Khoa học cơ bản', 'KHCB', 'Khoa Khoa học cơ bản'),
            ('QLKT', 'Quản lý kinh tế', 'QLKT', 'Khoa Quản lý kinh tế')
        ]
        
        for code, name, abbr, desc in default_departments:
            cursor.execute('''
                INSERT INTO departments (code, name, abbreviation, description)
                VALUES (?, ?, ?, ?)
            ''', (code, name, abbr, desc))
        
        # Insert default semesters
        current_year = datetime.now().year
        default_semesters = [
            (f'Học kỳ 1', current_year, f'{current_year}-{current_year+1}', f'{current_year}-09-01', f'{current_year+1}-01-15', 1),
            (f'Học kỳ 2', current_year, f'{current_year}-{current_year+1}', f'{current_year+1}-01-16', f'{current_year+1}-06-30', 0),
            (f'Học kỳ hè', current_year, f'{current_year}-{current_year+1}', f'{current_year+1}-07-01', f'{current_year+1}-08-31', 0)
        ]
        
        for name, year, academic_year, start_date, end_date, is_current in default_semesters:
            cursor.execute('''
                INSERT INTO semesters (name, year, academic_year, start_date, end_date, is_current)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, year, academic_year, start_date, end_date, is_current))
        
        conn.commit()
        print("✓ Database recreated successfully with sample data!")
        
        # Verify data
        cursor.execute("SELECT COUNT(*) FROM degrees")
        degree_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM departments")
        dept_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM semesters")
        semester_count = cursor.fetchone()[0]
        
        print(f"Created: {degree_count} degrees, {dept_count} departments, {semester_count} semesters")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error creating database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    recreate_database()
