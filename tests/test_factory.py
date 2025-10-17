# tests/test_factory.py

import pytest
import os
from config import TestingConfig 
from parameter_service import create_app


# Setup/Teardown for environment variable handling
@pytest.fixture() 
def setup_env_vars():
    """Ensure the base environment variables are set for testing."""
    # Set the required variables before tests run
    os.environ['DATABASE_URL'] = 'mysql+pymysql://test:test@localhost:3306/test_db'
    os.environ['TEST_DATABASE_URL'] = 'sqlite:///:memory:' 
    yield
    # Safely clean up environment variables after tests complete
    os.environ.pop('DATABASE_URL', None)
    os.environ.pop('TEST_DATABASE_URL', None)
    

def test_config_default_development(setup_env_vars): 
    """Test that the default config loads the Development environment."""
    app = create_app()
    assert app.config['DEBUG'] is True
    assert app.testing is False
    assert 'default-dev-secret-key' in app.config['SECRET_KEY']


def test_config_testing_environment():
    """Test that the 'testing' config loads the correct settings."""
    app = create_app('testing')
    assert app.testing is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    assert app.config['DEBUG'] is False


def test_config_production_environment(setup_env_vars): 
    """Test that the 'production' config loads the correct settings."""
    app = create_app('production')
    assert app.config['DEBUG'] is False
    assert app.testing is False
    assert 'mysql+pymysql' in app.config['SQLALCHEMY_DATABASE_URI']


def test_database_url_is_required_in_base_config(setup_env_vars):
    """Test that a RuntimeError is raised if the required DATABASE_URL is missing 
       for non-testing environments."""
    
    # Manually remove the env variable before creating the app
    os.environ.pop('DATABASE_URL', None) 

    # We expect a RuntimeError when SQLAlchemy attempts to initialize with a None URI.
    with pytest.raises(RuntimeError) as excinfo:
        create_app('default')
        
    assert "SQLALCHEMY_DATABASE_URI" in str(excinfo.value) or "must be set" in str(excinfo.value)
    
    # Ensure testing config still works without the external DATABASE_URL
    app = create_app('testing')
    assert app.testing is True