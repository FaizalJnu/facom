from flask import Blueprint, request, jsonify
from app import user_collection
from app.models.user import UserModel, UserResponseModel, UserUpdateModel
from app.utils.validators import validate_user_data, validate_object_id
from bson import ObjectId

user_bp = Blueprint('user', __name__)

@user_bp.route('', methods=['GET'])
def get_all_users():
    users = []
    for user in user_collection.find():
        if '_id' in user and user['_id'] is not None:
            user['_id'] = str(user['_id'])
        else:
            print(f"user with no id found: {user}")

        # user['_id'] = str(user['_id'])
        user.pop('password', None)
        users.append(user)
    
    return jsonify(users), 200

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    if not validate_object_id(user_id):
        return jsonify({"error": "Invalid user ID format"}), 400
    
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    user['_id'] = str(user['_id'])
    user.pop('password', None)
    
    return jsonify(user), 200

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    
    validation_result = validate_user_data(data)
    if validation_result:
        return jsonify({"error": validation_result}), 400
    
    if user_collection.find_one({"email": data['email']}):
        return jsonify({"error": "User with this email already exists, no two email ids can ever be the same"}), 400
    
    try:
        if '_id' in data:
            del data['_id']
        
        user = UserModel(**data)
        user_dict = user.dict(by_alias=True)

        if '_id' in user_dict and user_dict['_id'] is None:
            del user_dict['_id']

        result = user_collection.insert_one(user_dict)
        
        created_user = user_collection.find_one({"_id": result.inserted_id})
        
        if created_user and '_id' in created_user:
            created_user['_id'] = str(created_user['_id'])

        created_user.pop('password', None)
        
        return jsonify(created_user), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):

    if not validate_object_id(user_id):
        return jsonify({"error": "Invalid user ID format"}), 400
    
    data = request.get_json()
    if not user_collection.find_one({"_id": ObjectId(user_id)}):
        return jsonify({"error": "User not found"}), 404
    
    if 'email' in data:
        existing_user = user_collection.find_one({"email": data['email']})
        if existing_user and str(existing_user['_id']) != user_id:
            return jsonify({"error": "Email already in use by another user"}), 400
    
    try:
        update_data = UserUpdateModel(**data)
        update_dict = {}
    
        for field, value in update_data.dict(exclude_unset=True).items():
            if value is not None:
                update_dict[field] = value
        
        user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )
        updated_user = user_collection.find_one({"_id": ObjectId(user_id)})
        updated_user['_id'] = str(updated_user['_id'])
        updated_user.pop('password', None)
        
        return jsonify(updated_user), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@user_bp.route('/email/<email>', methods=['DELETE'])
def delete_user_by_email(email):
    """Delete a user by email."""
    user = user_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_collection.delete_one({"email": email})
    return jsonify({"message": "User successfully deleted"}), 200

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    if not validate_object_id(user_id):
        return jsonify({"error": "Invalid user ID format"}), 400
    
    if not user_collection.find_one({"_id": ObjectId(user_id)}):
        return jsonify({"error": "User not found"}), 404
    
    user_collection.delete_one({"_id": ObjectId(user_id)})
    
    return jsonify({"message": "User successfully deleted"}), 200