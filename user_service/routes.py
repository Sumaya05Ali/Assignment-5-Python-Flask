from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flasgger import swag_from

users_bp = Blueprint('users_bp', __name__)

# In-memory data structure to store users
users = []

@users_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'RegisterUser',
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                    'role': {'type': 'string', 'enum': ['Admin', 'User']}
                }
            }
        }
    ],
    'responses': {
        '201': {'description': 'User registered successfully'},
        '400': {'description': 'Bad request (missing or invalid data)'}
    }
})
def register():
    data = request.json
    if not data or not data.get('name') or not data.get('email') or not data.get('password') or not data.get('role'):
        return jsonify({"message": "Missing required fields"}), 400

    if data['role'] not in ['Admin', 'User']:
        return jsonify({"message": "Invalid role"}), 400

    hashed_password = generate_password_hash(data['password'])
    user = {
        "name": data['name'],
        "email": data['email'],
        "password": hashed_password,
        "role": data['role']
    }
    users.append(user)
    return jsonify({"message": "User registered successfully"}), 201


@users_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'LoginUser',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '200': {'description': 'Successfully logged in'},
        '401': {'description': 'Invalid credentials'}
    }
})
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing required fields"}), 400

    user = next((u for u in users if u['email'] == data['email']), None)
    if user and check_password_hash(user['password'], data['password']):
        # FIX: Use user's email as the identity and pass role in additional claims
        access_token = create_access_token(identity=user['email'], additional_claims={"role": user['role']})
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid credentials"}), 401


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'JWT token in the format: Bearer <token>'
        }
    ],
    'responses': {
        '200': {'description': 'User profile information'},
        '401': {'description': 'Unauthorized'}
    }
})
def profile():
    current_user_email = get_jwt_identity()  # This retrieves the email
    claims = get_jwt()  # This retrieves the additional claims (like role)
    
    user = next((u for u in users if u['email'] == current_user_email), None)
    if user:
        return jsonify({
            "name": user['name'],
            "email": user['email'],
            "role": claims.get('role')  
        }), 200
    return jsonify({"message": "User not found"}), 404
