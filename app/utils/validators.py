from email_validator import validate_email, EmailNotValidError
from bson import ObjectId

def validate_object_id(id_string):
    return ObjectId.is_valid(id_string)

def validate_user_data(data):
    if not data:
        return "No data provided"
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"

    if 'email' in data:
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            return "Invalid email format"
    
    if 'password' in data and len(data['password']) < 8:
        return "Password must be at least 8 characters long"
    if 'name' in data and not data['name'].strip():
        return "Name cannot be empty"
    
    return None