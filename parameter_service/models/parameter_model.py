# parameter_service/models/parameter_model.py

import json
from datetime import datetime
from typing import Any, Union, Dict, List
from flask_sqlalchemy import SQLAlchemy

from parameter_service import db # Assumes db is initialized in __init__.py


class ParameterType:
    """Defines the allowed, canonical types for parameter values."""
    STRING = 'String'
    NUMBER = 'Number'
    BOOLEAN = 'Boolean'
    JSON = 'JSON'
    ARRAY = 'Array'
    
    ALLOWED_TYPES = [STRING, NUMBER, BOOLEAN, JSON, ARRAY]


class Parameter(db.Model):
    """
    Represents a configuration parameter in the database.
    """
    __tablename__ = 'parameters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False, index=True)
    value_type = db.Column(db.String(50), nullable=False) # Stores 'String', 'Number', etc.
    value_storage = db.Column(db.Text, nullable=True)  # Stores serialized value
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Parameter(id={self.id}, name='{self.name}', type='{self.value_type}')>"

    @property
    def value(self) -> Any:
        """Deserializes the stored string value_storage back into its native Python type."""
        if self.value_storage is None:
            return None
            
        if self.value_type == ParameterType.STRING:
            return self.value_storage
        elif self.value_type == ParameterType.NUMBER:
            try:
                # Prioritize int if no decimal point, otherwise use float
                return float(self.value_storage) if '.' in self.value_storage else int(self.value_storage)
            except ValueError:
                return self.value_storage
        elif self.value_type == ParameterType.BOOLEAN:
            # Standardize string representations to Python boolean
            return self.value_storage.lower() == 'true'
        elif self.value_type in [ParameterType.JSON, ParameterType.ARRAY]:
            try:
                # JSON/Array are stored as JSON strings
                return json.loads(self.value_storage)
            except json.JSONDecodeError:
                return self.value_storage  # Return raw string on decoding failure
        else:
            return self.value_storage

    @value.setter
    def value(self, raw_value: Any):
        """
        Serializes the Python value into a string for storage (value_storage) 
        and sets the value_type.
        """
        if raw_value is None:
            self.value_type = ParameterType.STRING
            self.value_storage = None
            return

        # 🚨 FIX: Check for 'bool' first (bool is a subclass of int in Python)
        if isinstance(raw_value, bool):  
            self.value_type = ParameterType.BOOLEAN
            self.value_storage = str(raw_value).lower()
            
        elif isinstance(raw_value, (int, float)):
            self.value_type = ParameterType.NUMBER
            self.value_storage = str(raw_value)
            
        elif isinstance(raw_value, str):
            self.value_type = ParameterType.STRING
            self.value_storage = raw_value
            
        elif isinstance(raw_value, (dict, list)):
            self.value_type = ParameterType.ARRAY if isinstance(raw_value, list) else ParameterType.JSON
            # Serialize the complex object into a JSON string for storage
            self.value_storage = json.dumps(raw_value)
        else:
            # Fallback for unexpected types
            self.value_type = ParameterType.STRING
            self.value_storage = str(raw_value)
            
    def to_dict(self) -> Dict[str, Any]:
        """Converts the Parameter object into a serializable dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'value_type': self.value_type,
            'value': self.value, # Uses the @property for deserialized value
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }