# schemas/__init__.py
import json
import os

def load_schema(filename):
    """
    Load a JSON schema from the schemas directory.
    
    Args:
        filename (str): Name of the schema file
        
    Returns:
        dict: The loaded schema
    """
    schema_path = os.path.join(os.path.dirname(__file__), filename)
    with open(schema_path, 'r') as f:
        return json.load(f)

# Example schema for a user object
USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "phone": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"}
    },
    "additionalProperties": False
}

# Example schema for a list of users
USERS_LIST_SCHEMA = {
    "type": "array",
    "items": {"$ref": "#/definitions/user"},
    "definitions": {
        "user": USER_SCHEMA
    }
}

# Example schema for an error response
ERROR_SCHEMA = {
    "type": "object",
    "required": ["error", "message"],
    "properties": {
        "error": {"type": "string"},
        "message": {"type": "string"},
        "status_code": {"type": "integer"}
    }
}