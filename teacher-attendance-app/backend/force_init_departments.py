"""
Script to force initialize departments and degrees data
Run this to ensure dropdown data exists
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from database import init_db, db
import models

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
app.config['SECRET_KEY'] = 'your-secret-key-here'

init_db(app)

def force_init_data():
    with app.app_context():
        print("Force initializing departments and degrees...")
        
        try:
            from models.degree import Degree
            from models.Department import Department
            
            # Create degrees
            default_degrees = [
                ('Đại học', 'ĐH', 1.3, 'Bằng cử nhân'),
                ('Thạc sĩ', 'ThS', 1.5, 'Bằng thạc sĩ'),
                ('Tiến sĩ', 'TS', 1.7, 'Bằng tiến sĩ'),
                ('Phó giáo sư', 'PGS', 2.0, 'Học hàm phó giáo sư'),
                ('Giáo sư', 'GS', 2.5, 'Học hàm giáo sư')
            ]
            
            for name, abbr, coeff, desc in default_degrees:
                existing = Degree.query.filter_by(name=name).first()
                if not existing:
                    degree = Degree(
                        name=name,
                        abbreviation=abbr,
                        coefficient=coeff,
                        description=desc
                    )
                    degree.save()
                    print(f"Created degree: {name}")
                else:
                    print(f"Degree already exists: {name}")
            
            # Create departments
            default_departments = [
                ('CNTT', 'Công nghệ thông tin', 'CNTT', 'Khoa Công nghệ thông tin'),
                ('DTVT', 'Điện tử viễn thông', 'ĐTVT', 'Khoa Điện tử viễn thông'),
                ('KTCN', 'Kỹ thuật cơ năng', 'KTCN', 'Khoa Kỹ thuật cơ năng'),
                ('KHCB', 'Khoa học cơ bản', 'KHCB', 'Khoa Khoa học cơ bản'),
                ('QLKT', 'Quản lý kinh tế', 'QLKT', 'Khoa Quản lý kinh tế')
            ]
            
            for code, name, abbr, desc in default_departments:
                existing = Department.query.filter_by(name=name).first()
                if not existing:
                    dept = Department(
                        code=code,
                        name=name,
                        abbreviation=abbr,
                        description=desc
                    )
                    dept.save()
                    print(f"Created department: {name}")
                else:
                    print(f"Department already exists: {name}")
            
            # Check results
            dept_count = Department.query.count()
            degree_count = Degree.query.count()
            print(f"Total departments: {dept_count}")
            print(f"Total degrees: {degree_count}")
            
            # List all departments
            departments = Department.query.all()
            print("All departments:")
            for dept in departments:
                print(f"  {dept.id}: {dept.name} ({dept.code})")
                
            # List all degrees
            degrees = Degree.query.all()
            print("All degrees:")
            for degree in degrees:
                print(f"  {degree.id}: {degree.name} ({degree.abbreviation}) - {degree.coefficient}")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    force_init_data()
