"""
Reset database script - tạo lại database từ đầu
"""
import os
import sqlite3
from datetime import datetime

def reset_database():
    """Reset database - xóa và tạo lại từ đầu"""
    
    # Path to database
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'teacher_attendance.db')
    
    # Delete existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️  Deleted existing database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔨 Creating new database schema...")
        
        # Create subjects table
        cursor.execute("""
            CREATE TABLE subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                subject_code VARCHAR(20),
                department VARCHAR(100) NOT NULL,
                credits INTEGER DEFAULT 3,
                theory_hours INTEGER DEFAULT 0,
                practice_hours INTEGER DEFAULT 0,
                student_count INTEGER DEFAULT 0,
                standard_rate NUMERIC(10, 2) DEFAULT 0,
                subject_coefficient NUMERIC(3, 2) DEFAULT 1.0,
                difficulty_level VARCHAR(20) DEFAULT 'normal',
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create teachers table
        cursor.execute("""
            CREATE TABLE teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                employee_code VARCHAR(20),
                email VARCHAR(100),
                phone VARCHAR(15),
                department VARCHAR(100) NOT NULL,
                position VARCHAR(100),
                qualifications VARCHAR(200),
                academic_rank VARCHAR(50),
                degree VARCHAR(50),
                degree_level VARCHAR(20) DEFAULT 'dai_hoc',
                employee_type VARCHAR(20) DEFAULT 'lecturer',
                base_salary NUMERIC(12, 2) DEFAULT 0,
                hourly_rate NUMERIC(10, 2) DEFAULT 100000,
                teacher_coefficient NUMERIC(3, 2) DEFAULT 1.3,
                is_active BOOLEAN DEFAULT 1,
                hire_date DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create semesters table
        cursor.execute("""
            CREATE TABLE semesters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                year INTEGER NOT NULL,
                academic_year VARCHAR(10),
                start_date DATE,
                end_date DATE,
                is_current BOOLEAN DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create assignments table
        cursor.execute("""
            CREATE TABLE assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                semester_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers (id),
                FOREIGN KEY (subject_id) REFERENCES subjects (id),
                FOREIGN KEY (semester_id) REFERENCES semesters (id)
            )
        """)
        
        # Create schedules table
        cursor.execute("""
            CREATE TABLE schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                teacher_id INTEGER NOT NULL,
                semester_id INTEGER NOT NULL,
                day_of_week VARCHAR(10) NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                classroom VARCHAR(50),
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects (id),
                FOREIGN KEY (teacher_id) REFERENCES teachers (id),
                FOREIGN KEY (semester_id) REFERENCES semesters (id)
            )
        """)
        
        # Create teaching_assignments table
        cursor.execute("""
            CREATE TABLE teaching_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                semester_id INTEGER,
                class_code VARCHAR(50) NOT NULL,
                class_student_count INTEGER DEFAULT 0,
                planned_hours INTEGER NOT NULL,
                actual_hours INTEGER DEFAULT 0,
                theory_hours INTEGER DEFAULT 0,
                practice_hours INTEGER DEFAULT 0,
                teacher_coefficient_override NUMERIC(3, 2),
                subject_coefficient_override NUMERIC(3, 2),
                hourly_rate_override NUMERIC(10, 2),
                adjusted_hours NUMERIC(8, 2) DEFAULT 0,
                total_amount NUMERIC(12, 2) DEFAULT 0,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                status VARCHAR(20) DEFAULT 'assigned',
                notes TEXT,
                is_approved BOOLEAN DEFAULT 0,
                approved_by INTEGER,
                approved_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers (id),
                FOREIGN KEY (subject_id) REFERENCES subjects (id),
                FOREIGN KEY (semester_id) REFERENCES semesters (id),
                FOREIGN KEY (approved_by) REFERENCES teachers (id)
            )
        """)
        
        # Create teaching_records table
        cursor.execute("""
            CREATE TABLE teaching_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id INTEGER NOT NULL,
                teaching_date DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                actual_duration INTEGER NOT NULL,
                lesson_topic VARCHAR(200),
                teaching_method VARCHAR(50),
                student_count INTEGER DEFAULT 0,
                notes TEXT,
                is_makeup_class BOOLEAN DEFAULT 0,
                is_confirmed BOOLEAN DEFAULT 0,
                confirmed_by INTEGER,
                confirmed_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assignment_id) REFERENCES teaching_assignments (id),
                FOREIGN KEY (confirmed_by) REFERENCES teachers (id)
            )
        """)
        
        # Create salary_calculations table
        cursor.execute("""
            CREATE TABLE salary_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                calculation_period VARCHAR(20) NOT NULL,
                calculation_type VARCHAR(20) DEFAULT 'monthly',
                base_salary NUMERIC(12, 2) DEFAULT 0,
                teaching_hours INTEGER DEFAULT 0,
                teaching_amount NUMERIC(12, 2) DEFAULT 0,
                position_allowance NUMERIC(12, 2) DEFAULT 0,
                research_bonus NUMERIC(12, 2) DEFAULT 0,
                overtime_amount NUMERIC(12, 2) DEFAULT 0,
                other_allowances NUMERIC(12, 2) DEFAULT 0,
                insurance_deduction NUMERIC(12, 2) DEFAULT 0,
                tax_deduction NUMERIC(12, 2) DEFAULT 0,
                other_deductions NUMERIC(12, 2) DEFAULT 0,
                gross_salary NUMERIC(12, 2) DEFAULT 0,
                net_salary NUMERIC(12, 2) DEFAULT 0,
                status VARCHAR(20) DEFAULT 'draft',
                notes TEXT,
                calculated_by INTEGER,
                calculated_at DATETIME,
                approved_by INTEGER,
                approved_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers (id),
                FOREIGN KEY (calculated_by) REFERENCES teachers (id),
                FOREIGN KEY (approved_by) REFERENCES teachers (id)
            )
        """)
        
        # Insert sample data
        print("📝 Inserting sample data...")
        
        # Sample subjects
        cursor.execute("""
            INSERT INTO subjects (name, department, student_count, subject_coefficient) VALUES
            ('Toán cao cấp A1', 'Toán học', 45, 1.0),
            ('Vật lý đại cương', 'Vật lý', 60, 1.2),
            ('Hóa học đại cương', 'Hóa học', 35, 1.1),
            ('Lập trình Python', 'Công nghệ thông tin', 50, 1.3),
            ('Kỹ thuật số', 'Điện tử', 40, 1.4)
        """)
        
        # Sample teachers
        cursor.execute("""
            INSERT INTO teachers (name, department, degree_level, teacher_coefficient, hourly_rate) VALUES
            ('Nguyễn Văn An', 'Toán học', 'tien_si', 1.7, 120000),
            ('Trần Thị Bình', 'Vật lý', 'thac_si', 1.5, 100000),
            ('Lê Văn Cường', 'Hóa học', 'pho_giao_su', 2.0, 150000),
            ('Phạm Thị Dung', 'Công nghệ thông tin', 'tien_si', 1.7, 130000),
            ('Hoàng Văn Em', 'Điện tử', 'thac_si', 1.5, 110000)
        """)
        
        # Sample semesters
        cursor.execute("""
            INSERT INTO semesters (name, year, is_current) VALUES
            ('Học kỳ 1', 2024, 1),
            ('Học kỳ 2', 2024, 0),
            ('Học kỳ hè', 2024, 0)
        """)
        
        conn.commit()
        print("✅ Database reset completed successfully!")
        print(f"Database location: {db_path}")
        
    except Exception as e:
        print(f"❌ Error during database reset: {e}")
        conn.rollback()
        
    finally:
        conn.close()

if __name__ == "__main__":
    confirm = input("Are you sure you want to reset the database? This will delete all data! (y/N): ")
    if confirm.lower() == 'y':
        reset_database()
    else:
        print("Database reset cancelled.")