from datetime import datetime
from bson import ObjectId
from app.db.mongo import mongo

class Task:
    """Task model for MongoDB"""
    
    COLLECTION = 'tasks'
    
    @staticmethod
    def create(user_id, task_data):
        """Create a new task"""
        task_doc = {
            'user_id': ObjectId(user_id),
            'title': task_data.get('title'),
            'description': task_data.get('description'),
            'status': task_data.get('status', 'pending'),
            'due_date': task_data.get('due_date'),
            'priority': task_data.get('priority', 'normal'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        
        collection = mongo.get_collection(Task.COLLECTION)
        result = collection.insert_one(task_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_user(user_id):
        """Find all tasks for a user"""
        collection = mongo.get_collection(Task.COLLECTION)
        return list(collection.find({'user_id': ObjectId(user_id)}))
    
    @staticmethod
    def find_by_id(task_id):
        """Find task by ID"""
        collection = mongo.get_collection(Task.COLLECTION)
        return collection.find_one({'_id': ObjectId(task_id)})
    
    @staticmethod
    def update(task_id, update_data):
        """Update task"""
        collection = mongo.get_collection(Task.COLLECTION)
        update_data['updated_at'] = datetime.utcnow()
        result = collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(task_id):
        """Delete task"""
        collection = mongo.get_collection(Task.COLLECTION)
        result = collection.delete_one({'_id': ObjectId(task_id)})
        return result.deleted_count > 0