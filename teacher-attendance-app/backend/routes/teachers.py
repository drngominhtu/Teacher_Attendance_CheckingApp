from flask import Blueprint, request, jsonify
from ..models.teacher import Teacher

teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/teachers', methods=['POST'])
def add_teacher():
    data = request.json
    new_teacher = Teacher(name=data['name'], department=data['department'], qualifications=data['qualifications'])
    new_teacher.save()
    return jsonify({'message': 'Teacher added successfully'}), 201

@teachers_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    data = request.json
    teacher = Teacher.get_by_id(teacher_id)
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404
    teacher.name = data['name']
    teacher.department = data['department']
    teacher.qualifications = data['qualifications']
    teacher.save()
    return jsonify({'message': 'Teacher updated successfully'})

@teachers_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    teacher = Teacher.get_by_id(teacher_id)
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404
    teacher.delete()
    return jsonify({'message': 'Teacher deleted successfully'})

@teachers_bp.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.get_all()
    return jsonify([teacher.to_dict() for teacher in teachers])