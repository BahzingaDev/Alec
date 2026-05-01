from flask import Blueprint, request, jsonify
from app.models.task.task import Task
from app.core.errors import ValidationError, NotFoundError

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

@tasks_bp.post("/")
def create_task():
    """Create a new task"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        raise ValidationError('Title is required')
    
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        raise ValidationError('User ID is required')
    
    task_id = Task.create(user_id, data)
    return jsonify({'id': task_id, 'status': 'created'}), 201

@tasks_bp.get("/<user_id>")
def get_user_tasks(user_id):
    """Get all tasks for a user"""
    tasks = Task.find_by_user(user_id)
    return jsonify({'tasks': tasks, 'count': len(tasks)})

@tasks_bp.get("/<user_id>/<task_id>")
def get_task(user_id, task_id):
    """Get a specific task"""
    task = Task.find_by_id(task_id)
    
    if not task or str(task['user_id']) != user_id:
        raise NotFoundError('Task not found')
    
    # Convert ObjectId to string for JSON serialization
    task['_id'] = str(task['_id'])
    task['user_id'] = str(task['user_id'])
    
    return jsonify(task)

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    """Update a task"""
    data = request.get_json()
    success = Task.update(task_id, data)
    
    if not success:
        raise NotFoundError('Task not found')
    
    return jsonify({'status': 'updated'})

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    """Delete a task"""
    success = Task.delete(task_id)
    
    if not success:
        raise NotFoundError('Task not found')
    
    return jsonify({'status': 'deleted'})