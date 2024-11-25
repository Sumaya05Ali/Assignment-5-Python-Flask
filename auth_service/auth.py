# auth_service/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import check_password_hash
from user_service.routes import users

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing required fields"}), 400
    
    user = next((u for u in users if u['email'] == data['email']), None)
    
    if user and check_password_hash(user['password'], data['password']):
        # Create token with user information in the identity
        access_token = create_access_token(
            identity={
                "email": user['email'],
                "role": user.get('role', '').lower(),
                "user_id": user.get('id')
            }
        )
        
        return jsonify({
            "access_token": access_token,
            "role": user.get('role', '').lower(),
            "email": user['email'],
            "user_id": user.get('id')
        }), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    claims = get_jwt()
    return jsonify({
        "role": claims.get('role'),
        "email": claims.get('email'),
        "is_valid": True
    }), 200