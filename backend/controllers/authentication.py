from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import auth_token_required, utils
from controllers.database import db

from controllers.userdatastore import user_datastore

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = user_datastore.find_user(email=email)

        if not data:

            return make_response(jsonify({'message': 'Login Credentials are required'}), 400)
        
        if not email:

            return make_response(jsonify({'message': 'Email is required'}), 400)
        
        if not password:

            return make_response(jsonify({'message': 'Password is required'}), 400)
        
        if not user:

            return make_response(jsonify({'message': 'User not found'}), 404)

        if not utils.verify_password(password, user.password):

            return make_response(jsonify({'message': 'Invalid password'}), 401)
        
        auth_token = user.get_auth_token()

        utils.login_user(user)

        response = {
            'message': 'Login successful',
            'user': {
                'email': user.email,
                'roles': [role.name for role in user.roles],
                'auth_token': auth_token
            }
        }

        return make_response(jsonify(response), 200)
    
class Logout(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        return make_response(jsonify({'message': 'Logout successful'}), 200)
    
class Register(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not data:
            return make_response(jsonify({'message': 'Registration data is required'}), 400)
        
        if not name:
            return make_response(jsonify({'message': 'Name is required'}), 400)
        
        if not email:
            return make_response(jsonify({'message': 'Email is required'}), 400)
        
        if '@' not in email:
            return make_response(jsonify({'message': 'Invalid email format'}), 400)
        
        if not password:
            return make_response(jsonify({'message': 'Password is required'}), 400)
        
        if user_datastore.find_user(email=email):
            return make_response(jsonify({'message': 'User already exists'}), 409)
        
        user_role = user_datastore.find_or_create_role(name='user', description='User role')
        user_datastore.create_user(email=email, password=password, roles=[user_role], name=name)

        db.session.commit()

        response = {
            'message': 'Registration successful',
            'user': {
                'email': email,
                'name': name,
                'roles': [user_role.name]
            }
        }

        return make_response(jsonify(response), 201)