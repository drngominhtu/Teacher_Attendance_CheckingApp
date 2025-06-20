"""
Migration script v3 - Cấu trúc mới và rõ ràng hơn
"""
import os
import sqlite3

def migrate_database():
    """Run database migration"""
    try:
        print("🔄 Starting database migration...")
        
        # Define the path to your SQLite database file
        database_path = os.path.join(os.path.dirname(__file__), 'instance', 'teacher_attendance.db')
        
        # Create instance directory if it doesn't exist
        instance_dir = os.path.dirname(database_path)
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)
        
        # Connect to database
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        # Create basic tables only
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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS class_sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code VARCHAR(20) UNIQUE NOT NULL,
                name VARCHAR(200) NOT NULL,
                subject_id INTEGER,
                semester_id INTEGER,
                teacher_id INTEGER,
                student_count INTEGER DEFAULT 0,
                max_students INTEGER DEFAULT 50,
                classroom VARCHAR(50),
                schedule_info VARCHAR(200),
                start_date DATE,
                end_date DATE,
                notes TEXT,
                status VARCHAR(20) DEFAULT 'planned',
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects (id),
                FOREIGN KEY (semester_id) REFERENCES semesters (id),
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
            )
        ''')
        
        # Create salary_settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salary_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key VARCHAR(50) UNIQUE NOT NULL,
                setting_value TEXT NOT NULL,
                description VARCHAR(200),
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Drop and recreate salary_calculations table to ensure all columns exist
        cursor.execute('DROP TABLE IF EXISTS salary_calculations')
        
        # Create salary_calculations table with all required columns
        cursor.execute('''
            CREATE TABLE salary_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                semester_id INTEGER,
                calculation_date DATE DEFAULT (date('now')),
                total_hours REAL DEFAULT 0,
                adjusted_hours REAL DEFAULT 0,
                total_amount REAL DEFAULT 0,
                base_hourly_rate REAL DEFAULT 100000,
                teacher_coefficient REAL DEFAULT 1.0,
                notes TEXT,
                is_approved BOOLEAN DEFAULT 0,
                approved_by VARCHAR(100),
                approved_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers (id),
                FOREIGN KEY (semester_id) REFERENCES semesters (id)
            )
        ''')
        
        print("✓ Recreated salary_calculations table with all columns")
        
        # Insert basic data
        degrees = [
            ('Đại học', 'ĐH', 1.3, 'Bằng cử nhân'),
            ('Thạc sĩ', 'ThS', 1.5, 'Bằng thạc sĩ'),
            ('Tiến sĩ', 'TS', 1.7, 'Bằng tiến sĩ')
        ]
        
        for name, abbr, coeff, desc in degrees:
            cursor.execute('''
            INSERT OR IGNORE INTO degrees (name, abbreviation, coefficient, description)
            VALUES (?, ?, ?, ?)
            ''', (name, abbr, coeff, desc))
        
        departments = [
            ('CNTT', 'Công nghệ thông tin', 'CNTT', 'Khoa Công nghệ thông tin'),
            ('DTVT', 'Điện tử viễn thông', 'ĐTVT', 'Khoa Điện tử viễn thông'),
            ('KTCN', 'Kỹ thuật cơ năng', 'KTCN', 'Khoa Kỹ thuật cơ năng')
        ]
        
        for code, name, abbr, desc in departments:
            cursor.execute('''
            INSERT OR IGNORE INTO departments (code, name, abbreviation, description)
            VALUES (?, ?, ?, ?)
            ''', (code, name, abbr, desc))
        
        # Check results
        cursor.execute("SELECT COUNT(*) FROM degrees")
        degree_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM departments")
        dept_count = cursor.fetchone()[0]
        
        conn.commit()
        print(f"Migration v3 hoàn thành! Đã có {degree_count} bằng cấp và {dept_count} khoa.")
        print("✓ Database migration completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

# Chỉ chạy nếu script được thực thi trực tiếp
# if __name__ == "__main__":
#     migrate_database()
#         print("✓ Database migration completed successfully")
#         return True
        
#     except Exception as e:
#         print(f"❌ Migration error: {e}")
#         if conn:
#             conn.rollback()
#     finally:
#         if conn:
#             conn.close()

# Chỉ chạy nếu script được thực thi trực tiếp
if __name__ == "__main__":
    migrate_database()
