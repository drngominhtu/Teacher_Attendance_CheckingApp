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

# Simplified migration function
def run_migration():
    """Chạy migration đơn giản và an toàn"""
    try:
        from migrate_database_v3 import migrate_database
        migrate_database()
        return True
    except Exception as e:
        print(f"Migration warning: {e}")
        return False

# Initialize database
init_db(app)
run_migration()

# Import models with better error handling
with app.app_context():
    try:
        # Only import essential models for now
        from models.degree import Degree
        from models.Department import Department
        from models.teacher import Teacher
        from models.subject import Subject
        from models.semester import Semester
        
        # Try to import TeachingAssignment
        try:
            from models.teaching_assignment import TeachingAssignment
            globals()['TeachingAssignment'] = TeachingAssignment
            print("✓ TeachingAssignment model imported")
        except ImportError:
            print("! TeachingAssignment model not found - will create empty list")
        
        # Try to import ClassSection
        try:
            from models.class_section import ClassSection
            globals()['ClassSection'] = ClassSection
            print("✓ ClassSection model imported")
        except ImportError:
            print("! ClassSection model not found - will create empty list")
        
        # Try to import SalaryCalculation model
        try:
            from models.salary_calculation import SalaryCalculation
            globals()['SalaryCalculation'] = SalaryCalculation
            print("✓ SalaryCalculation model imported")
        except ImportError:
            print("! SalaryCalculation model not found")
        
        # Try to import SalarySetting model
        try:
            from models.salary_setting import SalarySetting
            globals()['SalarySetting'] = SalarySetting
            print("✓ SalarySetting model imported")
        except ImportError:
            print("! SalarySetting model not found")
        
        # Make them globally available
        globals()['Degree'] = Degree
        globals()['Department'] = Department
        globals()['Teacher'] = Teacher
        globals()['Subject'] = Subject
        globals()['Semester'] = Semester
        
        print("✓ Core models imported successfully")
        
        # Test basic queries
        try:
            degree_count = Degree.query.count()
            dept_count = Department.query.count()
            print(f"Database working: {degree_count} degrees, {dept_count} departments")
        except Exception as query_error:
            print(f"Database query error: {query_error}")
        
    except Exception as e:
        print(f"Model import error: {e}")

# Routes - keep simple for now
@app.route('/')
def index():
    try:
        # Simple counts without complex relationships
        subjects_count = 0
        teachers_count = 0
        departments_count = 0
        semesters_count = 0
        class_sections_count = 0
        
        try:
            if 'Subject' in globals():
                subjects_count = Subject.query.count()
            if 'Teacher' in globals():
                teachers_count = Teacher.query.count()
            if 'Department' in globals():
                departments_count = Department.query.count()
            if 'Semester' in globals():
                semesters_count = Semester.query.count()
        except:
            pass
        
        return render_template('index.html', 
                             subjects_count=subjects_count,
                             teachers_count=teachers_count,
                             departments_count=departments_count,
                             semesters_count=semesters_count,
                             class_sections_count=class_sections_count,
                             master_degree_rate=75,
                             assigned_classes_rate=80,
                             avg_enrollment_rate=85)
    except Exception as e:
        print(f"Index route error: {e}")
        return f"Error: {e}", 500

@app.route('/subjects')
def subjects():
    try:
        subjects_list = []
        departments_list = []
        
        # Get subjects
        if 'Subject' in globals():
            subjects_list = Subject.query.filter_by(is_active=True).order_by(Subject.created_at.desc()).all()
        
        # Get departments - FORCE load from database
        if 'Department' in globals():
            departments_list = Department.query.filter_by(is_active=True).order_by(Department.name).all()
            print(f"Found {len(departments_list)} departments for subjects")
        
        # Create departments from subjects if needed
        if not departments_list and 'Subject' in globals():
            existing_depts = db.session.query(Subject.department).filter(
                Subject.department.isnot(None),
                Subject.department != '',
                Subject.is_active == True
            ).distinct().all()
            
            for dept_tuple in existing_depts:
                dept_name = dept_tuple[0]
                if dept_name and 'Department' in globals():
                    existing = Department.query.filter_by(name=dept_name).first()
                    if not existing:
                        new_dept = Department(
                            code=dept_name.replace(' ', '')[:4].upper(),
                            name=dept_name,
                            abbreviation=dept_name.replace(' ', '')[:4].upper(),
                            description=f'Khoa {dept_name}'
                        )
                        if new_dept.save():
                            departments_list.append(new_dept)
            
            # Refresh from database
            if 'Department' in globals():
                departments_list = Department.query.filter_by(is_active=True).order_by(Department.name).all()
        
        return render_template('subjects.html', 
                             subjects=subjects_list, 
                             departments=departments_list)
    except Exception as e:
        print(f"Error in subjects route: {e}")
        import traceback
        traceback.print_exc()
        return render_template('subjects.html', subjects=[], departments=[])

@app.route('/teachers')
def teachers():
    try:
        print("=== Loading Teachers Page ===")
        
        # Debug: Check if models are available
        print(f"Degree in globals: {'Degree' in globals()}")
        print(f"Department in globals: {'Department' in globals()}")
        print(f"Teacher in globals: {'Teacher' in globals()}")
        
        teachers_list = []
        departments_list = []
        degrees_list = []
        
        # Get teachers with explicit model check
        try:
            from models.teacher import Teacher as TeacherModel
            teachers_list = TeacherModel.query.filter_by(is_active=True).order_by(TeacherModel.created_at.desc()).all()
            print(f"✓ Found {len(teachers_list)} teachers")
        except Exception as e:
            print(f"✗ Error loading teachers: {e}")
        
        # Get departments with explicit model check
        try:
            from models.Department import Department as DepartmentModel
            departments_list = DepartmentModel.query.filter_by(is_active=True).order_by(DepartmentModel.name).all()
            print(f"✓ Found {len(departments_list)} departments:")
            for dept in departments_list:
                print(f"   - ID: {dept.id}, Name: {dept.name}, Code: {dept.code}")
        except Exception as e:
            print(f"✗ Error loading departments: {e}")
            import traceback
            traceback.print_exc()
        
        # Get degrees with explicit model check
        try:
            from models.degree import Degree as DegreeModel
            degrees_list = DegreeModel.query.filter_by(is_active=True).order_by(DegreeModel.coefficient).all()
            print(f"✓ Found {len(degrees_list)} degrees:")
            for degree in degrees_list:
                print(f"   - ID: {degree.id}, Name: {degree.name}, Coeff: {degree.coefficient}")
        except Exception as e:
            print(f"✗ Error loading degrees: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"=== Rendering with {len(teachers_list)} teachers, {len(departments_list)} departments, {len(degrees_list)} degrees ===")
        
        return render_template('teachers.html', 
                             teachers=teachers_list,
                             departments=departments_list,
                             degrees=degrees_list)
    except Exception as e:
        print(f"✗ Error in teachers route: {e}")
        import traceback
        traceback.print_exc()
        return render_template('teachers.html', teachers=[], departments=[], degrees=[])

@app.route('/semesters')
def semesters():
    try:
        semesters_list = []
        current_year = datetime.now().year
        
        # Get semesters with safe error handling
        if 'Semester' in globals():
            semesters_list = Semester.query.filter_by(is_active=True).order_by(Semester.year.desc(), Semester.name).all()
        
        return render_template('semesters.html', 
                             semesters=semesters_list, 
                             current_year=current_year)
    except Exception as e:
        print(f"Error in semesters route: {e}")
        return render_template('semesters.html', 
                             semesters=[], 
                             current_year=datetime.now().year)

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
        teaching_assignments_list = []
        
        # Safely get teaching assignments
        if 'TeachingAssignment' in globals():
            teaching_assignments_list = TeachingAssignment.query.order_by(TeachingAssignment.created_at.desc()).all()
        else:
            print("TeachingAssignment model not available")
        
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
        import traceback
        traceback.print_exc()
        return render_template('teaching_assignments.html', 
                             teaching_assignments=[],
                             teachers=[],
                             subjects=[],
                             semesters=[])

# Salary Management Routes - Separate pages
@app.route('/salary-settings')
def salary_settings():
    try:
        settings = get_default_salary_settings()
        return render_template('salary_settings.html', settings=settings)
    except Exception as e:
        print(f"Error in salary settings route: {e}")
        return render_template('salary_settings.html', settings={})

@app.route('/salary-calculations')
def salary_calculations():
    try:
        teachers_list = []
        semesters_list = []
        
        if 'Teacher' in globals():
            teachers_list = Teacher.query.filter_by(is_active=True).all()
        if 'Semester' in globals():
            semesters_list = Semester.query.filter_by(is_active=True).all()
        
        return render_template('salary_calculations.html',
                             teachers=teachers_list,
                             semesters=semesters_list)
    except Exception as e:
        print(f"Error in salary calculations route: {e}")
        return render_template('salary_calculations.html', teachers=[], semesters=[])

@app.route('/salary-history')
def salary_history():
    try:
        calculations_list = []
        
        try:
            from models.salary_calculation import SalaryCalculation
            # Test if table exists and has required columns
            calculations_raw = SalaryCalculation.query.order_by(SalaryCalculation.created_at.desc()).all()
            calculations_list = [calc.to_dict() for calc in calculations_raw]
        except Exception as db_error:
            print(f"Database error in salary_history: {db_error}")
            # Create empty list if table doesn't exist or has missing columns
            calculations_list = []
        
        return render_template('salary_history.html', calculations=calculations_list)
    except Exception as e:
        print(f"Error in salary history route: {e}")
        return render_template('salary_history.html', calculations=[])

@app.route('/degrees')
def degrees():
    try:
        if 'Degree' in globals():
            degrees_list = Degree.query.filter_by(is_active=True).order_by(Degree.coefficient).all()
        else:
            degrees_list = []
        return render_template('degrees.html', degrees=degrees_list)
    except Exception as e:
        print(f"Error in degrees route: {e}")
        return render_template('degrees.html', degrees=[])

@app.route('/departments')
def departments():
    try:
        if 'Department' in globals():
            departments_list = Department.query.filter_by(is_active=True).order_by(Department.name).all()
        else:
            departments_list = []
        return render_template('departments.html', departments=departments_list)
    except Exception as e:
        print(f"Error in departments route: {e}")
        return render_template('departments.html', departments=[])

@app.route('/class-sections')
def class_sections():
    try:
        class_sections_list = []
        subjects_list = []
        semesters_list = []
        teachers_list = []
        
        try:
            from models.class_section import ClassSection
            class_sections_raw = ClassSection.query.filter_by(is_active=True).order_by(ClassSection.created_at.desc()).all()
            class_sections_list = [cs.to_dict() for cs in class_sections_raw]
        except Exception as e:
            print(f"Error loading class sections: {e}")
        
        if 'Subject' in globals():
            subjects_list = Subject.query.filter_by(is_active=True).all()
        if 'Semester' in globals():
            semesters_list = Semester.query.filter_by(is_active=True).all()
        if 'Teacher' in globals():
            teachers_list = Teacher.query.filter_by(is_active=True).all()
        
        return render_template('class_sections.html', 
                             class_sections=class_sections_list,
                             subjects=subjects_list,
                             semesters=semesters_list,
                             teachers=teachers_list)
    except Exception as e:
        print(f"Error in class sections route: {e}")
        return render_template('class_sections.html', 
                             class_sections=[],
                             subjects=[],
                             semesters=[],
                             teachers=[])

@app.route('/teacher-statistics')
def teacher_statistics():
    try:
        stats = calculate_teacher_statistics()
        return render_template('teacher_statistics.html', stats=stats)
    except Exception as e:
        print(f"Error in teacher statistics route: {e}")
        return render_template('teacher_statistics.html', stats={})

@app.route('/class-statistics')
def class_statistics():
    try:
        stats = calculate_class_statistics()
        return render_template('class_statistics.html', stats=stats)
    except Exception as e:
        print(f"Error in class statistics route: {e}")
        return render_template('class_statistics.html', stats={})

@app.route('/subject-statistics')
def subject_statistics():
    try:
        stats = calculate_subject_statistics()
        return render_template('subject_statistics.html', stats=stats)
    except Exception as e:
        print(f"Error in subject statistics route: {e}")
        return render_template('subject_statistics.html', stats={})

def calculate_teacher_statistics():
    """Calculate teacher statistics"""
    try:
        stats = {
            'total_teachers': 0,
            'active_teachers': 0,
            'phd_teachers': 0,
            'avg_age': 0,
            'department_stats': [],
            'department_chart_data': {'labels': [], 'data': []},
            'degree_chart_data': {'labels': [], 'data': []}
        }
        
        if 'Teacher' not in globals():
            return stats
            
        # Basic counts
        stats['total_teachers'] = Teacher.query.count()
        stats['active_teachers'] = Teacher.query.filter_by(is_active=True).count()
        
        # Calculate average age
        from sqlalchemy import func
        current_date = datetime.now().date()
        teachers_with_birth_date = Teacher.query.filter(
            Teacher.birth_date.isnot(None),
            Teacher.is_active == True
        ).all()
        
        if teachers_with_birth_date:
            total_age = 0
            count = 0
            for teacher in teachers_with_birth_date:
                age = (current_date - teacher.birth_date).days / 365.25
                total_age += age
                count += 1
            stats['avg_age'] = total_age / count if count > 0 else 0
        
        # PhD count based on degree names
        try:
            if 'Degree' in globals():
                phd_degrees = Degree.query.filter(
                    Degree.name.like('%Tiến sĩ%') | 
                    Degree.name.like('%PhD%') |
                    Degree.name.like('%TS%')
                ).all()
                
                phd_degree_ids = [degree.id for degree in phd_degrees]
                if phd_degree_ids:
                    stats['phd_teachers'] = Teacher.query.filter(
                        Teacher.degree_id.in_(phd_degree_ids),
                        Teacher.is_active == True
                    ).count()
        except Exception as e:
            print(f"Error counting PhD teachers: {e}")
        
        # Department statistics
        if 'Department' in globals():
            departments = Department.query.filter_by(is_active=True).all()
            dept_stats = []
            dept_labels = []
            dept_data = []
            
            for dept in departments:
                dept_teachers = Teacher.query.filter_by(
                    department_id=dept.id, 
                    is_active=True
                ).all()
                
                if len(dept_teachers) == 0:
                    continue
                
                # Count degrees in this department
                phd_count = 0
                master_count = 0
                bachelor_count = 0
                dept_total_age = 0
                dept_age_count = 0
                
                for teacher in dept_teachers:
                    # Count by degree
                    if teacher.degree_id:
                        try:
                            degree = Degree.query.get(teacher.degree_id)
                            if degree:
                                degree_name = degree.name.lower()
                                if 'tiến sĩ' in degree_name or 'phd' in degree_name or 'ts' in degree_name:
                                    phd_count += 1
                                elif 'thạc sĩ' in degree_name or 'master' in degree_name or 'ths' in degree_name:
                                    master_count += 1
                                else:
                                    bachelor_count += 1
                        except:
                            bachelor_count += 1
                    else:
                        bachelor_count += 1
                    
                    # Calculate age
                    if teacher.birth_date:
                        age = (current_date - teacher.birth_date).days / 365.25
                        dept_total_age += age
                        dept_age_count += 1
                
                dept_avg_age = dept_total_age / dept_age_count if dept_age_count > 0 else 0
                
                dept_stat = {
                    'department_name': dept.name,
                    'total_teachers': len(dept_teachers),
                    'active_teachers': len(dept_teachers),
                    'phd_teachers': phd_count,
                    'master_teachers': master_count,
                    'bachelor_teachers': bachelor_count,
                    'avg_age': dept_avg_age
                }
                
                dept_stats.append(dept_stat)
                dept_labels.append(dept.name)
                dept_data.append(len(dept_teachers))
            
            stats['department_stats'] = dept_stats
            stats['department_chart_data'] = {
                'labels': dept_labels,
                'data': dept_data
            }
        
        # Degree statistics for chart
        if 'Degree' in globals():
            degrees = Degree.query.filter_by(is_active=True).all()
            degree_labels = []
            degree_data = []
            
            for degree in degrees:
                count = Teacher.query.filter_by(
                    degree_id=degree.id,
                    is_active=True
                ).count()
                
                if count > 0:
                    degree_labels.append(degree.name)
                    degree_data.append(count)
            
            stats['degree_chart_data'] = {
                'labels': degree_labels,
                'data': degree_data
            }
        
        return stats
        
    except Exception as e:
        print(f"Error calculating teacher statistics: {e}")
        import traceback
        traceback.print_exc()
        return {
            'total_teachers': 0,
            'active_teachers': 0,
            'phd_teachers': 0,
            'avg_age': 0,
            'department_stats': [],
            'department_chart_data': {'labels': [], 'data': []},
            'degree_chart_data': {'labels': [], 'data': []}
        }

def calculate_class_statistics():
    """Calculate class statistics"""
    try:
        stats = {
            'total_classes': 0,
            'active_classes': 0,
            'total_students': 0,
            'avg_class_size': 0,
            'top_classes': []
        }
        
        if 'ClassSection' not in globals():
            return stats
            
        # Basic counts
        stats['total_classes'] = ClassSection.query.count()
        stats['active_classes'] = ClassSection.query.filter_by(status='active').count()
        
        # Student counts
        from sqlalchemy import func
        total_students = db.session.query(func.sum(ClassSection.student_count)).scalar()
        stats['total_students'] = total_students or 0
        
        if stats['total_classes'] > 0:
            stats['avg_class_size'] = stats['total_students'] / stats['total_classes']
        
        return stats
        
    except Exception as e:
        print(f"Error calculating class statistics: {e}")
        return {}

def calculate_subject_statistics():
    """Calculate subject statistics"""
    try:
        stats = {
            'total_subjects': 0,
            'active_subjects': 0,
            'total_credits': 0,
            'avg_credits': 0,
            'hard_subjects': 0,
            'normal_subjects': 0,
            'very_hard_subjects': 0,
            'subjects_with_classes': 0,
            'department_stats': [],
            'department_chart_data': {'labels': [], 'data': []},
            'credits_chart_data': {'labels': [], 'data': []}
        }
        
        if 'Subject' not in globals():
            return stats
            
        # Basic counts
        stats['total_subjects'] = Subject.query.count()
        stats['active_subjects'] = Subject.query.filter_by(is_active=True).count()
        
        # Credits statistics
        from sqlalchemy import func
        total_credits = db.session.query(func.sum(Subject.credits)).filter_by(is_active=True).scalar()
        stats['total_credits'] = total_credits or 0
        
        if stats['active_subjects'] > 0:
            stats['avg_credits'] = stats['total_credits'] / stats['active_subjects']
        
        # Difficulty level counts
        stats['normal_subjects'] = Subject.query.filter_by(
            difficulty_level='normal', is_active=True
        ).count()
        stats['hard_subjects'] = Subject.query.filter_by(
            difficulty_level='hard', is_active=True
        ).count()
        stats['very_hard_subjects'] = Subject.query.filter_by(
            difficulty_level='very_hard', is_active=True
        ).count()
        
        # Subjects with classes count
        if 'ClassSection' in globals():
            subjects_with_classes = db.session.query(ClassSection.subject_id).filter_by(
                is_active=True
            ).distinct().count()
            stats['subjects_with_classes'] = subjects_with_classes
        
        # Department statistics
        if 'Department' in globals():
            departments = Department.query.filter_by(is_active=True).all()
            dept_stats = []
            dept_labels = []
            dept_data = []
            
            for dept in departments:
                dept_subjects = Subject.query.filter_by(
                    department_id=dept.id, 
                    is_active=True
                ).all()
                
                if len(dept_subjects) == 0:
                    continue
                
                # Calculate department statistics
                dept_total_credits = sum(s.credits for s in dept_subjects)
                dept_avg_credits = dept_total_credits / len(dept_subjects) if len(dept_subjects) > 0 else 0
                
                # Count by difficulty
                dept_hard_subjects = len([s for s in dept_subjects if s.difficulty_level in ['hard', 'very_hard']])
                
                # Count classes for this department
                dept_total_classes = 0
                if 'ClassSection' in globals():
                    dept_total_classes = db.session.query(ClassSection).join(Subject).filter(
                        Subject.department_id == dept.id,
                        ClassSection.is_active == True
                    ).count()
                
                dept_stat = {
                    'department_name': dept.name,
                    'total_subjects': len(dept_subjects),
                    'active_subjects': len(dept_subjects),
                    'total_credits': dept_total_credits,
                    'avg_credits': dept_avg_credits,
                    'hard_subjects': dept_hard_subjects,
                    'total_classes': dept_total_classes
                }
                
                dept_stats.append(dept_stat)
                dept_labels.append(dept.name)
                dept_data.append(len(dept_subjects))
            
            stats['department_stats'] = dept_stats
            stats['department_chart_data'] = {
                'labels': dept_labels,
                'data': dept_data
            }
        
        # Credits distribution for chart
        credits_distribution = {}
        active_subjects = Subject.query.filter_by(is_active=True).all()
        for subject in active_subjects:
            credits = subject.credits
            if credits in credits_distribution:
                credits_distribution[credits] += 1
            else:
                credits_distribution[credits] = 1
        
        if credits_distribution:
            stats['credits_chart_data'] = {
                'labels': [f'{k} TC' for k in sorted(credits_distribution.keys())],
                'data': [credits_distribution[k] for k in sorted(credits_distribution.keys())]
            }
        
        return stats
        
    except Exception as e:
        print(f"Error calculating subject statistics: {e}")
        import traceback
        traceback.print_exc()
        return {
            'total_subjects': 0,
            'active_subjects': 0,
            'total_credits': 0,
            'avg_credits': 0,
            'hard_subjects': 0,
            'normal_subjects': 0,
            'very_hard_subjects': 0,
            'subjects_with_classes': 0,
            'department_stats': [],
            'department_chart_data': {'labels': [], 'data': []},
            'credits_chart_data': {'labels': [], 'data': []}
        }

# API Routes
@app.route('/api/subjects', methods=['POST'])
def create_subject():
    try:
        if 'Subject' not in globals():
            return jsonify({'success': False, 'message': 'Subject model not available'})
            
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Không có dữ liệu'})
        
        # Validate required fields - remove semester_id requirement
        required_fields = ['name', 'department_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        # Check for existing subject
        existing = Subject.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'success': False, 'message': 'Học phần này đã tồn tại'})
        
        subject = Subject(
            name=data['name'],
            code=data.get('code'),
            department_id=data['department_id'],
            credits=data.get('credits', 3),
            theory_hours=data.get('theory_hours', 0),
            practice_hours=data.get('practice_hours', 0),
            subject_coefficient=data.get('subject_coefficient', 1.0),
            difficulty_level=data.get('difficulty_level', 'normal'),
            description=data.get('description', '')
        )
        
        if subject.save():
            return jsonify({'success': True, 'message': 'Học phần đã được tạo'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi lưu học phần'})
        
    except Exception as e:
        print(f"Error creating subject: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/subjects/<int:id>', methods=['PUT'])
def update_subject(id):
    try:
        subject = Subject.get_by_id(id)
        if not subject:
            return jsonify({'success': False, 'message': 'Không tìm thấy học phần'})
        
        data = request.get_json()
        
        subject.name = data.get('name', subject.name)
        subject.code = data.get('code', subject.code)
        subject.department_id = data.get('department_id', subject.department_id)
        subject.credits = data.get('credits', subject.credits)
        subject.theory_hours = data.get('theory_hours', subject.theory_hours)
        subject.practice_hours = data.get('practice_hours', subject.practice_hours)
        subject.subject_coefficient = data.get('subject_coefficient', subject.subject_coefficient)
        subject.difficulty_level = data.get('difficulty_level', subject.difficulty_level)
        subject.description = data.get('description', subject.description)
        # Removed semester_id reference
        
        if subject.save():
            return jsonify({'success': True, 'message': 'Học phần đã được cập nhật'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi cập nhật học phần'})
        
    except Exception as e:
        print(f"Error updating subject: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/subjects/<int:id>', methods=['GET'])
def api_get_subject(id):
    try:
        if 'Subject' not in globals():
            return jsonify({'success': False, 'message': 'Subject model not available'})
            
        subject = Subject.query.get(id)
        if not subject:
            return jsonify({'success': False, 'message': 'Không tìm thấy học phần'})
        
        return jsonify({'success': True, 'subject': subject.to_dict()})
    except Exception as e:
        print(f"Error getting subject: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/subjects/<int:id>', methods=['DELETE'])
def api_delete_subject(id):
    try:
        if 'Subject' not in globals():
            return jsonify({'success': False, 'message': 'Subject model not available'})
            
        subject = Subject.query.get(id)
        if not subject:
            return jsonify({'success': False, 'message': 'Không tìm thấy học phần'})
        
        # Check if any teaching assignments are using this subject
        try:
            if 'TeachingAssignment' in globals():
                assignment_count = TeachingAssignment.query.filter_by(subject_id=id).count()
                if assignment_count > 0:
                    return jsonify({'success': False, 'message': f'Không thể xóa học phần đang có {assignment_count} phân công giảng dạy'})
        except:
            pass
        
        db.session.delete(subject)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Học phần đã được xóa thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting subject: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Teachers  
@app.route('/api/teachers', methods=['POST'])
def create_teacher():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'Không có dữ liệu được gửi'})
        
        print(f"Received data: {data}")
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'success': False, 'message': 'Tên không được để trống'})
        
        # Check for existing teacher
        if data.get('employee_code'):
            from models.teacher import Teacher
            existing = Teacher.query.filter_by(employee_code=data['employee_code']).first()
            if existing:
                return jsonify({'success': False, 'message': 'Mã số giảng viên này đã tồn tại'})
        
        if data.get('email'):
            from models.teacher import Teacher
            existing = Teacher.query.filter_by(email=data['email']).first()
            if existing:
                return jsonify({'success': False, 'message': 'Email này đã tồn tại'})

        # Create teacher
        from models.teacher import Teacher
        teacher = Teacher()
        teacher.name = data['name']
        teacher.employee_code = data.get('employee_code')
        teacher.phone = data.get('phone')
        teacher.email = data.get('email')
        teacher.department_id = int(data['department_id']) if data.get('department_id') else 1
        teacher.degree_id = int(data['degree_id']) if data.get('degree_id') else 1
        teacher.position = data.get('position')
        teacher.qualifications = data.get('qualifications')
        teacher.base_salary = float(data.get('base_salary', 0))
        teacher.hourly_rate = float(data.get('hourly_rate', 100000))
        
        # Handle birth_date safely - use different variable name
        if data.get('birth_date'):
            try:
                from datetime import datetime as dt_parser
                teacher.birth_date = dt_parser.strptime(data['birth_date'], '%Y-%m-%d').date()
            except Exception as date_error:
                print(f"Date parsing error: {date_error}")
                pass
        
        # Set defaults
        teacher.is_active = True
        teacher.hire_date = datetime.now()
        
        # Save to database
        db.session.add(teacher)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Giảng viên đã được tạo thành công!',
            'teacher': teacher.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating teacher: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Lỗi hệ thống: {str(e)}'})

@app.route('/api/teachers/list', methods=['GET'])
def get_teachers_list():
    try:
        from models.teacher import Teacher
        
        # Get filter parameters
        department_id = request.args.get('department_id')
        
        query = Teacher.query.filter_by(is_active=True)
        if department_id:
            query = query.filter_by(department_id=department_id)
        
        teachers = query.order_by(Teacher.created_at.desc()).all()
        teachers_data = [teacher.to_dict() for teacher in teachers]
        
        return jsonify({'success': True, 'teachers': teachers_data})
    except Exception as e:
        print(f"Error getting teachers list: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teachers/<int:id>', methods=['GET'])
def api_get_teacher(id):
    try:
        from models.teacher import Teacher
        teacher = Teacher.query.get(id)
        if not teacher:
            return jsonify({'success': False, 'message': 'Không tìm thấy giảng viên'})
        
        return jsonify({'success': True, 'teacher': teacher.to_dict()})
    except Exception as e:
        print(f"Error getting teacher: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teachers/<int:id>', methods=['PUT'])
def api_update_teacher(id):
    try:
        from models.teacher import Teacher
        teacher = Teacher.query.get(id)
        if not teacher:
            return jsonify({'success': False, 'message': 'Không tìm thấy giảng viên'})
        
        data = request.get_json()
        
        # Check for existing teacher with same employee_code/email (exclude current)
        if data.get('employee_code') and data['employee_code'] != teacher.employee_code:
            existing_code = Teacher.query.filter_by(employee_code=data['employee_code']).first()
            if existing_code:
                return jsonify({'success': False, 'message': 'Mã số giảng viên này đã tồn tại'})
        
        if data.get('email') and data['email'] != teacher.email:
            existing_email = Teacher.query.filter_by(email=data['email']).first()
            if existing_email:
                return jsonify({'success': False, 'message': 'Email này đã tồn tại'})
        
        # Update fields
        teacher.employee_code = data.get('employee_code', teacher.employee_code)
        teacher.name = data.get('name', teacher.name)
        teacher.phone = data.get('phone', teacher.phone)
        teacher.email = data.get('email', teacher.email)
        teacher.department_id = int(data.get('department_id', teacher.department_id))
        teacher.degree_id = int(data.get('degree_id', teacher.degree_id))
        teacher.position = data.get('position', teacher.position)
        teacher.qualifications = data.get('qualifications', teacher.qualifications)
        
        # Handle birth_date
        if data.get('birth_date'):
            try:
                from datetime import datetime as dt_parser
                teacher.birth_date = dt_parser.strptime(data['birth_date'], '%Y-%m-%d').date()
            except:
                pass
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Giảng viên đã được cập nhật thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating teacher: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teachers/<int:id>', methods=['DELETE'])
def api_delete_teacher(id):
    try:
        from models.teacher import Teacher
        teacher = Teacher.query.get(id)
        if not teacher:
            return jsonify({'success': False, 'message': 'Không tìm thấy giảng viên'})
        
        # Check if any teaching assignments are using this teacher
        try:
            if 'TeachingAssignment' in globals():
                assignment_count = TeachingAssignment.query.filter_by(teacher_id=id).count()
                if assignment_count > 0:
                    return jsonify({'success': False, 'message': f'Không thể xóa giảng viên đang có {assignment_count} phân công giảng dạy'})
        except:
            pass
        
        db.session.delete(teacher)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Giảng viên đã được xóa thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting teacher: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Degrees
@app.route('/api/degrees', methods=['POST'])
def api_create_degree():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'Không có dữ liệu được gửi'})
        
        # Validate required fields
        required_fields = ['name', 'abbreviation', 'coefficient']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        from models.degree import Degree
        
        # Check for existing degree
        existing = Degree.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'success': False, 'message': 'Bằng cấp này đã tồn tại'})
        
        degree = Degree(
            name=data['name'],
            abbreviation=data['abbreviation'],
            coefficient=float(data['coefficient']),
            description=data.get('description', '')
        )
        
        db.session.add(degree)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Bằng cấp đã được tạo thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating degree: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/degrees/<int:id>', methods=['GET'])
def api_get_degree(id):
    try:
        from models.degree import Degree
        degree = Degree.query.get(id)
        if not degree:
            return jsonify({'success': False, 'message': 'Không tìm thấy bằng cấp'})
        
        return jsonify({'success': True, 'degree': degree.to_dict()})
    except Exception as e:
        print(f"Error getting degree: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/degrees/<int:id>', methods=['PUT'])
def api_update_degree(id):
    try:
        from models.degree import Degree
        degree = Degree.query.get(id)
        if not degree:
            return jsonify({'success': False, 'message': 'Không tìm thấy bằng cấp'})
        
        data = request.get_json()
        
        # Check for existing degree with same name/abbreviation (exclude current)
        if data.get('name') and data['name'] != degree.name:
            existing_name = Degree.query.filter_by(name=data['name']).first()
            if existing_name:
                return jsonify({'success': False, 'message': 'Tên bằng cấp này đã tồn tại'})
        
        if data.get('abbreviation') and data['abbreviation'] != degree.abbreviation:
            existing_abbr = Degree.query.filter_by(abbreviation=data['abbreviation']).first()
            if existing_abbr:
                return jsonify({'success': False, 'message': 'Viết tắt này đã tồn tại'})
        
        # Update fields
        degree.name = data.get('name', degree.name)
        degree.abbreviation = data.get('abbreviation', degree.abbreviation)
        degree.coefficient = float(data.get('coefficient', degree.coefficient))
        degree.description = data.get('description', degree.description)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Bằng cấp đã được cập nhật thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating degree: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/degrees/<int:id>', methods=['DELETE'])
def api_delete_degree(id):
    try:
        from models.degree import Degree
        degree = Degree.query.get(id)
        if not degree:
            return jsonify({'success': False, 'message': 'Không tìm thấy bằng cấp'})
        
        # Check if degree is being used by any teachers
        from models.teacher import Teacher
        teachers_using = Teacher.query.filter_by(degree_id=id, is_active=True).count()
        if teachers_using > 0:
            return jsonify({
                'success': False, 
                'message': f'Không thể xóa bằng cấp này vì đang có {teachers_using} giảng viên sử dụng'
            })
        
        db.session.delete(degree)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Bằng cấp đã được xóa thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting degree: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/degrees/list', methods=['GET'])
def api_degrees_list():
    try:
        from models.degree import Degree
        degrees = Degree.query.filter_by(is_active=True).all()
        degrees_list = [degree.to_dict() for degree in degrees]
        
        return jsonify({'success': True, 'degrees': degrees_list})
        
    except Exception as e:
        print(f"Error getting degrees list: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Departments
@app.route('/api/departments', methods=['POST'])
def api_create_department():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'Không có dữ liệu được gửi'})
        
        # Validate required fields
        required_fields = ['code', 'name', 'abbreviation']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        from models.Department import Department
        
        # Check for existing department
        existing_code = Department.query.filter_by(code=data['code']).first()
        existing_name = Department.query.filter_by(name=data['name']).first()
        
        if existing_code:
            return jsonify({'success': False, 'message': 'Mã khoa này đã tồn tại'})
        if existing_name:
            return jsonify({'success': False, 'message': 'Tên khoa này đã tồn tại'})
        
        department = Department(
            code=data['code'],
            name=data['name'],
            abbreviation=data['abbreviation'],
            description=data.get('description', '')
        )
        
        db.session.add(department)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Khoa đã được tạo thành công!',
            'department': department.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating department: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/departments/list', methods=['GET'])
def api_get_departments_list():
    try:
        from models.Department import Department
        departments = Department.query.filter_by(is_active=True).order_by(Department.name).all()
        departments_data = [dept.to_dict() for dept in departments]
        return jsonify({'success': True, 'departments': departments_data})
    except Exception as e:
        print(f"Error getting departments list: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/departments/<int:id>', methods=['GET'])
def api_get_department(id):
    try:
        from models.Department import Department
        department = Department.query.get(id)
        if not department:
            return jsonify({'success': False, 'message': 'Không tìm thấy khoa'})
        
        return jsonify({'success': True, 'department': department.to_dict()})
    except Exception as e:
        print(f"Error getting department: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/departments/<int:id>', methods=['PUT'])
def api_update_department(id):
    try:
        from models.Department import Department
        department = Department.query.get(id)
        if not department:
            return jsonify({'success': False, 'message': 'Không tìm thấy khoa'})
        
        data = request.get_json()
        
        # Check for existing department with same code/name (exclude current)
        if data.get('code') and data['code'] != department.code:
            existing_code = Department.query.filter_by(code=data['code']).first()
            if existing_code:
                return jsonify({'success': False, 'message': 'Mã khoa này đã tồn tại'})
        
        if data.get('name') and data['name'] != department.name:
            existing_name = Department.query.filter_by(name=data['name']).first()
            if existing_name:
                return jsonify({'success': False, 'message': 'Tên khoa này đã tồn tại'})
        
        # Update fields
        department.code = data.get('code', department.code)
        department.name = data.get('name', department.name)
        department.abbreviation = data.get('abbreviation', department.abbreviation)
        department.description = data.get('description', department.description)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Khoa đã được cập nhật thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating department: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/departments/<int:id>', methods=['DELETE'])
def api_delete_department(id):
    try:
        from models.Department import Department
        department = Department.query.get(id)
        if not department:
            return jsonify({'success': False, 'message': 'Không tìm thấy khoa'})
        
        # Check if any teachers are using this department using safe method
        teacher_count = department.get_teachers_count()
        if teacher_count > 0:
            return jsonify({'success': False, 'message': f'Không thể xóa khoa đang được sử dụng bởi {teacher_count} giảng viên'})
        
        # Check if any subjects are using this department using safe method
        subject_count = department.get_subjects_count()
        if subject_count > 0:
            return jsonify({'success': False, 'message': f'Không thể xóa khoa đang được sử dụng bởi {subject_count} học phần'})
        
        db.session.delete(department)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Khoa đã được xóa thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting department: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Teaching Assignments
@app.route('/api/teaching-assignments', methods=['POST'])
def create_teaching_assignment():
    try:
        if 'TeachingAssignment' not in globals():
            return jsonify({'success': False, 'message': 'TeachingAssignment model not available'})
            
        data = request.get_json()
        print(f"Received teaching assignment data: {data}")  # Debug log
        
        if not data:
            return jsonify({'success': False, 'message': 'Không có dữ liệu được gửi'})
        
        # Validate required fields
        required_fields = ['teacher_id', 'subject_id', 'class_code', 'planned_hours', 'start_date', 'end_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        # Validate teacher exists
        teacher = Teacher.query.get(data['teacher_id'])
        if not teacher:
            return jsonify({'success': False, 'message': 'Giảng viên không tồn tại'})
        
        # Validate subject exists
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify({'success': False, 'message': 'Học phần không tồn tại'})
        
        # Validate semester if provided
        if data.get('semester_id'):
            semester = Semester.query.get(data['semester_id'])
            if not semester:
                return jsonify({'success': False, 'message': 'Kỳ học không tồn tại'})
        
        # Import TeachingAssignment model
        from models.teaching_assignment import TeachingAssignment
        
        # Parse dates safely
        from datetime import datetime as dt_parser
        start_date = dt_parser.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = dt_parser.strptime(data['end_date'], '%Y-%m-%d').date()
        
        assignment = TeachingAssignment(
            teacher_id=data['teacher_id'],
            subject_id=data['subject_id'],
            semester_id=data.get('semester_id'),
            class_code=data['class_code'],
            class_student_count=data.get('class_student_count', 0),
            planned_hours=data['planned_hours'],
            actual_hours=data.get('actual_hours', 0),
            start_date=start_date,
            end_date=end_date,
            notes=data.get('notes', ''),
            status='assigned'
        )
        
        # Calculate payment if method exists
        if hasattr(assignment, 'calculate_payment'):
            assignment.calculate_payment()
        
        db.session.add(assignment)
        db.session.commit()
        
        print(f"Teaching assignment created successfully: {assignment.to_dict()}")  # Debug log
        
        return jsonify({
            'success': True, 
            'message': 'Phân công giảng dạy đã được tạo thành công!',
            'assignment': assignment.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating teaching assignment: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Lỗi hệ thống: {str(e)}'})

@app.route('/api/teaching-assignments/list', methods=['GET'])
def get_teaching_assignments_list():
    try:
        if 'TeachingAssignment' not in globals():
            return jsonify({'success': False, 'message': 'TeachingAssignment model not available'})
        
        # Get filter parameters
        teacher_id = request.args.get('teacher_id')
        semester_id = request.args.get('semester_id')
        
        query = TeachingAssignment.query
        if teacher_id:
            query = query.filter_by(teacher_id=teacher_id)
        if semester_id:
            query = query.filter_by(semester_id=semester_id)
        
        assignments = query.order_by(TeachingAssignment.created_at.desc()).all()
        assignments_data = [assignment.to_dict() for assignment in assignments]
        
        return jsonify({'success': True, 'teaching_assignments': assignments_data})
    except Exception as e:
        print(f"Error getting teaching assignments list: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teaching-assignments/<int:id>', methods=['GET'])
def get_teaching_assignment(id):
    try:
        if 'TeachingAssignment' not in globals():
            return jsonify({'success': False, 'message': 'TeachingAssignment model not available'})
            
        assignment = TeachingAssignment.query.get(id)
        if not assignment:
            return jsonify({'success': False, 'message': 'Không tìm thấy phân công'})
        
        return jsonify({'success': True, 'assignment': assignment.to_dict()})
        
    except Exception as e:
        print(f"Error getting teaching assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teaching-assignments/<int:id>', methods=['PUT'])
def api_update_teaching_assignment(id):
    try:
        if 'TeachingAssignment' not in globals():
            return jsonify({'success': False, 'message': 'TeachingAssignment model not available'})
            
        assignment = TeachingAssignment.query.get(id)
        if not assignment:
            return jsonify({'success': False, 'message': 'Không tìm thấy phân công'})
        
        data = request.get_json()
        
        # Update fields
        assignment.actual_hours = data.get('actual_hours', assignment.actual_hours)
        assignment.class_student_count = data.get('class_student_count', assignment.class_student_count)
        assignment.notes = data.get('notes', assignment.notes)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Phân công đã được cập nhật thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating teaching assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/teaching-assignments/<int:id>', methods=['DELETE'])
def api_delete_teaching_assignment(id):
    try:
        if 'TeachingAssignment' not in globals():
            return jsonify({'success': False, 'message': 'TeachingAssignment model not available'})
            
        assignment = TeachingAssignment.query.get(id)
        if not assignment:
            return jsonify({'success': False, 'message': 'Không tìm thấy phân công'})
        
        db.session.delete(assignment)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Phân công đã được xóa thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting teaching assignment: {e}")
        return jsonify({'success': False, 'message': str(e)})

# Salary Management API Routes
@app.route('/api/salary-settings', methods=['GET'])
def api_get_salary_settings():
    try:
        settings = get_default_salary_settings()
        return jsonify({'success': True, 'settings': settings})
    except Exception as e:
        print(f"Error getting salary settings API: {e}")
        return jsonify({'success': False, 'message': str(e)})

def get_default_salary_settings():
    """Get default salary settings"""
    try:
        from models.salary_setting import SalarySetting
        
        base_rate = SalarySetting.get_setting('base_hourly_rate', '100000')
        
        return {
            'base_hourly_rate': int(base_rate),
            'degree_coefficients': {
                'dai_hoc': float(SalarySetting.get_setting('degree_coeff_dai_hoc', '1.0')),
                'thac_si': float(SalarySetting.get_setting('degree_coeff_thac_si', '1.2')),
                'tien_si': float(SalarySetting.get_setting('degree_coeff_tien_si', '1.5')),
                'pho_giao_su': float(SalarySetting.get_setting('degree_coeff_pho_giao_su', '1.8')),
                'giao_su': float(SalarySetting.get_setting('degree_coeff_giao_su', '2.0'))
            },
            'class_coefficients': {
                'under_20': float(SalarySetting.get_setting('class_coeff_under_20', '-0.3')),
                '20_29': float(SalarySetting.get_setting('class_coeff_20_29', '-0.2')),
                '30_39': float(SalarySetting.get_setting('class_coeff_30_39', '-0.1')),
                '40_49': float(SalarySetting.get_setting('class_coeff_40_49', '0.0')),
                '50_59': float(SalarySetting.get_setting('class_coeff_50_59', '0.1')),
                '60_69': float(SalarySetting.get_setting('class_coeff_60_69', '0.2')),
                '70_79': float(SalarySetting.get_setting('class_coeff_70_79', '0.3')),
                'over_80': float(SalarySetting.get_setting('class_coeff_over_80', '0.4'))
            }
        }
    except:
        return {
            'base_hourly_rate': 100000,
            'degree_coefficients': {
                'dai_hoc': 1.0, 'thac_si': 1.2, 'tien_si': 1.5,
                'pho_giao_su': 1.8, 'giao_su': 2.0
            },
            'class_coefficients': {
                'under_20': -0.3, '20_29': -0.2, '30_39': -0.1, '40_49': 0.0,
                '50_59': 0.1, '60_69': 0.2, '70_79': 0.3, 'over_80': 0.4
            }
        }

# API Routes for Salary Settings
@app.route('/api/salary-settings', methods=['POST'])
def api_update_salary_settings():
    try:
        data = request.get_json()
        
        try:
            from models.salary_setting import SalarySetting
            
            # Update base hourly rate
            if 'base_hourly_rate' in data:
                SalarySetting.set_setting('base_hourly_rate', data['base_hourly_rate'], 'Định mức tiền theo tiết')
            
            # Update degree coefficients
            if 'degree_coefficients' in data:
                for degree, coeff in data['degree_coefficients'].items():
                    SalarySetting.set_setting(f'degree_coeff_{degree}', coeff, f'Hệ số bằng cấp {degree}')
            
            # Update class coefficients
            if 'class_coefficients' in data:
                for class_range, coeff in data['class_coefficients'].items():
                    SalarySetting.set_setting(f'class_coeff_{class_range}', coeff, f'Hệ số lớp {class_range}')
        except ImportError:
            # If SalarySetting model not available, just return success
            pass
        
        return jsonify({'success': True, 'message': 'Cài đặt đã được cập nhật thành công!'})
    except Exception as e:
        print(f"Error updating salary settings: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/salary-calculate', methods=['POST'])
def api_calculate_salary():
    try:
        data = request.get_json()
        teacher_id = data.get('teacher_id')
        semester_id = data.get('semester_id')
        
        if not teacher_id:
            return jsonify({'success': False, 'message': 'Vui lòng chọn giảng viên'})
        
        result = calculate_teacher_salary_detailed(teacher_id, semester_id)
        
        if 'error' in result:
            return jsonify({'success': False, 'message': result['error']})
        
        # Save calculation result
        try:
            from models.salary_calculation import SalaryCalculation
            calculation = SalaryCalculation(
                teacher_id=teacher_id,
                semester_id=semester_id,
                total_hours=result['total_hours'],
                adjusted_hours=result['adjusted_hours'],
                total_amount=result['total_amount'],
                base_hourly_rate=result['base_hourly_rate'],
                teacher_coefficient=result['teacher_coefficient']
            )
            db.session.add(calculation)
            db.session.commit()
        except Exception as e:
            print(f"Error saving calculation: {e}")
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        print(f"Error calculating salary: {e}")
        return jsonify({'success': False, 'message': str(e)})

def calculate_teacher_salary_detailed(teacher_id, semester_id=None):
    """Calculate detailed salary for a teacher"""
    try:
        if 'Teacher' not in globals():
            return {'error': 'Teacher model not available'}
        
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {'error': 'Không tìm thấy giảng viên'}
        
        settings = get_default_salary_settings()
        assignments = []
        total_hours = 0
        adjusted_hours = 0
        
        # Get teaching assignments
        try:
            if 'TeachingAssignment' in globals():
                query = TeachingAssignment.query.filter_by(teacher_id=teacher_id)
                if semester_id:
                    query = query.filter_by(semester_id=semester_id)
                
                teaching_assignments = query.all()
                
                for assignment in teaching_assignments:
                    assignment_dict = assignment.to_dict()
                    assignments.append(assignment_dict)
                    total_hours += assignment_dict.get('actual_hours', 0)
                    adjusted_hours += assignment_dict.get('calculated_adjusted_hours', 0)
        except Exception as e:
            print(f"Error getting teaching assignments: {e}")
        
        # Calculate total amount
        teacher_coeff = teacher.effective_teacher_coefficient if hasattr(teacher, 'effective_teacher_coefficient') else 1.5
        base_rate = settings['base_hourly_rate']
        total_amount = adjusted_hours * teacher_coeff * base_rate
        
        # Get department name safely
        department_name = 'N/A'
        try:
            if hasattr(teacher, 'department_id') and teacher.department_id:
                department = Department.query.get(teacher.department_id)
                if department:
                    department_name = department.name
        except:
            pass
        
        return {
            'teacher_id': teacher_id,
            'teacher_name': teacher.name,
            'department_name': department_name,
            'total_hours': total_hours,
            'adjusted_hours': adjusted_hours,
            'total_amount': total_amount,
            'base_hourly_rate': base_rate,
            'teacher_coefficient': teacher_coeff,
            'assignments': assignments
        }
    except Exception as e:
        print(f"Error in calculate_teacher_salary_detailed: {e}")
        return {'error': str(e)}

@app.route('/api/salary-calculations/list', methods=['GET'])
def api_get_salary_calculations_list():
    try:
        try:
            from models.salary_calculation import SalaryCalculation
            calculations = SalaryCalculation.query.order_by(SalaryCalculation.created_at.desc()).all()
            calculations_data = [calc.to_dict() for calc in calculations]
            return jsonify({'success': True, 'calculations': calculations_data})
        except Exception as db_error:
            print(f"Database error in api_get_salary_calculations_list: {db_error}")
            # Return empty list if table doesn't exist or has issues
            return jsonify({'success': True, 'calculations': []})
    except Exception as e:
        print(f"Error getting salary calculations list: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/salary-calculations/<int:id>', methods=['GET'])
def api_get_salary_calculation(id):
    try:
        try:
            from models.salary_calculation import SalaryCalculation
            calculation = SalaryCalculation.query.get(id)
            if not calculation:
                return jsonify({'success': False, 'message': 'Không tìm thấy kết quả tính toán'})
            
            return jsonify({'success': True, 'calculation': calculation.to_dict()})
        except ImportError:
            return jsonify({'success': False, 'message': 'SalaryCalculation model not available'})
    except Exception as e:
        print(f"Error getting salary calculation: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/salary-calculations/<int:id>/approve', methods=['POST'])
def api_approve_salary_calculation(id):
    try:
        try:
            from models.salary_calculation import SalaryCalculation
            calculation = SalaryCalculation.query.get(id)
            if not calculation:
                return jsonify({'success': False, 'message': 'Không tìm thấy kết quả tính toán'})
            
            data = request.get_json()
            calculation.is_approved = True
            calculation.approved_by = data.get('approved_by', 'Admin')
            calculation.approved_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Kết quả tính toán đã được duyệt!'})
        except ImportError:
            return jsonify({'success': False, 'message': 'SalaryCalculation model not available'})
    except Exception as e:
        db.session.rollback()
        print(f"Error approving salary calculation: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/salary-calculations/<int:id>', methods=['DELETE'])
def api_delete_salary_calculation(id):
    try:
        try:
            from models.salary_calculation import SalaryCalculation
            calculation = SalaryCalculation.query.get(id)
            if not calculation:
                return jsonify({'success': False, 'message': 'Không tìm thấy kết quả tính toán'})
            
            db.session.delete(calculation)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Kết quả tính toán đã được xóa!'})
        except ImportError:
            return jsonify({'success': False, 'message': 'SalaryCalculation model not available'})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting salary calculation: {e}")
        return jsonify({'success': False, 'message': str(e)})

# API Routes for Class Sections
@app.route('/api/class-sections', methods=['POST'])
def create_class_section():
    try:
        if 'ClassSection' not in globals():
            return jsonify({'success': False, 'message': 'ClassSection model not available'})
            
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'Không có dữ liệu được gửi'})
        
        # Validate required fields
        required_fields = ['code', 'name', 'subject_id', 'semester_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} không được để trống'})
        
        # Check for existing class section
        from models.class_section import ClassSection
        existing = ClassSection.query.filter_by(code=data['code']).first()
        if existing:
            return jsonify({'success': False, 'message': 'Mã lớp này đã tồn tại'})
        
        # Validate foreign keys
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify({'success': False, 'message': 'Học phần không tồn tại'})
        
        semester = Semester.query.get(data['semester_id'])
        if not semester:
            return jsonify({'success': False, 'message': 'Kỳ học không tồn tại'})
        
        class_section = ClassSection(
            code=data['code'],
            name=data['name'],
            subject_id=data['subject_id'],
            semester_id=data['semester_id'],
            teacher_id=data.get('teacher_id') if data.get('teacher_id') else None,
            student_count=data.get('student_count', 0),
            max_students=data.get('max_students', 50),
            classroom=data.get('classroom'),
            schedule_info=data.get('schedule_info'),
            notes=data.get('notes'),
            status='planned'
        )
        
        db.session.add(class_section)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Lớp học phần đã được tạo thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating class section: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/class-sections/list', methods=['GET'])
def get_class_sections_list():
    try:
        if 'ClassSection' not in globals():
            return jsonify({'success': False, 'message': 'ClassSection model not available'})
        
        # Get filter parameters
        teacher_id = request.args.get('teacher_id')
        subject_id = request.args.get('subject_id')
        semester_id = request.args.get('semester_id')
        
        query = ClassSection.query.filter_by(is_active=True)
        if teacher_id:
            query = query.filter_by(teacher_id=teacher_id)
        if subject_id:
            query = query.filter_by(subject_id=subject_id)
        if semester_id:
            query = query.filter_by(semester_id=semester_id)
        
        class_sections = query.order_by(ClassSection.created_at.desc()).all()
        class_sections_data = [section.to_dict() for section in class_sections]
        
        return jsonify({'success': True, 'class_sections': class_sections_data})
    except Exception as e:
        print(f"Error getting class sections list: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/class-sections/<int:id>', methods=['GET'])
def api_get_class_section(id):
    try:
        try:
            from models.class_section import ClassSection
        except ImportError:
            return jsonify({'success': False, 'message': 'ClassSection model not available'})
            
        class_section = ClassSection.query.get(id)
        if not class_section:
            return jsonify({'success': False, 'message': 'Không tìm thấy lớp học phần'})
        
        return jsonify({'success': True, 'class_section': class_section.to_dict()})
    except Exception as e:
        print(f"Error getting class section: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/class-sections/<int:id>', methods=['PUT'])
def api_update_class_section(id):
    try:
        try:
            from models.class_section import ClassSection
        except ImportError:
            return jsonify({'success': False, 'message': 'ClassSection model not available'})
            
        class_section = ClassSection.query.get(id)
        if not class_section:
            return jsonify({'success': False, 'message': 'Không tìm thấy lớp học phần'})
        
        data = request.get_json()
        
        # Check for existing class section with same code (exclude current)
        if data.get('code') and data['code'] != class_section.code:
            existing_code = ClassSection.query.filter_by(code=data['code']).first()
            if existing_code:
                return jsonify({'success': False, 'message': 'Mã lớp này đã tồn tại'})
        
        # Update fields
        class_section.code = data.get('code', class_section.code)
        class_section.name = data.get('name', class_section.name)
        class_section.student_count = data.get('student_count', class_section.student_count)
        class_section.max_students = data.get('max_students', class_section.max_students)
        class_section.classroom = data.get('classroom', class_section.classroom)
        class_section.schedule_info = data.get('schedule_info', class_section.schedule_info)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Lớp học phần đã được cập nhật thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating class section: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/class-sections/<int:id>', methods=['DELETE'])
def api_delete_class_section(id):
    try:
        try:
            from models.class_section import ClassSection
        except ImportError:
            return jsonify({'success': False, 'message': 'ClassSection model not available'})
            
        class_section = ClassSection.query.get(id)
        if not class_section:
            return jsonify({'success': False, 'message': 'Không tìm thấy lớp học phần'})
        
        # Check if any teaching assignments are using this class
        try:
            if 'TeachingAssignment' in globals():
                assignment_count = TeachingAssignment.query.filter_by(class_code=class_section.code).count()
                if assignment_count > 0:
                    return jsonify({'success': False, 'message': f'Không thể xóa lớp đang có {assignment_count} phân công giảng dạy'})
        except:
            pass
        
        db.session.delete(class_section)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Lớp học phần đã được xóa thành công!'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting class section: {e}")
        return jsonify({'success': False, 'message': str(e)})

# Statistics API Routes
@app.route('/api/statistics/teacher', methods=['GET'])
def api_teacher_statistics():
    try:
        stats = calculate_teacher_statistics()
        return jsonify({'success': True, 'statistics': stats})
    except Exception as e:
        print(f"Error getting teacher statistics: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/statistics/class', methods=['GET'])
def api_class_statistics():
    try:
        stats = calculate_class_statistics()
        return jsonify({'success': True, 'statistics': stats})
    except Exception as e:
        print(f"Error getting class statistics: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/statistics/subject', methods=['GET'])
def api_subject_statistics():
    try:
        stats = calculate_subject_statistics()
        return jsonify({'success': True, 'statistics': stats})
    except Exception as e:
        print(f"Error getting subject statistics: {e}")
        return jsonify({'success': False, 'message': str(e)})

# Reports Routes
@app.route('/reports')
def reports():
    try:
        teachers_list = []
        departments_list = []
        semesters_list = []
        years_list = []
        
        if 'Teacher' in globals():
            teachers_list = Teacher.query.filter_by(is_active=True).order_by(Teacher.name).all()
        if 'Department' in globals():
            departments_list = Department.query.filter_by(is_active=True).order_by(Department.name).all()
        if 'Semester' in globals():
            semesters_list = Semester.query.filter_by(is_active=True).order_by(Semester.year.desc(), Semester.name).all()
            # Get unique years
            years_query = db.session.query(Semester.year).filter_by(is_active=True).distinct().order_by(Semester.year.desc()).all()
            years_list = [year[0] for year in years_query]
        
        current_year = datetime.now().year
        if current_year not in years_list:
            years_list.insert(0, current_year)
        
        return render_template('reports.html',
                             teachers=teachers_list,
                             departments=departments_list,
                             semesters=semesters_list,
                             years=years_list,
                             current_year=current_year)
    except Exception as e:
        print(f"Error in reports route: {e}")
        return render_template('reports.html', 
                             teachers=[], departments=[], semesters=[], years=[], current_year=datetime.now().year)

# API Routes for Reports
@app.route('/api/reports/teacher-yearly', methods=['POST'])
def api_teacher_yearly_report():
    try:
        data = request.get_json()
        teacher_id = data.get('teacher_id')
        year = data.get('year')
        
        if not teacher_id or not year:
            return jsonify({'success': False, 'message': 'Vui lòng chọn giảng viên và năm'})
        
        # Get teacher info
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return jsonify({'success': False, 'message': 'Không tìm thấy giảng viên'})
        
        # Get department name
        department_name = 'N/A'
        if teacher.department_id:
            department = Department.query.get(teacher.department_id)
            if department:
                department_name = department.name
        
        # Get semesters in the year
        semesters = Semester.query.filter_by(year=int(year), is_active=True).all()
        
        report_data = {
            'teacher_info': {
                'id': teacher.id,
                'name': teacher.name,
                'employee_code': teacher.employee_code or '',
                'department_name': department_name
            },
            'year': int(year),
            'semesters': [],
            'total_hours': 0,
            'total_adjusted_hours': 0,
            'total_amount': 0
        }
        
        # Calculate for each semester
        for semester in semesters:
            semester_data = calculate_teacher_salary_detailed(teacher_id, semester.id)
            
            if 'error' not in semester_data:
                semester_info = {
                    'semester_id': semester.id,
                    'semester_name': semester.name,
                    'total_hours': semester_data.get('total_hours', 0),
                    'adjusted_hours': semester_data.get('adjusted_hours', 0),
                    'total_amount': semester_data.get('total_amount', 0),
                    'assignments': semester_data.get('assignments', [])
                }
                
                report_data['semesters'].append(semester_info)
                report_data['total_hours'] += semester_info['total_hours']
                report_data['total_adjusted_hours'] += semester_info['adjusted_hours']
                report_data['total_amount'] += semester_info['total_amount']
        
        return jsonify({'success': True, 'report': report_data})
        
    except Exception as e:
        print(f"Error generating teacher yearly report: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/reports/department-salary', methods=['POST'])
def api_department_salary_report():
    try:
        data = request.get_json()
        department_id = data.get('department_id')
        semester_id = data.get('semester_id')
        year = data.get('year')
        
        if not department_id:
            return jsonify({'success': False, 'message': 'Vui lòng chọn khoa'})
        
        # Get department info
        department = Department.query.get(department_id)
        if not department:
            return jsonify({'success': False, 'message': 'Không tìm thấy khoa'})
        
        # Get teachers in department
        teachers = Teacher.query.filter_by(department_id=department_id, is_active=True).all()
        
        report_data = {
            'department_info': {
                'id': department.id,
                'name': department.name,
                'code': department.code
            },
            'period_info': {},
            'teachers': [],
            'total_hours': 0,
            'total_adjusted_hours': 0,
            'total_amount': 0
        }
        
        # Set period info
        if semester_id:
            semester = Semester.query.get(semester_id)
            if semester:
                report_data['period_info'] = {
                    'type': 'semester',
                    'semester_name': semester.name,
                    'year': semester.year
                }
        elif year:
            report_data['period_info'] = {
                'type': 'year',
                'year': int(year)
            }
        
        # Calculate for each teacher
        for teacher in teachers:
            if semester_id:
                # Calculate for specific semester
                teacher_data = calculate_teacher_salary_detailed(teacher.id, semester_id)
            elif year:
                # Calculate for whole year
                teacher_data = calculate_teacher_yearly_salary(teacher.id, int(year))
            else:
                # Calculate for all time
                teacher_data = calculate_teacher_salary_detailed(teacher.id)
            
            if 'error' not in teacher_data:
                teacher_info = {
                    'teacher_id': teacher.id,
                    'teacher_name': teacher.name,
                    'employee_code': teacher.employee_code or '',
                    'total_hours': teacher_data.get('total_hours', 0),
                    'adjusted_hours': teacher_data.get('adjusted_hours', 0),
                    'total_amount': teacher_data.get('total_amount', 0),
                    'assignments_count': len(teacher_data.get('assignments', []))
                }
                
                report_data['teachers'].append(teacher_info)
                report_data['total_hours'] += teacher_info['total_hours']
                report_data['total_adjusted_hours'] += teacher_info['adjusted_hours']
                report_data['total_amount'] += teacher_info['total_amount']
        
        # Sort teachers by total amount (descending)
        report_data['teachers'].sort(key=lambda x: x['total_amount'], reverse=True)
        
        return jsonify({'success': True, 'report': report_data})
        
    except Exception as e:
        print(f"Error generating department salary report: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/reports/school-salary', methods=['POST'])
def api_school_salary_report():
    try:
        data = request.get_json()
        semester_id = data.get('semester_id')
        year = data.get('year')
        
        # Get all departments
        departments = Department.query.filter_by(is_active=True).order_by(Department.name).all()
        
        report_data = {
            'period_info': {},
            'departments': [],
            'total_hours': 0,
            'total_adjusted_hours': 0,
            'total_amount': 0,
            'total_teachers': 0
        }
        
        # Set period info
        if semester_id:
            semester = Semester.query.get(semester_id)
            if semester:
                report_data['period_info'] = {
                    'type': 'semester',
                    'semester_name': semester.name,
                    'year': semester.year
                }
        elif year:
            report_data['period_info'] = {
                'type': 'year',
                'year': int(year)
            }
        
        # Calculate for each department
        for department in departments:
            teachers = Teacher.query.filter_by(department_id=department.id, is_active=True).all()
            
            dept_data = {
                'department_id': department.id,
                'department_name': department.name,
                'department_code': department.code,
                'teachers_count': len(teachers),
                'total_hours': 0,
                'total_adjusted_hours': 0,
                'total_amount': 0,
                'top_teachers': []
            }
            
            # Calculate for each teacher in department
            teacher_amounts = []
            for teacher in teachers:
                if semester_id:
                    teacher_data = calculate_teacher_salary_detailed(teacher.id, semester_id)
                elif year:
                    teacher_data = calculate_teacher_yearly_salary(teacher.id, int(year))
                else:
                    teacher_data = calculate_teacher_salary_detailed(teacher.id)
                
                if 'error' not in teacher_data:
                    teacher_amount = teacher_data.get('total_amount', 0)
                    teacher_hours = teacher_data.get('total_hours', 0)
                    teacher_adjusted_hours = teacher_data.get('adjusted_hours', 0)
                    
                    dept_data['total_hours'] += teacher_hours
                    dept_data['total_adjusted_hours'] += teacher_adjusted_hours
                    dept_data['total_amount'] += teacher_amount
                    
                    if teacher_amount > 0:
                        teacher_amounts.append({
                            'name': teacher.name,
                            'employee_code': teacher.employee_code or '',
                            'amount': teacher_amount
                        })
            
            # Get top 3 teachers by amount
            teacher_amounts.sort(key=lambda x: x['amount'], reverse=True)
            dept_data['top_teachers'] = teacher_amounts[:3]
            
            if dept_data['total_amount'] > 0 or dept_data['teachers_count'] > 0:
                report_data['departments'].append(dept_data)
                report_data['total_hours'] += dept_data['total_hours']
                report_data['total_adjusted_hours'] += dept_data['total_adjusted_hours']
                report_data['total_amount'] += dept_data['total_amount']
                report_data['total_teachers'] += dept_data['teachers_count']
        
        # Sort departments by total amount (descending)
        report_data['departments'].sort(key=lambda x: x['total_amount'], reverse=True)
        
        return jsonify({'success': True, 'report': report_data})
        
    except Exception as e:
        print(f"Error generating school salary report: {e}")
        return jsonify({'success': False, 'message': str(e)})

def calculate_teacher_yearly_salary(teacher_id, year):
    """Calculate teacher salary for entire year"""
    try:
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {'error': 'Không tìm thấy giảng viên'}
        
        # Get all semesters in year
        semesters = Semester.query.filter_by(year=year, is_active=True).all()
        
        total_hours = 0
        total_adjusted_hours = 0
        all_assignments = []
        
        for semester in semesters:
            semester_data = calculate_teacher_salary_detailed(teacher_id, semester.id)
            if 'error' not in semester_data:
                total_hours += semester_data.get('total_hours', 0)
                total_adjusted_hours += semester_data.get('adjusted_hours', 0)
                all_assignments.extend(semester_data.get('assignments', []))
        
        # Calculate total amount
        settings = get_default_salary_settings()
        teacher_coeff = teacher.effective_teacher_coefficient if hasattr(teacher, 'effective_teacher_coefficient') else 1.5
        base_rate = settings['base_hourly_rate']
        total_amount = total_adjusted_hours * teacher_coeff * base_rate
        
        return {
            'teacher_id': teacher_id,
            'teacher_name': teacher.name,
            'total_hours': total_hours,
            'adjusted_hours': total_adjusted_hours,
            'total_amount': total_amount,
            'base_hourly_rate': base_rate,
            'teacher_coefficient': teacher_coeff,
            'assignments': all_assignments
        }
    except Exception as e:
        print(f"Error calculating yearly salary: {e}")
        return {'error': str(e)}

# Make sure app runs
if __name__ == '__main__':
    try:
        print("🚀 Starting Flask application...")
        print(f"📍 App will be available at: http://127.0.0.1:5000")
        print("🔄 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except Exception as e:
        print(f"❌ Failed to start app: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")