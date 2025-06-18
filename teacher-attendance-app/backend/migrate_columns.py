"""
Migration script to add missing columns to existing database
"""
import sqlite3
import os

def migrate_columns():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(current_dir, 'instance')
    database_path = os.path.join(instance_dir, 'teacher_attendance.db')
    
    if not os.path.exists(database_path):
        print("Database does not exist yet")
        return
    
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        print("Starting column migration...")
        
        # Check current teachers table structure
        cursor.execute("PRAGMA table_info(teachers)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        print(f"Existing teacher columns: {existing_columns}")
        
        # Add missing columns to teachers table
        missing_columns = {
            'birth_date': 'DATE',
            'department_id': 'INTEGER DEFAULT 1',
            'degree_id': 'INTEGER DEFAULT 1',
            'teacher_coefficient_override': 'DECIMAL(3,2)',
            'hire_date': 'DATETIME'
        }
        
        for column, data_type in missing_columns.items():
            if column not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE teachers ADD COLUMN {column} {data_type}")
                    print(f"✓ Added column: {column}")
                except Exception as e:
                    print(f"✗ Error adding {column}: {e}")
        
        # Check subjects table
        cursor.execute("PRAGMA table_info(subjects)")
        existing_subject_columns = [col[1] for col in cursor.fetchall()]
        print(f"Existing subject columns: {existing_subject_columns}")
        
        # Add missing columns to subjects table
        subject_missing_columns = {
            'code': 'VARCHAR(20)',
            'department_id': 'INTEGER DEFAULT 1',
            'total_hours': 'INTEGER DEFAULT 0',
            'subject_coefficient': 'DECIMAL(3,2) DEFAULT 1.0',
            'difficulty_level': 'VARCHAR(20) DEFAULT "normal"',
            'prerequisites': 'TEXT'
        }
        
        for column, data_type in subject_missing_columns.items():
            if column not in existing_subject_columns:
                try:
                    cursor.execute(f"ALTER TABLE subjects ADD COLUMN {column} {data_type}")
                    print(f"✓ Added subject column: {column}")
                except Exception as e:
                    print(f"✗ Error adding subject {column}: {e}")
        
        conn.commit()
        print("✓ Column migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Migration error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_columns()
