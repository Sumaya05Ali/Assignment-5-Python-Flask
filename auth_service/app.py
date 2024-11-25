import sys
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger

# Add parent directory to system path for imports to work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth import auth_bp  # Import the authentication blueprint

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

# Initialize Swagger and JWT manager
swagger = Swagger(app)
jwt = JWTManager(app)

# Register the authentication blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(port=5002)
