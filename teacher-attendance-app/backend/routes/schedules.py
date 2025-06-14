from flask import Blueprint, request, jsonify
from models.schedule import Schedule

schedules_bp = Blueprint('schedules', __name__)

@schedules_bp.route('/schedules', methods=['GET'])
def get_schedules():
    schedules = Schedule.query.all()
    return jsonify([schedule.to_dict() for schedule in schedules]), 200

@schedules_bp.route('/schedules', methods=['POST'])
def create_schedule():
    data = request.get_json()
    new_schedule = Schedule(**data)
    new_schedule.save()
    return jsonify(new_schedule.to_dict()), 201

@schedules_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    data = request.get_json()
    schedule = Schedule.query.get_or_404(schedule_id)
    for key, value in data.items():
        setattr(schedule, key, value)
    schedule.save()
    return jsonify(schedule.to_dict()), 200

@schedules_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    schedule.delete()
    return jsonify({'message': 'Schedule deleted successfully'}), 204