from flask import Blueprint, request, jsonify
from ..models.assignment import Assignment
from ..models.teacher import Teacher
from ..models.subject import Subject

assignments_bp = Blueprint('assignments', __name__)

@assignments_bp.route('/assignments', methods=['GET'])
def get_assignments():
    assignments = Assignment.query.all()
    return jsonify([assignment.to_dict() for assignment in assignments])

@assignments_bp.route('/assignments', methods=['POST'])
def create_assignment():
    data = request.json
    teacher_id = data.get('teacher_id')
    subject_id = data.get('subject_id')
    
    teacher = Teacher.query.get(teacher_id)
    subject = Subject.query.get(subject_id)
    
    if not teacher or not subject:
        return jsonify({'error': 'Invalid teacher or subject ID'}), 400
    
    assignment = Assignment(teacher_id=teacher_id, subject_id=subject_id)
    assignment.save()
    
    return jsonify(assignment.to_dict()), 201

@assignments_bp.route('/assignments/<int:id>', methods=['PUT'])
def update_assignment(id):
    data = request.json
    assignment = Assignment.query.get(id)
    
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    teacher_id = data.get('teacher_id')
    subject_id = data.get('subject_id')
    
    if teacher_id:
        assignment.teacher_id = teacher_id
    if subject_id:
        assignment.subject_id = subject_id
    
    assignment.save()
    
    return jsonify(assignment.to_dict())

@assignments_bp.route('/assignments/<int:id>', methods=['DELETE'])
def delete_assignment(id):
    assignment = Assignment.query.get(id)
    
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    assignment.delete()
    
    return jsonify({'message': 'Assignment deleted successfully'})