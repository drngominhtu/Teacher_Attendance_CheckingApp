from flask import Blueprint, request, jsonify
from ..models.semester import Semester

semesters_bp = Blueprint('semesters', __name__)

@semesters_bp.route('/semesters', methods=['POST'])
def add_semester():
    data = request.json
    new_semester = Semester(name=data['name'], year=data['year'])
    new_semester.save()
    return jsonify({'message': 'Semester added successfully', 'id': new_semester.id}), 201

@semesters_bp.route('/semesters/<int:id>', methods=['PUT'])
def update_semester(id):
    data = request.json
    semester = Semester.get_by_id(id)
    if semester:
        semester.name = data['name']
        semester.year = data['year']
        semester.save()
        return jsonify({'message': 'Semester updated successfully'}), 200
    return jsonify({'message': 'Semester not found'}), 404

@semesters_bp.route('/semesters/<int:id>', methods=['DELETE'])
def delete_semester(id):
    semester = Semester.get_by_id(id)
    if semester:
        semester.delete()
        return jsonify({'message': 'Semester deleted successfully'}), 200
    return jsonify({'message': 'Semester not found'}), 404

@semesters_bp.route('/semesters', methods=['GET'])
def get_semesters():
    semesters = Semester.get_all()
    return jsonify([semester.to_dict() for semester in semesters]), 200