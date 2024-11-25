from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

destination_bp = Blueprint('destination_bp', __name__)

# Sample data - In-memory storage
destinations = [
    {"id": 1, "name": "Paris", "description": "City of Lights", "location": "France"},
    {"id": 2, "name": "Tokyo", "description": "Capital of Japan", "location": "Japan"}
]

@destination_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Destinations'],
    'responses': {
        200: {
            'description': 'A list of destinations',
            'examples': {
                'application/json': destinations
            }
        }
    }
})
def get_destinations():
    return jsonify(destinations), 200

@destination_bp.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Destinations'],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'JWT token in the format: Bearer <token>'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Destination',
                'required': ['name', 'description', 'location'],
                'properties': {
                    'name': {'type': 'string', 'example': 'Paris'},
                    'description': {'type': 'string', 'example': 'City of Lights'},
                    'location': {'type': 'string', 'example': 'France'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Destination added successfully'},
        403: {'description': 'Admin access required'},
        400: {'description': 'Missing required fields'}
    }
})
def add_destination():
    try:
        # Get user identity from JWT token
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if not current_user or current_user.get('role') != 'admin':
            return jsonify({"message": "Admin access required"}), 403

        data = request.get_json()
        if not data or not all(key in data for key in ['name', 'description', 'location']):
            return jsonify({"message": "Missing required fields"}), 400

        new_destination = {
            "id": max([d["id"] for d in destinations], default=0) + 1,
            "name": data['name'],
            "description": data['description'],
            "location": data['location']
        }
        destinations.append(new_destination)

        return jsonify({
            "message": "Destination added successfully",
            "destination": new_destination
        }), 201

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@destination_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Destinations'],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'JWT token in the format: Bearer <token>'
        },
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Destination ID to delete'
        }
    ],
    'responses': {
        200: {'description': 'Destination deleted successfully'},
        403: {'description': 'Admin access required'},
        404: {'description': 'Destination not found'}
    }
})
def delete_destination(id):
    try:
        # Get user identity from JWT token
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if not current_user or current_user.get('role') != 'admin':
            return jsonify({"message": "Admin access required"}), 403

        destination = next((d for d in destinations if d["id"] == id), None)
        if not destination:
            return jsonify({"message": "Destination not found"}), 404

        destinations.remove(destination)
        return jsonify({"message": "Destination deleted successfully"}), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
