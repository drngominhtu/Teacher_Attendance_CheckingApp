from flask import Blueprint

# Initialize the routes blueprint
routes_bp = Blueprint('routes', __name__)

# Import routes to register them with the blueprint
from .subjects import subjects_bp
from .semesters import semesters_bp
from .schedules import schedules_bp
from .teachers import teachers_bp
from .assignments import assignments_bp
from .teaching_assignments import teaching_assignments_bp
from .salary_calculations import salary_calculations_bp