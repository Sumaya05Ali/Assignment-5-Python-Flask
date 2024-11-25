import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify
from app import create_app  
from flask_jwt_extended import create_access_token

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app() 
        self.app = app.test_client()
        self.app_context = app.app_context() 
        self.app_context.push() 


        self.admin_token = create_access_token(identity={"email": "admin@test.com", "role": "admin"})
        
    def tearDown(self):
        self.app_context.pop()  


    # Test user registration
    def test_user_registration(self):
        response = self.app.post('/users/register', json={
            'name': 'Test User',
            'email': 'test@test.com',
            'password': 'testpass',
            'role': 'User'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

    # Test registration with missing fields
    def test_user_registration_missing_fields(self):
        response = self.app.post('/users/register', json={
            'name': '',
            'email': '',
            'password': 'testpass',
            'role': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid input data', response.data)

    # Test login with valid credentials
    def test_login(self):
        # Register user first
        self.app.post('/users/register', json={
            'name': 'Login Test User',
            'email': 'login@test.com',
            'password': 'testpass',
            'role': 'User'
        })
        response = self.app.post('/users/login', json={
            'email': 'login@test.com',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'access_token', response.data)

    # Test login with invalid credentials
    def test_login_invalid(self):
        response = self.app.post('/users/login', json={
            'email': 'fake@test.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials', response.data)

    # Test profile access with a valid token
    def test_profile_access(self):
        response = self.app.get('/users/profile', headers={
            'Authorization': f'Bearer {self.user_token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user@test.com', response.data)

    # Test profile access without a token (should fail)
    def test_profile_access_without_token(self):
        response = self.app.get('/users/profile')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Unauthorized', response.data)

    # Test profile access with an invalid token
    def test_profile_access_with_invalid_token(self):
        response = self.app.get('/users/profile', headers={
            'Authorization': 'Bearer invalid_token'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Token is invalid', response.data)

    # Test destination GET for all users
    def test_get_destinations(self):
        response = self.app.get('/destinations/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Paris', response.data)

    # Test destination POST (only Admin should succeed)
    def test_add_destination_as_admin(self):
        response = self.app.post('/destinations/', json={
            'name': 'Berlin',
            'description': 'Capital of Germany',
            'location': 'Germany'
        }, headers={
            'Authorization': f'Bearer {self.admin_token}'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Destination added successfully', response.data)

    # Test destination POST (non-admin should fail)
    def test_add_destination_as_user(self):
        response = self.app.post('/destinations/', json={
            'name': 'Berlin',
            'description': 'Capital of Germany',
            'location': 'Germany'
        }, headers={
            'Authorization': f'Bearer {self.user_token}'
        })
        self.assertEqual(response.status_code, 403)
        self.assertIn(b'Admin access required', response.data)

    # Test add destination with invalid data
    def test_add_destination_with_invalid_data(self):
        response = self.app.post('/destinations/', json={
            'name': '',
            'description': 'No name provided',
            'location': ''
        }, headers={
            'Authorization': f'Bearer {self.admin_token}'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid destination data', response.data)

    # Test delete destination as Admin
    def test_delete_destination_as_admin(self):
        # Add destination first
        self.app.post('/destinations/', json={
            'name': 'Berlin',
            'description': 'Capital of Germany',
            'location': 'Germany'
        }, headers={
            'Authorization': f'Bearer {self.admin_token}'
        })
        response = self.app.delete('/destinations/1', headers={
            'Authorization': f'Bearer {self.admin_token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Destination deleted successfully', response.data)

    # Test delete destination as non-admin (should fail)
    def test_delete_destination_as_user(self):
        response = self.app.delete('/destinations/1', headers={
            'Authorization': f'Bearer {self.user_token}'
        })
        self.assertEqual(response.status_code, 403)
        self.assertIn(b'Admin access required', response.data)

    # Test registration with existing email
    def test_registration_with_existing_email(self):
        # Register first user
        self.app.post('/users/register', json={
            'name': 'Existing User',
            'email': 'exist@test.com',
            'password': 'testpass',
            'role': 'User'
        })
        # Try to register with the same email again
        response = self.app.post('/users/register', json={
            'name': 'Another User',
            'email': 'exist@test.com',
            'password': 'newpass',
            'role': 'User'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Email already exists', response.data)

    # Test token verification
    def test_verify_token(self):
        response = self.app.get('/auth/verify-token', headers={
            'Authorization': f'Bearer {self.admin_token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'admin', response.data)


if __name__ == '__main__':
    unittest.main()
