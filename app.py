from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from user_service.routes import users_bp   # Import users blueprint
from auth_service.auth import auth_bp      # Import auth blueprint
from destination_service.routes import destination_bp  # Import destination blueprint

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

# Initialize Swagger and JWT manager
swagger = Swagger(app)
jwt = JWTManager(app)

# Register the blueprints
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(destination_bp, url_prefix='/destinations')  # Register destination blueprint

if __name__ == '__main__':
    app.run(port=5000)  # Single port for all services
