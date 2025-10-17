import pytest
# ADDED IMPORT: Fixes NameError for JSON/Array tests
import json 
from parameter_service import create_app, db
# 🚨 FIX APPLIED: Changed 'parameter' to 'parameter_model' to match the file name
from parameter_service.models.parameter_model import Parameter, ParameterType 


# --- FIXTURES (db_session is already correct from previous step) ---

@pytest.fixture(scope='module')
def test_app():
    # ... (setup code)
    app = create_app('testing')
    with app.app_context():
        # Create all tables for the models
        db.create_all()
        yield app
        # Drop all tables after tests are done
        db.drop_all()

@pytest.fixture(scope='function')
def db_session(test_app):
    """Provide a clean session with transaction rollback for each test function."""
    with test_app.app_context():
        db.session.begin_nested() 
        yield db.session 
        db.session.rollback()
        db.session.remove() 

# --- TESTS ---

@pytest.mark.parametrize("input_value, expected_type, expected_deserialized_value", [
    # String types
    ("Hello World", ParameterType.STRING, "Hello World"),
    ("", ParameterType.STRING, ""),
    # Number types (Integer)
    (12345, ParameterType.NUMBER, 12345),
    (-100, ParameterType.NUMBER, -100),
    # Number types (Float)
    (3.14159, ParameterType.NUMBER, 3.14159),
    (0.0, ParameterType.NUMBER, 0.0),
    # Boolean types
    (True, ParameterType.BOOLEAN, True), # <-- Fix applied in parameter_model.py setter
    (False, ParameterType.BOOLEAN, False), # <-- Fix applied in parameter_model.py setter
    # JSON type (Dict)
    ({'key': 'value', 'count': 1}, ParameterType.JSON, {'key': 'value', 'count': 1}),
    # Array type (List)
    ([1, 2, "a"], ParameterType.ARRAY, [1, 2, "a"]),
    # Null value
    (None, ParameterType.STRING, None),
])
def test_value_setter_and_getter_polymorphism(db_session, input_value, expected_type, expected_deserialized_value):
    """Test serialization and deserialization across all supported parameter types."""
    param = Parameter(name='test_param', value=input_value)
    
    # Test setter logic
    assert param.value_type == expected_type
    
    if expected_type in [ParameterType.JSON, ParameterType.ARRAY]:
        # JSON/Array should be stored as a JSON string
        assert isinstance(param.value_storage, str)
        # Ensure it's valid JSON that was stored (fixed by adding import json)
        assert expected_deserialized_value == json.loads(param.value_storage)
    elif expected_type == ParameterType.BOOLEAN:
        # Booleans should be stored as 'true' or 'false' lowercase strings
        assert param.value_storage == str(input_value).lower()
    else:
        # Other types should be stored as their string representation
        # FIX: Ensure we assert against the input_value's string representation, 
        # or None if input_value is None.
        assert param.value_storage == str(input_value) if input_value is not None else None
        
    # Commit and retrieve from database (simulate real workflow)
    db_session.add(param)
    db_session.commit()
    retrieved_param = db_session.get(Parameter, param.id)
    
    # Test getter logic (deserialization)
    assert retrieved_param.value == expected_deserialized_value
    assert retrieved_param.value_type == expected_type


def test_updated_at_timestamp(db_session):
    """Test that the updated_at field is correctly modified on update."""
    param = Parameter(name='version', value=1.0)
    db_session.add(param)
    db_session.commit()

    initial_updated_at = param.updated_at
    
    # Simulate a small time delay for updated_at to be different
    # In a real application, the database takes care of the timestamp difference.
    # In SQLite/in-memory, we rely on SQLAlchemy's update logic.
    
    param.value = 2.0  # Trigger the update
    db_session.add(param)
    db_session.commit()
    
    retrieved_param = db_session.get(Parameter, param.id)

    # The updated_at time should be later than the created_at time (which is the initial updated_at)
    # The actual difference might be milliseconds, but it should be non-equal.
    assert retrieved_param.updated_at > initial_updated_at
    assert retrieved_param.value == 2.0


def test_to_dict_method(db_session):
    """Test the object serialization method (to_dict)."""
    param = Parameter(name='settings', value={'theme': 'dark'})
    db_session.add(param)
    db_session.commit()
    
    param_dict = param.to_dict()
    
    assert isinstance(param_dict, dict)
    assert param_dict['name'] == 'settings'
    assert param_dict['value_type'] == ParameterType.JSON
    assert param_dict['value'] == {'theme': 'dark'}
    assert 'id' in param_dict
    assert 'created_at' in param_dict
    assert 'updated_at' in param_dict