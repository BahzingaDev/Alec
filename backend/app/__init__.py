from flask import Flask
from flask_cors import CORS
from app.core.config import get_config
from app.db.mongo import mongo
from app.core.errors import register_error_handlers

def create_app(env=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(env)
    app.config.from_object(config)
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    # Setup CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', ['http://localhost:5173'])
        }
    })
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    from app.routes.health import health_bp
    from app.routes.tasks import tasks_bp
    from app.routes.reminders import reminders_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(reminders_bp)
    
    # Close MongoDB connection on app teardown
    @app.teardown_appcontext
    def close_db(error):
        mongo.close()
    
    return app