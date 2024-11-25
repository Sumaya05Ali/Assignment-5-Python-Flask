# Assignment-5-Python-Flask

# Travel API with Microservices

This project is a basic Travel API developed using Flask and microservices architecture. The API is split into three microservices:

- Destination Service: Manages travel destinations.
- User Service: Handles user registration, login, and profile management.
- Authentication Service: Manages JWT authentication and enforces role-based access control.

The API follows OpenAPI/Swagger standards for documentation.

## Features

1. Destination Service

  - Retrieve all travel destinations
  - Delete destinations (Admin only)
  - User Service

2. User registration
  
  - User login (returns a JWT token)
  - View user profile (requires authentication)
  - Authentication Service

3. Role-based access control

 - Admin-only access for certain endpoints

## Requirements

- Python 3.x
- Flask
- Flask-JWT-Extended
- Flasgger (for Swagger API documentation)
- Other dependencies (listed in requirements.txt)   

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sumaya05Ali/Assignment-5-Python-Flask.git
   cd Assignment-5-Python-Flask-main
   ```
2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```  
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the API:
   ```bash
   python app.py
   ```
The API will be available at http://127.0.0.1:5000.

## API Documentation
The API documentation is available via Swagger at http://127.0.0.1:5000/apidocs.

Usage Examples

1. User Registration
  - Endpoint: /users/register
  - Method: POST
  - Request Body:
    ```bash
    {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "User"
    }
    ```
Response:
 ```bash
 {
  "message": "User registered successfully"
 }
 ```
2. User Login
  - Endpoint: /users/login
  - Method: POST
  - Request Body:
    ```bash
     {
       "email": "john@example.com",
       "password": "password123"
    }
    ```
   
Response:
 ```bash
 {
  "access_token": "<JWT_TOKEN>"
}
 ```



    
