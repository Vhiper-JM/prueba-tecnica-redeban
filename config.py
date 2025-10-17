# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    
    # ------------------
    # Core Application Settings
    # ------------------
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key')
    LOG_LEVEL = 'INFO'
    TESTING = False
    
    # ------------------
    # Database Settings (MySQL)
    # ------------------
    # The format will be: mysql+pymysql://<user>:<password>@<host>:<port>/<db_name>
    # Note: We rely on the Application Factory to validate this is set 
    # for non-testing environments.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True


class TestingConfig(Config):
    """Configuration for testing environment."""
    TESTING = True
    # Use an in-memory SQLite database URI for speed and isolation in unit tests.
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///:memory:')


class ProductionConfig(Config):
    """Configuration for production environment."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'


# Dictionary to easily get the correct configuration class
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}