# parameter_service/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name

# Initialize SQLAlchemy outside of the factory, but without binding to the app yet.
db = SQLAlchemy()

def create_app(config_name: str = 'default') -> Flask:
    """
    Flask application factory function.
    """
    app = Flask(__name__)
    
    # 1. Load Configuration
    config_object = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config_object)
    
    # 2. Initialize Extensions
    # Bind the SQLAlchemy object to the running Flask application
    try:
        db.init_app(app)
    except ValueError as e:
        # This will catch the error if DATABASE_URL is not set for a non-testing env.
        app.logger.error(f"Failed to initialize database: {e}")
        raise

    # 3. Register Blueprints (Future Step)
    # Import models here to ensure they are registered with SQLAlchemy when called
    from .models.parameter_model import Parameter 
    
    # Optional: Basic health check route
    @app.route('/health')
    def health_check():
        return {'status': 'ok'}, 200

    return app