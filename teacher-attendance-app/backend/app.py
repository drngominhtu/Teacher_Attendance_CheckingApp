from flask import Flask, render_template, request, jsonify
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

# Configuration
database_path = os.path.join(instance_dir, 'teacher_attendance.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize database
from database import init_db, db

# Run migration before initializing database
def run_migration():
    """Run database migration if needed"""
    try:
        from migrate_database import migrate_database
        migrate_database()
    except Exception as e:
        print(f"Migration error (might be normal for new db): {e}")

# Run migration first
run_migration()

# Then initialize database
init_db(app)

# Import models after database initialization
with app.app_context():
    from models import (
        Teacher, Subject, Semester, Assignment, Schedule,
        TeachingAssignment, TeachingRecord, SalaryCalculation,
        setup_relationships, DegreeLevel
    )
    # Setup relationships
    setup_relationships()

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

@app.route('/teachers')
def teachers():
    try:
        # Query teachers với error handling cho enum
        teachers_query = Teacher.query.order_by(Teacher.created_at.desc())
        teachers_list = []
        
        for teacher in teachers_query:
            try:
                # Safely convert to dict and handle potential enum errors
                teacher_dict = teacher.to_dict()
                teachers_list.append(teacher)
            except Exception as enum_error:
                print(f"Error processing teacher {teacher.id}: {enum_error}")
                # Ensure degree_level is valid
                if hasattr(teacher, 'degree_level') and teacher.degree_level not in ['dai_hoc', 'thac_si', 'tien_si', 'pho_giao_su', 'giao_su']:
                    teacher.degree_level = 'dai_hoc'
                    teacher.save()
                teachers_list.append(teacher)
        
        return render_template('teachers.html', teachers=teachers_list)
    except Exception as e:
        print(f"Error in teachers route: {e}")
        return render_template('teachers.html', teachers=[])

@app.route('/semesters')
def semesters():
    try:
        semesters_list = Semester.query.order_by(Semester.created_at.desc()).all()
        current_year = datetime.now().year
        return render_template('semesters.html', semesters=semesters_list, current_year=current_year)
    except Exception as e:
        print(f"Error in semesters route: {e}")
        return render_template('semesters.html', semesters=[], current_year=datetime.now().year)

@app.route('/assignments')
def assignments():
    try:
        assignments_list = Assignment.query.order_by(Assignment.created_at.desc()).all()
        
        # Handle potential enum errors in related teachers
        teachers_query = Teacher.query.all()
        teachers_list = []
        for teacher in teachers_query:
            try:
                teacher.to_dict()  # Test if this works
                teachers_list.append(teacher)
            except Exception:
                # Fix invalid enum values
                if hasattr(teacher, 'degree_level') and teacher.degree_level not in ['dai_hoc', 'thac_si', 'tien_si', 'pho_giao_su', 'giao_su']:
                    teacher.degree_level = 'dai_hoc'
                    teacher.save()
                teachers_list.append(teacher)
        
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

@app.route('/schedules')
def schedules():
    return render_template('schedules.html')

@app.route('/teaching-assignments')
def teaching_assignments():
    try:
        teaching_assignments_list = TeachingAssignment.query.order_by(TeachingAssignment.created_at.desc()).all()
        
        # Handle potential enum errors in related teachers
        teachers_query = Teacher.query.filter_by(is_active=True)
        teachers_list = []
        for teacher in teachers_query:
            try:
                teacher.to_dict()  # Test if this works
                teachers_list.append(teacher)
            except Exception:
                # Fix invalid enum values
                if hasattr(teacher, 'degree_level') and teacher.degree_level not in ['dai_hoc', 'thac_si', 'tien_si', 'pho_giao_su', 'giao_su']:
                    teacher.degree_level = 'dai_hoc'
                    teacher.save()
                teachers_list.append(teacher)
        
        subjects_list = Subject.query.filter_by(is_active=True).all()
        semesters_list = Semester.query.filter_by(is_active=True).all()
        return render_template('teaching_assignments.html', 
                             teaching_assignments=teaching_assignments_list,
                             teachers=teachers_list,
                             subjects=subjects_list,
                             semesters=semesters_list)
    except Exception as e:
        print(f"Error in teaching assignments route: {e}")
        return render_template('teaching_assignments.html', 
                             teaching_assignments=[],
                             teachers=[],
                             subjects=[],
                             semesters=[])

@app.route('/salary-calculations')
def salary_calculations():
    try:
        calculations_list = SalaryCalculation.query.order_by(SalaryCalculation.created_at.desc()).all()
        teachers_list = Teacher.query.filter_by(is_active=True).all()
        return render_template('salary_calculations.html',
                             calculations=calculations_list,
                             teachers=teachers_list)
    except Exception as e:
        print(f"Error in salary calculations route: {e}")
        return render_template('salary_calculations.html',
                             calculations=[],
                             teachers=[])

# API Routes for Subjects
@app.route('/api/subjects', methods=['POST'])
def create_subject():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'Không có dữ liệu được gửi'})
        
        # Validate required fields
        required_fields = ['name', 'department']
        for field in required_fields:
            if not data.get(field, '').strip():
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        # Check for existing subject
        existing = Subject.query.filter_by(
            name=data['name'].strip(), 
            department=data['department'].strip()
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'Học phần này đã tồn tại'})
        
        subject = Subject(
            name=data['name'].strip(),
            department=data['department'].strip(),
            student_count=int(data.get('student_count', 0)),
            credits=int(data.get('credits', 3)),
            theory_hours=int(data.get('theory_hours', 0)),
            practice_hours=int(data.get('practice_hours', 0)),
            standard_rate=float(data.get('standard_rate', 0)),
            subject_coefficient=float(data.get('subject_coefficient', 1.0)),
            difficulty_level=data.get('difficulty_level', 'normal'),
            description=data.get('description', '').strip()
        )
        
        if subject.save():
            return jsonify({'success': True, 'message': 'Học phần đã được tạo'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi lưu học phần'})
        
    except Exception as e:
        print(f"Error creating subject: {e}")
        return jsonify({'success': False, 'message': f'Lỗi hệ thống: {str(e)}'})

@app.route('/api/subjects/<int:id>', methods=['PUT'])
def update_subject(id):
    try:
        subject = Subject.get_by_id(id)
        if not subject:
            return jsonify({'success': False, 'message': 'Không tìm thấy học phần'})
        
        data = request.get_json()
        
        subject.name = data.get('name', subject.name)
        subject.department = data.get('department', subject.department)
        subject.student_count = int(data.get('student_count', subject.student_count))
        subject.credits = int(data.get('credits', subject.credits))
        subject.theory_hours = int(data.get('theory_hours', subject.theory_hours))
        subject.practice_hours = int(data.get('practice_hours', subject.practice_hours))
        subject.standard_rate = float(data.get('standard_rate', subject.standard_rate))
        subject.subject_coefficient = float(data.get('subject_coefficient', subject.subject_coefficient))
        subject.difficulty_level = data.get('difficulty_level', subject.difficulty_level)
        subject.description = data.get('description', subject.description)
        
        if subject.save():
            return jsonify({'success': True, 'message': 'Học phần đã được cập nhật'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi cập nhật học phần'})
        
    except Exception as e:
        print(f"Error updating subject: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/subjects/<int:id>', methods=['DELETE'])
def delete_subject(id):
    try:
        subject = Subject.get_by_id(id)
        if not subject:
            return jsonify({'success': False, 'message': 'Không tìm thấy học phần'})
        
        if subject.delete():
            return jsonify({'success': True, 'message': 'Học phần đã được xóa'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi xóa học phần'})
        
    except Exception as e:
        print(f"Error deleting subject: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Teachers
@app.route('/api/teachers', methods=['POST'])
def create_teacher():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'department']
        for field in required_fields:
            if not data.get(field, '').strip():
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        # Check for existing teacher
        existing = Teacher.query.filter_by(
            name=data['name'].strip(),
            department=data['department'].strip()
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'Giảng viên này đã tồn tại'})
        
        # Validate degree level
        valid_degrees = ['dai_hoc', 'thac_si', 'tien_si', 'pho_giao_su', 'giao_su']
        degree_level = data.get('degree_level', 'dai_hoc')
        if degree_level not in valid_degrees:
            degree_level = 'dai_hoc'
        
        teacher = Teacher(
            name=data['name'].strip(),
            department=data['department'].strip(),
            employee_code=data.get('employee_code', '').strip() or None,
            qualifications=data.get('qualifications', '').strip(),
            email=data.get('email', '').strip() or None,
            phone=data.get('phone', '').strip(),
            position=data.get('position', '').strip(),
            academic_rank=data.get('academic_rank', '').strip(),
            degree=data.get('degree', '').strip(),
            degree_level=degree_level,
            base_salary=float(data.get('base_salary', 0)),
            hourly_rate=float(data.get('hourly_rate', 100000))
        )
        
        # Update teacher coefficient based on degree level
        teacher.update_teacher_coefficient()
        
        if teacher.save():
            return jsonify({'success': True, 'message': 'Giảng viên đã được tạo', 'teacher': teacher.to_dict()})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi lưu giảng viên'})
        
    except Exception as e:
        print(f"Error creating teacher: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teachers/<int:id>', methods=['PUT'])
def update_teacher(id):
    try:
        teacher = Teacher.get_by_id(id)
        if not teacher:
            return jsonify({'success': False, 'message': 'Không tìm thấy giảng viên'})
        
        data = request.get_json()
        
        teacher.name = data.get('name', teacher.name)
        teacher.department = data.get('department', teacher.department)
        teacher.employee_code = data.get('employee_code', teacher.employee_code) or None
        teacher.qualifications = data.get('qualifications', teacher.qualifications)
        teacher.email = data.get('email', teacher.email) or None
        teacher.phone = data.get('phone', teacher.phone)
        teacher.position = data.get('position', teacher.position)
        teacher.academic_rank = data.get('academic_rank', teacher.academic_rank)
        teacher.degree = data.get('degree', teacher.degree)
        
        # Update degree level if provided
        if 'degree_level' in data:
            valid_degrees = ['dai_hoc', 'thac_si', 'tien_si', 'pho_giao_su', 'giao_su']
            degree_level = data['degree_level']
            if degree_level in valid_degrees:
                teacher.degree_level = degree_level
                teacher.update_teacher_coefficient()
        
        teacher.base_salary = float(data.get('base_salary', teacher.base_salary))
        teacher.hourly_rate = float(data.get('hourly_rate', teacher.hourly_rate))
        
        if teacher.save():
            return jsonify({'success': True, 'message': 'Giảng viên đã được cập nhật', 'teacher': teacher.to_dict()})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi cập nhật giảng viên'})
        
    except Exception as e:
        print(f"Error updating teacher: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teachers/list', methods=['GET'])
def get_teachers_list():
    try:
        teachers = Teacher.query.order_by(Teacher.created_at.desc()).all()
        teachers_data = []
        for teacher in teachers:
            teachers_data.append(teacher.to_dict())
        
        return jsonify({'success': True, 'teachers': teachers_data})
    except Exception as e:
        print(f"Error getting teachers list: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teachers/<int:id>', methods=['GET'])
def get_teacher(id):
    try:
        teacher = Teacher.get_by_id(id)
        if not teacher:
            return jsonify({'success': False, 'message': 'Không tìm thấy giảng viên'})
        
        return jsonify({'success': True, 'teacher': teacher.to_dict()})
    except Exception as e:
        print(f"Error getting teacher: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Semesters
@app.route('/api/semesters', methods=['POST'])
def create_semester():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'year']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        # Check for existing semester
        existing = Semester.query.filter_by(
            name=data['name'],
            year=int(data['year'])
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'Kì học này đã tồn tại'})
        
        semester = Semester(
            name=data['name'],
            year=int(data['year']),
            academic_year=data.get('academic_year', ''),
            is_current=data.get('is_current', False)
        )
        
        if semester.save():
            return jsonify({'success': True, 'message': 'Kì học đã được tạo'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi lưu kì học'})
        
    except Exception as e:
        print(f"Error creating semester: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/semesters/<int:id>', methods=['PUT'])
def update_semester(id):
    try:
        semester = Semester.get_by_id(id)
        if not semester:
            return jsonify({'success': False, 'message': 'Không tìm thấy kì học'})
        
        data = request.get_json()
        
        semester.name = data.get('name', semester.name)
        semester.year = int(data.get('year', semester.year))
        semester.academic_year = data.get('academic_year', semester.academic_year)
        semester.is_current = data.get('is_current', semester.is_current)
        
        if semester.save():
            return jsonify({'success': True, 'message': 'Kì học đã được cập nhật'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi cập nhật kì học'})
        
    except Exception as e:
        print(f"Error updating semester: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/semesters/<int:id>', methods=['DELETE'])
def delete_semester(id):
    try:
        semester = Semester.get_by_id(id)
        if not semester:
            return jsonify({'success': False, 'message': 'Không tìm thấy kì học'})
        
        if semester.delete():
            return jsonify({'success': True, 'message': 'Kì học đã được xóa'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi xóa kì học'})
        
    except Exception as e:
        print(f"Error deleting semester: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Assignments
@app.route('/api/assignments', methods=['POST'])
def create_assignment():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['teacher_id', 'subject_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        # Check if teacher and subject exist
        teacher = Teacher.get_by_id(data['teacher_id'])
        subject = Subject.get_by_id(data['subject_id'])
        
        if not teacher:
            return jsonify({'success': False, 'message': 'Không tìm thấy giảng viên'})
        if not subject:
            return jsonify({'success': False, 'message': 'Không tìm thấy học phần'})
        
        # Check for existing assignment
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
        
        if assignment.save():
            return jsonify({'success': True, 'message': 'Phân công đã được tạo'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi lưu phân công'})
        
    except Exception as e:
        print(f"Error creating assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/assignments/<int:id>', methods=['DELETE'])
def delete_assignment(id):
    try:
        assignment = Assignment.get_by_id(id)
        if not assignment:
            return jsonify({'success': False, 'message': 'Không tìm thấy phân công'})
        
        if assignment.delete():
            return jsonify({'success': True, 'message': 'Phân công đã được xóa'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi xóa phân công'})
        
    except Exception as e:
        print(f"Error deleting assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Teaching Assignments
@app.route('/api/teaching-assignments', methods=['POST'])
def create_teaching_assignment():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['teacher_id', 'subject_id', 'class_code', 'class_student_count', 'planned_hours', 'start_date', 'end_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        assignment = TeachingAssignment(
            teacher_id=data['teacher_id'],
            subject_id=data['subject_id'],
            semester_id=data.get('semester_id'),
            class_code=data['class_code'],
            class_student_count=int(data['class_student_count']),
            planned_hours=int(data['planned_hours']),
            actual_hours=int(data.get('actual_hours', 0)),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        )
        
        # Tính toán tiền dạy
        assignment.calculate_payment()
        
        if assignment.save():
            return jsonify({'success': True, 'message': 'Phân công giảng dạy đã được tạo'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi lưu phân công'})
            
    except Exception as e:
        print(f"Error creating teaching assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teaching-assignments/<int:id>', methods=['PUT'])
def update_teaching_assignment(id):
    try:
        assignment = TeachingAssignment.get_by_id(id)
        if not assignment:
            return jsonify({'success': False, 'message': 'Không tìm thấy phân công'})
        
        data = request.get_json()
        
        # Update fields
        if 'class_student_count' in data:
            assignment.class_student_count = int(data['class_student_count'])
        if 'actual_hours' in data:
            assignment.actual_hours = int(data['actual_hours'])
        if 'planned_hours' in data:
            assignment.planned_hours = int(data['planned_hours'])
        if 'teacher_coefficient_override' in data:
            assignment.teacher_coefficient_override = float(data['teacher_coefficient_override'])
        if 'subject_coefficient_override' in data:
            assignment.subject_coefficient_override = float(data['subject_coefficient_override'])
        if 'hourly_rate_override' in data:
            assignment.hourly_rate_override = float(data['hourly_rate_override'])
        
        # Recalculate payment
        assignment.calculate_payment()
        
        if assignment.save():
            return jsonify({'success': True, 'message': 'Phân công đã được cập nhật'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi cập nhật phân công'})
            
    except Exception as e:
        print(f"Error updating teaching assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teaching-assignments/<int:id>', methods=['DELETE'])
def delete_teaching_assignment(id):
    try:
        assignment = TeachingAssignment.get_by_id(id)
        if not assignment:
            return jsonify({'success': False, 'message': 'Không tìm thấy phân công'})
        
        if assignment.delete():
            return jsonify({'success': True, 'message': 'Phân công đã được xóa'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi xóa phân công'})
            
    except Exception as e:
        print(f"Error deleting teaching assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teaching-assignments/<int:id>/calculate', methods=['POST'])
def recalculate_teaching_assignment(id):
    try:
        assignment = TeachingAssignment.get_by_id(id)
        if not assignment:
            return jsonify({'success': False, 'message': 'Không tìm thấy phân công'})
        
        # Recalculate payment
        old_amount = assignment.total_amount
        new_amount = assignment.calculate_payment()
        assignment.save()
        
        return jsonify({
            'success': True, 
            'message': 'Đã tính toán lại tiền dạy',
            'old_amount': float(old_amount) if old_amount else 0,
            'new_amount': float(new_amount),
            'calculation_details': {
                'actual_hours': assignment.actual_hours,
                'adjusted_hours': assignment.calculated_adjusted_hours,
                'teacher_coefficient': assignment.effective_teacher_coefficient,
                'subject_coefficient': assignment.effective_subject_coefficient,
                'class_coefficient': assignment.class_coefficient,
                'hourly_rate': assignment.effective_hourly_rate
            }
        })
            
    except Exception as e:
        print(f"Error recalculating teaching assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Salary Calculations
@app.route('/api/salary-calculations', methods=['POST'])
def create_salary_calculation():
    try:
        data = request.get_json()
        
        calculation = SalaryCalculation(
            teacher_id=data['teacher_id'],
            calculation_period=data['calculation_period'],
            calculation_type=data.get('calculation_type', 'monthly'),
            base_salary=data.get('base_salary', 0),
            teaching_hours=data.get('teaching_hours', 0),
            teaching_amount=data.get('teaching_amount', 0),
            position_allowance=data.get('position_allowance', 0),
            research_bonus=data.get('research_bonus', 0),
            overtime_amount=data.get('overtime_amount', 0),
            other_allowances=data.get('other_allowances', 0),
            insurance_deduction=data.get('insurance_deduction', 0),
            tax_deduction=data.get('tax_deduction', 0),
            other_deductions=data.get('other_deductions', 0)
        )
        
        calculation.calculate_totals()
        
        if calculation.save():
            return jsonify({'success': True, 'message': 'Bảng lương đã được tạo'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi lưu bảng lương'})
            
    except Exception as e:
        print(f"Error creating salary calculation: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/salary-calculations/<int:id>', methods=['DELETE'])
def delete_salary_calculation(id):
    try:
        calculation = SalaryCalculation.get_by_id(id)
        if not calculation:
            return jsonify({'success': False, 'message': 'Không tìm thấy bảng lương'})
        
        if calculation.delete():
            return jsonify({'success': True, 'message': 'Bảng lương đã được xóa'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi xóa bảng lương'})
            
    except Exception as e:
        print(f"Error deleting salary calculation: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teaching-assignments/list', methods=['GET'])
def get_teaching_assignments_list():
    try:
        assignments = TeachingAssignment.query.order_by(TeachingAssignment.created_at.desc()).all()
        assignments_data = []
        for assignment in assignments:
            assignments_data.append(assignment.to_dict())
        
        return jsonify({'success': True, 'teaching_assignments': assignments_data})
    except Exception as e:
        print(f"Error getting teaching assignments list: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/assignments/list', methods=['GET'])
def get_assignments_list():
    try:
        assignments = Assignment.query.order_by(Assignment.created_at.desc()).all()
        assignments_data = []
        for assignment in assignments:
            assignment_dict = assignment.to_dict()
            # Add related data
            if assignment.teacher:
                assignment_dict['teacher_name'] = assignment.teacher.name
                assignment_dict['teacher_department'] = assignment.teacher.department
            if assignment.subject:
                assignment_dict['subject_name'] = assignment.subject.name
                assignment_dict['subject_department'] = assignment.subject.department
            if assignment.semester:
                assignment_dict['semester_name'] = assignment.semester.name
                assignment_dict['semester_year'] = assignment.semester.year
            assignments_data.append(assignment_dict)
        
        return jsonify({'success': True, 'assignments': assignments_data})
    except Exception as e:
        print(f"Error getting assignments list: {e}")
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    print("Starting Flask app on http://127.0.0.1:5000")
    print(f"Template folder: {template_folder}")
    print(f"Static folder: {static_folder}")
    print(f"Database location: {database_path}")
    app.run(debug=True, host='127.0.0.1', port=5000)