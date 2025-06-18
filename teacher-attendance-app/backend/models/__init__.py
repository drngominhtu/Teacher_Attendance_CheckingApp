# Import theo thứ tự để tránh circular import
from .base import BaseModel

# Import models in correct order to avoid circular imports
models = {}

# Import base models first (no foreign keys)
try:
    from .degree import Degree
    models['Degree'] = Degree
    print("✓ Degree model imported")
except ImportError as e:
    print(f"✗ Could not import Degree model: {e}")

try:
    from .Department import Department  
    models['Department'] = Department
    print("✓ Department model imported")
except ImportError as e:
    print(f"✗ Could not import Department model: {e}")

try:
    from .semester import Semester
    models['Semester'] = Semester
    print("✓ Semester model imported")
except ImportError as e:
    print(f"✗ Could not import Semester model: {e}")

# Import models with foreign keys to base models
try:
    from .teacher import Teacher, EmployeeType
    models['Teacher'] = Teacher
    models['EmployeeType'] = EmployeeType
    print("✓ Teacher model imported")
except ImportError as e:
    print(f"✗ Could not import Teacher model: {e}")

try:
    from .subject import Subject
    models['Subject'] = Subject
    print("✓ Subject model imported")
except ImportError as e:
    print(f"✗ Could not import Subject model: {e}")

# Import models with foreign keys to other models
try:
    from .class_section import ClassSection
    models['ClassSection'] = ClassSection
    print("✓ ClassSection model imported")
except ImportError as e:
    print(f"✗ Could not import ClassSection model: {e}")

try:
    from .teaching_assignment import TeachingAssignment
    models['TeachingAssignment'] = TeachingAssignment
    print("✓ TeachingAssignment model imported")
except ImportError as e:
    print(f"✗ Could not import TeachingAssignment model: {e}")

# Import optional models
try:
    from .assignment import Assignment
    models['Assignment'] = Assignment
    print("✓ Assignment model imported")
except ImportError:
    print("Assignment model not found (optional)")

def setup_relationships():
    """Setup any additional relationships after all models are loaded"""
    pass

# Export what we have
__all__ = ['BaseModel', 'setup_relationships'] + list(models.keys())

# Add to globals for direct import
globals().update(models)