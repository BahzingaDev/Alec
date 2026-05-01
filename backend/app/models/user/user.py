from datetime import datetime
from bson import ObjectId
from app.db.mongo import mongo

class User:
    """User model for MongoDB"""
    
    COLLECTION = 'users'
    
    @staticmethod
    def create(user_data):
        """Create a new user"""
        user_doc = {
            'name': user_data.get('name'),
            'email': user_data.get('email'),
            'password_hash': user_data.get('password_hash'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        
        collection = mongo.get_collection(User.COLLECTION)
        result = collection.insert_one(user_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        collection = mongo.get_collection(User.COLLECTION)
        return collection.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        collection = mongo.get_collection(User.COLLECTION)
        return collection.find_one({'email': email})
    
    @staticmethod
    def update(user_id, update_data):
        """Update user"""
        collection = mongo.get_collection(User.COLLECTION)
        update_data['updated_at'] = datetime.utcnow()
        result = collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(user_id):
        """Delete user"""
        collection = mongo.get_collection(User.COLLECTION)
        result = collection.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count > 0