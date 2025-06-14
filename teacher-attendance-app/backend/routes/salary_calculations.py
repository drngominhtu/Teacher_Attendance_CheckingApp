from flask import Blueprint, request, jsonify
from models.salary_calculation import SalaryCalculation
from models.teacher import Teacher
from models.teaching_assignment import TeachingAssignment
from datetime import datetime

salary_calculations_bp = Blueprint('salary_calculations', __name__)

@salary_calculations_bp.route('/salary-calculations', methods=['GET'])
def get_salary_calculations():
    calculations = SalaryCalculation.query.all()
    return jsonify([calc.to_dict() for calc in calculations])

@salary_calculations_bp.route('/salary-calculations', methods=['POST'])
def create_salary_calculation():
    try:
        data = request.json
        
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
        return jsonify({'success': False, 'message': str(e)})

@salary_calculations_bp.route('/salary-calculations/<int:id>/calculate', methods=['POST'])
def auto_calculate_salary(id):
    try:
        calculation = SalaryCalculation.get_by_id(id)
        if not calculation:
            return jsonify({'success': False, 'message': 'Không tìm thấy bảng lương'})
        
        # Tự động tính toán từ teaching assignments
        teacher_assignments = TeachingAssignment.query.filter_by(
            teacher_id=calculation.teacher_id,
            is_approved=True
        ).all()
        
        total_hours = sum(assignment.actual_hours for assignment in teacher_assignments)
        total_amount = sum(assignment.calculated_amount for assignment in teacher_assignments)
        
        calculation.teaching_hours = total_hours
        calculation.teaching_amount = total_amount
        calculation.calculate_totals()
        calculation.status = 'calculated'
        calculation.calculated_at = datetime.utcnow()
        
        if calculation.save():
            return jsonify({'success': True, 'message': 'Lương đã được tính toán tự động'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi tính toán lương'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@salary_calculations_bp.route('/salary-calculations/<int:id>/approve', methods=['POST'])
def approve_salary_calculation(id):
    try:
        calculation = SalaryCalculation.get_by_id(id)
        if not calculation:
            return jsonify({'success': False, 'message': 'Không tìm thấy bảng lương'})
        
        data = request.json
        calculation.status = 'approved'
        calculation.approved_by = data.get('approved_by')
        calculation.approved_at = datetime.utcnow()
        
        if calculation.save():
            return jsonify({'success': True, 'message': 'Bảng lương đã được duyệt'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi duyệt bảng lương'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@salary_calculations_bp.route('/salary-calculations/<int:id>', methods=['DELETE'])
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
        return jsonify({'success': False, 'message': str(e)})