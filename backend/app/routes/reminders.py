from flask import Blueprint, request, jsonify
from app.models.reminder.reminder import Reminder
from app.core.errors import ValidationError, NotFoundError

reminders_bp = Blueprint("reminders", __name__, url_prefix="/api/reminders")

@reminders_bp.post("/")
def create_reminder():
    """Create a new reminder"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        raise ValidationError('Title is required')
    
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        raise ValidationError('User ID is required')
    
    reminder_id = Reminder.create(user_id, data)
    return jsonify({'id': reminder_id, 'status': 'created'}), 201

@reminders_bp.get("/<user_id>")
def get_user_reminders(user_id):
    """Get all reminders for a user"""
    reminders = Reminder.find_by_user(user_id)
    return jsonify({'reminders': reminders, 'count': len(reminders)})

@reminders_bp.get("/<user_id>/<reminder_id>")
def get_reminder(user_id, reminder_id):
    """Get a specific reminder"""
    reminder = Reminder.find_by_id(reminder_id)
    
    if not reminder or str(reminder['user_id']) != user_id:
        raise NotFoundError('Reminder not found')
    
    # Convert ObjectId to string for JSON serialization
    reminder['_id'] = str(reminder['_id'])
    reminder['user_id'] = str(reminder['user_id'])
    
    return jsonify(reminder)

@reminders_bp.put("/<reminder_id>")
def update_reminder(reminder_id):
    """Update a reminder"""
    data = request.get_json()
    success = Reminder.update(reminder_id, data)
    
    if not success:
        raise NotFoundError('Reminder not found')
    
    return jsonify({'status': 'updated'})

@reminders_bp.delete("/<reminder_id>")
def delete_reminder(reminder_id):
    """Delete a reminder"""
    success = Reminder.delete(reminder_id)
    
    if not success:
        raise NotFoundError('Reminder not found')
    
    return jsonify({'status': 'deleted'})