"""
Fix existing data with invalid enum values
"""
import sqlite3
import os

def fix_enum_data():
    """Fix invalid enum values in database"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'teacher_attendance.db')
    
    if not os.path.exists(db_path):
        print("Database doesn't exist.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔧 Fixing enum values in database...")
        
        # Fix degree_level values
        valid_degrees = ['dai_hoc', 'thac_si', 'tien_si', 'pho_giao_su', 'giao_su']
        
        # Get all teachers with invalid degree_level
        cursor.execute("SELECT id, degree_level FROM teachers WHERE degree_level IS NOT NULL")
        teachers = cursor.fetchall()
        
        fixed_count = 0
        for teacher_id, degree_level in teachers:
            if degree_level not in valid_degrees:
                print(f"Fixing teacher {teacher_id}: {degree_level} -> dai_hoc")
                cursor.execute("UPDATE teachers SET degree_level = 'dai_hoc' WHERE id = ?", (teacher_id,))
                fixed_count += 1
        
        # Fix employee_type values
        valid_employee_types = ['lecturer', 'admin_staff', 'researcher', 'manager']
        
        cursor.execute("SELECT id, employee_type FROM teachers WHERE employee_type IS NOT NULL")
        teachers = cursor.fetchall()
        
        for teacher_id, employee_type in teachers:
            if employee_type not in valid_employee_types:
                print(f"Fixing teacher {teacher_id} employee_type: {employee_type} -> lecturer")
                cursor.execute("UPDATE teachers SET employee_type = 'lecturer' WHERE id = ?", (teacher_id,))
                fixed_count += 1
        
        # Update teacher coefficients based on degree_level
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
        
        conn.commit()
        print(f"✅ Fixed {fixed_count} enum values!")
        print("✅ Updated teacher coefficients!")
        
    except Exception as e:
        print(f"❌ Error fixing enum data: {e}")
        conn.rollback()
        
    finally:
        conn.close()

if __name__ == "__main__":
    fix_enum_data()