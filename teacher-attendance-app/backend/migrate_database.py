"""
Database migration script to update existing database schema
"""
import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Migrate existing database to new schema"""
    
    # Path to database
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'teacher_attendance.db')
    
    if not os.path.exists(db_path):
        print("Database doesn't exist. It will be created when you run the app.")
        return
    
    print(f"Migrating database at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Function to add column if not exists
        def add_column_if_not_exists(table_name, column_name, column_type, default_value=None):
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            if column_name not in columns:
                if default_value:
                    cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT {default_value}')
                else:
                    cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}')
                print(f"Added column {column_name} to {table_name}")
                return True
            return False
        
        # Check current schema for subjects table
        cursor.execute("PRAGMA table_info(subjects)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Current subjects columns: {columns}")
        
        # Add missing columns to subjects table
        subject_changes = []
        
        if add_column_if_not_exists('subjects', 'subject_code', 'VARCHAR(20)'):
            subject_changes.append('subject_code')
        if add_column_if_not_exists('subjects', 'credits', 'INTEGER', '3'):
            subject_changes.append('credits')
        if add_column_if_not_exists('subjects', 'theory_hours', 'INTEGER', '0'):
            subject_changes.append('theory_hours')
        if add_column_if_not_exists('subjects', 'practice_hours', 'INTEGER', '0'):
            subject_changes.append('practice_hours')
        if add_column_if_not_exists('subjects', 'standard_rate', 'NUMERIC(10, 2)', '0'):
            subject_changes.append('standard_rate')
        if add_column_if_not_exists('subjects', 'subject_coefficient', 'NUMERIC(3, 2)', '1.0'):
            subject_changes.append('subject_coefficient')
        if add_column_if_not_exists('subjects', 'difficulty_level', 'VARCHAR(20)', '"normal"'):
            subject_changes.append('difficulty_level')
        if add_column_if_not_exists('subjects', 'description', 'TEXT'):
            subject_changes.append('description')
        if add_column_if_not_exists('subjects', 'is_active', 'BOOLEAN', '1'):
            subject_changes.append('is_active')
        if add_column_if_not_exists('subjects', 'created_at', 'DATETIME', f'"{datetime.now().isoformat()}"'):
            subject_changes.append('created_at')
        if add_column_if_not_exists('subjects', 'updated_at', 'DATETIME', f'"{datetime.now().isoformat()}"'):
            subject_changes.append('updated_at')
        
        # Check teachers table
        cursor.execute("PRAGMA table_info(teachers)")
        teacher_columns = [col[1] for col in cursor.fetchall()]
        print(f"Current teachers columns: {teacher_columns}")
        
        # Add missing columns to teachers table
        teacher_changes = []
        
        if add_column_if_not_exists('teachers', 'employee_code', 'VARCHAR(20)'):
            teacher_changes.append('employee_code')
        if add_column_if_not_exists('teachers', 'email', 'VARCHAR(100)'):
            teacher_changes.append('email')
        if add_column_if_not_exists('teachers', 'phone', 'VARCHAR(15)'):
            teacher_changes.append('phone')
        if add_column_if_not_exists('teachers', 'position', 'VARCHAR(100)'):
            teacher_changes.append('position')
        if add_column_if_not_exists('teachers', 'academic_rank', 'VARCHAR(50)'):
            teacher_changes.append('academic_rank')
        if add_column_if_not_exists('teachers', 'degree', 'VARCHAR(50)'):
            teacher_changes.append('degree')
        if add_column_if_not_exists('teachers', 'degree_level', 'VARCHAR(20)', '"dai_hoc"'):
            teacher_changes.append('degree_level')
        if add_column_if_not_exists('teachers', 'employee_type', 'VARCHAR(20)', '"lecturer"'):
            teacher_changes.append('employee_type')
        if add_column_if_not_exists('teachers', 'base_salary', 'NUMERIC(12, 2)', '0'):
            teacher_changes.append('base_salary')
        if add_column_if_not_exists('teachers', 'hourly_rate', 'NUMERIC(10, 2)', '100000'):
            teacher_changes.append('hourly_rate')
        if add_column_if_not_exists('teachers', 'teacher_coefficient', 'NUMERIC(3, 2)', '1.3'):
            teacher_changes.append('teacher_coefficient')
        if add_column_if_not_exists('teachers', 'is_active', 'BOOLEAN', '1'):
            teacher_changes.append('is_active')
        if add_column_if_not_exists('teachers', 'hire_date', 'DATETIME'):
            teacher_changes.append('hire_date')
        if add_column_if_not_exists('teachers', 'created_at', 'DATETIME', f'"{datetime.now().isoformat()}"'):
            teacher_changes.append('created_at')
        if add_column_if_not_exists('teachers', 'updated_at', 'DATETIME', f'"{datetime.now().isoformat()}"'):
            teacher_changes.append('updated_at')
        
        # Check semesters table
        cursor.execute("PRAGMA table_info(semesters)")
        semester_columns = [col[1] for col in cursor.fetchall()]
        print(f"Current semesters columns: {semester_columns}")
        
        # Add missing columns to semesters table
        semester_changes = []
        
        if add_column_if_not_exists('semesters', 'academic_year', 'VARCHAR(10)'):
            semester_changes.append('academic_year')
        if add_column_if_not_exists('semesters', 'start_date', 'DATE'):
            semester_changes.append('start_date')
        if add_column_if_not_exists('semesters', 'end_date', 'DATE'):
            semester_changes.append('end_date')
        if add_column_if_not_exists('semesters', 'is_current', 'BOOLEAN', '0'):
            semester_changes.append('is_current')
        if add_column_if_not_exists('semesters', 'is_active', 'BOOLEAN', '1'):
            semester_changes.append('is_active')
        if add_column_if_not_exists('semesters', 'created_at', 'DATETIME', f'"{datetime.now().isoformat()}"'):
            semester_changes.append('created_at')
        if add_column_if_not_exists('semesters', 'updated_at', 'DATETIME', f'"{datetime.now().isoformat()}"'):
            semester_changes.append('updated_at')
        
        # Check assignments table
        cursor.execute("PRAGMA table_info(assignments)")
        assignment_columns = [col[1] for col in cursor.fetchall()]
        print(f"Current assignments columns: {assignment_columns}")
        
        # Add missing columns to assignments table
        assignment_changes = []
        
        if add_column_if_not_exists('assignments', 'created_at', 'DATETIME', f'"{datetime.now().isoformat()}"'):
            assignment_changes.append('created_at')
        if add_column_if_not_exists('assignments', 'updated_at', 'DATETIME', f'"{datetime.now().isoformat()}"'):
            assignment_changes.append('updated_at')
        
        # Create teaching_assignments table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teaching_assignments (
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
        
        # Create teaching_records table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teaching_records (
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
        
        # Create salary_calculations table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salary_calculations (
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
        
        # Commit changes
        conn.commit()
        
        print("✅ Database migration completed successfully!")
        if subject_changes:
            print(f"Added columns to subjects: {subject_changes}")
        if teacher_changes:
            print(f"Added columns to teachers: {teacher_changes}")
        if semester_changes:
            print(f"Added columns to semesters: {semester_changes}")
        if assignment_changes:
            print(f"Added columns to assignments: {assignment_changes}")
        
        # Update existing records with timestamps if they're NULL
        current_time = datetime.now().isoformat()
        
        # Update subjects
        cursor.execute("UPDATE subjects SET created_at = ? WHERE created_at IS NULL", (current_time,))
        cursor.execute("UPDATE subjects SET updated_at = ? WHERE updated_at IS NULL", (current_time,))
        
        # Update teachers
        cursor.execute("UPDATE teachers SET created_at = ? WHERE created_at IS NULL", (current_time,))
        cursor.execute("UPDATE teachers SET updated_at = ? WHERE updated_at IS NULL", (current_time,))
        
        # Update semesters
        cursor.execute("UPDATE semesters SET created_at = ? WHERE created_at IS NULL", (current_time,))
        cursor.execute("UPDATE semesters SET updated_at = ? WHERE updated_at IS NULL", (current_time,))
        
        # Update assignments
        cursor.execute("UPDATE assignments SET created_at = ? WHERE created_at IS NULL", (current_time,))
        cursor.execute("UPDATE assignments SET updated_at = ? WHERE updated_at IS NULL", (current_time,))
        
        # Update teacher coefficients based on degree_level
        print("Updating teacher coefficients...")
        cursor.execute("""
            UPDATE teachers 
            SET teacher_coefficient = CASE 
                WHEN degree_level = 'dai_hoc' THEN 1.3
                WHEN degree_level = 'thac_si' THEN 1.5
                WHEN degree_level = 'tien_si' THEN 1.7
                WHEN degree_level = 'pho_giao_su' THEN 2.0
                WHEN degree_level = 'giao_su' THEN 2.5
                ELSE 1.3
            END
        """)
        
        # Set default hourly rate if not set
        cursor.execute("UPDATE teachers SET hourly_rate = 100000 WHERE hourly_rate = 0 OR hourly_rate IS NULL")
        
        conn.commit()
        print("✅ Updated teacher coefficients, hourly rates, and timestamps!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
        
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()