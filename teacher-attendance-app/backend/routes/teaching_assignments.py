from flask import Blueprint, request, jsonify
from models.teaching_assignment import TeachingAssignment
from models.teacher import Teacher
from models.subject import Subject
from models.semester import Semester

teaching_assignments_bp = Blueprint('teaching_assignments', __name__)

@teaching_assignments_bp.route('/teaching-assignments', methods=['GET'])
def get_teaching_assignments():
    assignments = TeachingAssignment.query.all()
    return jsonify([assignment.to_dict() for assignment in assignments])

@teaching_assignments_bp.route('/teaching-assignments', methods=['POST'])
def create_teaching_assignment():
    try:
        data = request.json
        
        assignment = TeachingAssignment(
            teacher_id=data['teacher_id'],
            subject_id=data['subject_id'],
            semester_id=data.get('semester_id'),
            class_code=data['class_code'],
            planned_hours=data['planned_hours'],
            hourly_rate=data['hourly_rate'],
            start_date=data['start_date'],
            end_date=data['end_date']
        )
        
        if assignment.save():
            return jsonify({'success': True, 'message': 'Phân công giảng dạy đã được tạo'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi lưu phân công'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@teaching_assignments_bp.route('/teaching-assignments/<int:id>', methods=['PUT'])
def update_teaching_assignment(id):
    try:
        assignment = TeachingAssignment.get_by_id(id)
        if not assignment:
            return jsonify({'success': False, 'message': 'Không tìm thấy phân công'})
        
        data = request.json
        
        assignment.class_code = data.get('class_code', assignment.class_code)
        assignment.planned_hours = data.get('planned_hours', assignment.planned_hours)
        assignment.actual_hours = data.get('actual_hours', assignment.actual_hours)
        assignment.hourly_rate = data.get('hourly_rate', assignment.hourly_rate)
        assignment.total_amount = assignment.calculated_amount
        
        if assignment.save():
            return jsonify({'success': True, 'message': 'Phân công đã được cập nhật'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi cập nhật phân công'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@teaching_assignments_bp.route('/teaching-assignments/<int:id>', methods=['DELETE'])
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
        return jsonify({'success': False, 'message': str(e)})