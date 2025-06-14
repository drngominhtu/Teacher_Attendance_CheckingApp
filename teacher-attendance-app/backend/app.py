from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Get paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
template_folder = os.path.join(parent_dir, 'frontend', 'templates')
static_folder = os.path.join(parent_dir, 'frontend', 'static')

# Create instance directory for database
instance_dir = os.path.join(current_dir, 'instance')
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

# Initialize Flask app
app = Flask(__name__, 
            template_folder=template_folder,
            static_folder=static_folder,
            instance_relative_config=True)

# Configuration - Use absolute path for database
database_path = os.path.join(instance_dir, 'teacher_attendance.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize database
db = SQLAlchemy(app)

# Models
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    student_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'student_count': self.student_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Semester(db.Model):
    __tablename__ = 'semesters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    qualifications = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'qualifications': self.qualifications,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    teacher = db.relationship('Teacher', backref='assignments')
    subject = db.relationship('Subject', backref='assignments')
    semester = db.relationship('Semester', backref='assignments')

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'subject_id': self.subject_id,
            'semester_id': self.semester_id,
            'teacher_name': self.teacher.name if self.teacher else None,
            'subject_name': self.subject.name if self.subject else None,
            'semester_name': self.semester.name if self.semester else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Routes
@app.route('/')
def index():
    try:
        subjects_count = Subject.query.count()
        semesters_count = Semester.query.count()
        teachers_count = Teacher.query.count()
        assignments_count = Assignment.query.count()
        total_students = db.session.query(db.func.sum(Subject.student_count)).scalar() or 0
        
        return render_template('index.html', 
                             subjects_count=subjects_count,
                             semesters_count=semesters_count, 
                             teachers_count=teachers_count,
                             assignments_count=assignments_count,
                             total_students=total_students)
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template('index.html', 
                             subjects_count=0,
                             semesters_count=0, 
                             teachers_count=0,
                             assignments_count=0,
                             total_students=0)

@app.route('/subjects')
def subjects():
    try:
        subjects_list = Subject.query.order_by(Subject.created_at.desc()).all()
        return render_template('subjects.html', subjects=subjects_list)
    except Exception as e:
        print(f"Error in subjects route: {e}")
        return render_template('subjects.html', subjects=[])

@app.route('/semesters')
def semesters():
    try:
        semesters_list = Semester.query.order_by(Semester.created_at.desc()).all()
        current_year = datetime.now().year
        return render_template('semesters.html', semesters=semesters_list, current_year=current_year)
    except Exception as e:
        print(f"Error in semesters route: {e}")
        return render_template('semesters.html', semesters=[], current_year=datetime.now().year)

@app.route('/schedules')
def schedules():
    return render_template('schedules.html')

@app.route('/teachers')
def teachers():
    try:
        teachers_list = Teacher.query.order_by(Teacher.created_at.desc()).all()
        return render_template('teachers.html', teachers=teachers_list)
    except Exception as e:
        print(f"Error in teachers route: {e}")
        return render_template('teachers.html', teachers=[])

@app.route('/assignments')
def assignments():
    try:
        assignments_list = Assignment.query.order_by(Assignment.created_at.desc()).all()
        teachers_list = Teacher.query.all()
        subjects_list = Subject.query.all()
        semesters_list = Semester.query.all()
        return render_template('assignments.html', 
                             assignments=assignments_list,
                             teachers=teachers_list,
                             subjects=subjects_list,
                             semesters=semesters_list)
    except Exception as e:
        print(f"Error in assignments route: {e}")
        return render_template('assignments.html', 
                             assignments=[],
                             teachers=[],
                             subjects=[],
                             semesters=[])

# API Routes
@app.route('/api/subjects', methods=['POST'])
def create_subject():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug log
        
        if not data:
            return jsonify({'success': False, 'message': 'Không có dữ liệu được gửi'})
        
        name = data.get('name', '').strip()
        department = data.get('department', '').strip()
        student_count = data.get('student_count', 0)
        
        if not name or not department:
            return jsonify({'success': False, 'message': 'Tên học phần và khoa không được để trống'})
        
        # Check for existing subject
        existing = Subject.query.filter_by(name=name, department=department).first()
        if existing:
            return jsonify({'success': False, 'message': 'Học phần này đã tồn tại'})
        
        subject = Subject(
            name=name,
            department=department,
            student_count=int(student_count) if student_count else 0
        )
        
        db.session.add(subject)
        db.session.commit()
        
        print(f"Subject created successfully: {subject.to_dict()}")  # Debug log
        return jsonify({'success': True, 'message': 'Học phần đã được tạo'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating subject: {e}")
        return jsonify({'success': False, 'message': f'Lỗi hệ thống: {str(e)}'})

@app.route('/api/subjects/<int:id>', methods=['PUT'])
def update_subject(id):
    try:
        subject = Subject.query.get_or_404(id)
        data = request.get_json()
        
        subject.name = data['name']
        subject.department = data['department']
        subject.student_count = int(data.get('student_count', 0))
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Học phần đã được cập nhật'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating subject: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/subjects/<int:id>', methods=['DELETE'])
def delete_subject(id):
    try:
        subject = Subject.query.get_or_404(id)
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Học phần đã được xóa'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting subject: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teachers', methods=['POST'])
def create_teacher():
    try:
        data = request.get_json()
        
        existing = Teacher.query.filter_by(
            name=data['name'], 
            department=data['department']
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'Giảng viên này đã tồn tại'})
        
        teacher = Teacher(
            name=data['name'],
            department=data['department'],
            qualifications=data.get('qualifications', '')
        )
        
        db.session.add(teacher)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Giảng viên đã được tạo'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating teacher: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teachers/<int:id>', methods=['PUT'])
def update_teacher(id):
    try:
        teacher = Teacher.query.get_or_404(id)
        data = request.get_json()
        
        teacher.name = data['name']
        teacher.department = data['department']
        teacher.qualifications = data.get('qualifications', '')
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Giảng viên đã được cập nhật'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating teacher: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teachers/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    try:
        teacher = Teacher.query.get_or_404(id)
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Giảng viên đã được xóa'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting teacher: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/semesters', methods=['POST'])
def create_semester():
    try:
        data = request.get_json()
        
        existing = Semester.query.filter_by(
            name=data['name'], 
            year=int(data['year'])
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'Kì học này đã tồn tại'})
        
        semester = Semester(
            name=data['name'], 
            year=int(data['year'])
        )
        
        db.session.add(semester)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Kì học đã được tạo'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating semester: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/semesters/<int:id>', methods=['PUT'])
def update_semester(id):
    try:
        semester = Semester.query.get_or_404(id)
        data = request.get_json()
        
        semester.name = data['name']
        semester.year = int(data['year'])
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Kì học đã được cập nhật'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating semester: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/semesters/<int:id>', methods=['DELETE'])
def delete_semester(id):
    try:
        semester = Semester.query.get_or_404(id)
        db.session.delete(semester)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Kì học đã được xóa'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting semester: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/assignments', methods=['POST'])
def create_assignment():
    try:
        data = request.get_json()
        
        existing = Assignment.query.filter_by(
            teacher_id=data['teacher_id'],
            subject_id=data['subject_id'],
            semester_id=data.get('semester_id')
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'Phân công này đã tồn tại'})
        
        assignment = Assignment(
            teacher_id=data['teacher_id'],
            subject_id=data['subject_id'],
            semester_id=data.get('semester_id')
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Phân công đã được tạo'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/assignments/<int:id>', methods=['DELETE'])
def delete_assignment(id):
    try:
        assignment = Assignment.query.get_or_404(id)
        db.session.delete(assignment)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Phân công đã được xóa'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

def init_database():
    """Initialize database and create tables"""
    try:
        print(f"Database path: {database_path}")
        print(f"Instance directory: {instance_dir}")
        
        # Check if instance directory exists and is writable
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)
            print(f"Created instance directory: {instance_dir}")
        
        # Check write permissions
        if not os.access(instance_dir, os.W_OK):
            print(f"Warning: No write permission for {instance_dir}")
        
        # Create all tables
        with app.app_context():
            db.create_all()
            print("Database tables created successfully!")
            
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == '__main__':
    # Initialize database
    if init_database():
        print("Starting Flask app on http://127.0.0.1:5000")
        print(f"Template folder: {template_folder}")
        print(f"Static folder: {static_folder}")
        print(f"Database location: {database_path}")
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        print("Failed to initialize database. Exiting...")