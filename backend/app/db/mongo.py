from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from flask import Flask
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    """MongoDB connection wrapper"""
    
    def __init__(self):
        self.client = None
        self.db = None
    
    def init_app(self, app: Flask):
        """Initialize MongoDB connection with Flask app"""
        try:
            self.client = MongoClient(
                app.config['MONGO_URI'],
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            # Verify connection
            self.client.admin.command('ping')
            self.db = self.client.get_database()
            logger.info('MongoDB connection successful')
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            logger.error(f'Failed to connect to MongoDB: {e}')
            raise
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info('MongoDB connection closed')
    
    def get_db(self):
        """Get database instance"""
        return self.db
    
    def get_collection(self, collection_name: str):
        """Get a specific collection"""
        return self.db[collection_name] if self.db else None

# Global MongoDB instance
mongo = MongoDB()