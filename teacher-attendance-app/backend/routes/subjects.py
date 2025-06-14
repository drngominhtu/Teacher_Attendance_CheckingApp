from flask import Blueprint, request, jsonify
from ..models.subject import Subject

subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route('/subjects', methods=['POST'])
def add_subject():
    data = request.json
    subject = Subject(name=data['name'], department=data['department'])
    subject.save()
    return jsonify({'message': 'Subject added successfully', 'subject': subject.to_dict()}), 201

@subjects_bp.route('/subjects/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    data = request.json
    subject = Subject.get_by_id(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found'}), 404
    subject.name = data['name']
    subject.department = data['department']
    subject.save()
    return jsonify({'message': 'Subject updated successfully', 'subject': subject.to_dict()})

@subjects_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    subject = Subject.get_by_id(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found'}), 404
    subject.delete()
    return jsonify({'message': 'Subject deleted successfully'})