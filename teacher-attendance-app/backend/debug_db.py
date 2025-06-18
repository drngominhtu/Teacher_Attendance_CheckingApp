"""
Debug script to check database and models
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from database import init_db, db

# Create app instance
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
template_folder = os.path.join(parent_dir, 'frontend', 'templates')
static_folder = os.path.join(parent_dir, 'frontend', 'static')
instance_dir = os.path.join(current_dir, 'instance')

app = Flask(__name__, 
            template_folder=template_folder,
            static_folder=static_folder,
            instance_relative_config=True)

database_path = os.path.join(instance_dir, 'teacher_attendance.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'debug-key'

init_db(app)

def debug_database():
    with app.app_context():
        print("=== DATABASE DEBUG ===")
        print(f"Database path: {database_path}")
        print(f"Database exists: {os.path.exists(database_path)}")
        
        try:
            # Check tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tables in database: {tables}")
            
            # Try to import models
            print("\n=== IMPORTING MODELS ===")
            
            try:
                from models.degree import Degree
                count = Degree.query.count()
                print(f"✓ Degree model: {count} records")
                
                if count == 0:
                    print("  Creating default degrees...")
                    defaults = [
                        ('Đại học', 'ĐH', 1.3, 'Bằng cử nhân'),
                        ('Thạc sĩ', 'ThS', 1.5, 'Bằng thạc sĩ'),
                        ('Tiến sĩ', 'TS', 1.7, 'Bằng tiến sĩ')
                    ]
                    
                    for name, abbr, coeff, desc in defaults:
                        degree = Degree(name=name, abbreviation=abbr, coefficient=coeff, description=desc)
                        db.session.add(degree)
                    
                    db.session.commit()
                    print(f"  ✓ Created {len(defaults)} degrees")
                
            except Exception as e:
                print(f"✗ Degree model error: {e}")
            
            try:
                from models.Department import Department
                count = Department.query.count()
                print(f"✓ Department model: {count} records")
                
                if count == 0:
                    print("  Creating default departments...")
                    defaults = [
                        ('CNTT', 'Công nghệ thông tin', 'CNTT'),
                        ('DTVT', 'Điện tử viễn thông', 'ĐTVT'),
                        ('KTCN', 'Kỹ thuật cơ năng', 'KTCN')
                    ]
                    
                    for code, name, abbr in defaults:
                        dept = Department(code=code, name=name, abbreviation=abbr, description=f'Khoa {name}')
                        db.session.add(dept)
                    
                    db.session.commit()
                    print(f"  ✓ Created {len(defaults)} departments")
                
            except Exception as e:
                print(f"✗ Department model error: {e}")
            
            try:
                from models.teacher import Teacher
                count = Teacher.query.count()
                print(f"✓ Teacher model: {count} records")
            except Exception as e:
                print(f"✗ Teacher model error: {e}")
            
            print("\n=== FINAL CHECK ===")
            from models.degree import Degree
            from models.Department import Department
            from models.teacher import Teacher
            
            degrees = Degree.query.all()
            departments = Department.query.all()
            teachers = Teacher.query.all()
            
            print(f"Final counts:")
            print(f"  Degrees: {len(degrees)}")
            print(f"  Departments: {len(departments)}")
            print(f"  Teachers: {len(teachers)}")
            
            print(f"\nDegree details:")
            for d in degrees:
                print(f"  {d.id}: {d.name} ({d.abbreviation}) - {d.coefficient}")
            
            print(f"\nDepartment details:")
            for d in departments:
                print(f"  {d.id}: {d.name} ({d.code})")
            
        except Exception as e:
            print(f"Database error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_database()
