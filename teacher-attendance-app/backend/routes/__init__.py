from flask import Blueprint

# Initialize the routes blueprint
routes_bp = Blueprint('routes', __name__)

# Import routes to register them with the blueprint
from .subjects import *
from .semesters import *
from .schedules import *
from .teachers import *
from .assignments import *