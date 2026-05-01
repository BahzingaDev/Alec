from datetime import datetime
from bson import ObjectId
from app.db.mongo import mongo

class Reminder:
    """Reminder model for MongoDB"""
    
    COLLECTION = 'reminders'
    
    @staticmethod
    def create(user_id, reminder_data):
        """Create a new reminder"""
        reminder_doc = {
            'user_id': ObjectId(user_id),
            'title': reminder_data.get('title'),
            'description': reminder_data.get('description'),
            'reminder_time': reminder_data.get('reminder_time'),
            'frequency': reminder_data.get('frequency', 'once'),  # once, daily, weekly, monthly
            'is_active': reminder_data.get('is_active', True),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        
        collection = mongo.get_collection(Reminder.COLLECTION)
        result = collection.insert_one(reminder_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_user(user_id):
        """Find all reminders for a user"""
        collection = mongo.get_collection(Reminder.COLLECTION)
        return list(collection.find({'user_id': ObjectId(user_id)}))
    
    @staticmethod
    def find_by_id(reminder_id):
        """Find reminder by ID"""
        collection = mongo.get_collection(Reminder.COLLECTION)
        return collection.find_one({'_id': ObjectId(reminder_id)})
    
    @staticmethod
    def update(reminder_id, update_data):
        """Update reminder"""
        collection = mongo.get_collection(Reminder.COLLECTION)
        update_data['updated_at'] = datetime.utcnow()
        result = collection.update_one(
            {'_id': ObjectId(reminder_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(reminder_id):
        """Delete reminder"""
        collection = mongo.get_collection(Reminder.COLLECTION)
        result = collection.delete_one({'_id': ObjectId(reminder_id)})
        return result.deleted_count > 0