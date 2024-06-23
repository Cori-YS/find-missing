from flask import Blueprint, request, jsonify
from database.crud_operations import create_user, get_user_by_username, list_users
from uitlities import encode, decode
import jwt

user_routes = Blueprint('user_routes', __name__)
jwt_secret = "AFDASG#@#%$33"
jwt_algorithm = "HS256"

@user_routes.route('/user/register', methods=['POST'])
def register():
  data = request.get_json(force=True)
  username = data['username']
  email = data['email']
  password = data['password']
  try:
    create_user(email, encode(password), username)
    return jsonify({'message': 'Cadastro efetuado como sucesso.'})
  except:
    return jsonify({'token': '0'}), 400

@user_routes.route('/user/login', methods=['POST'])
def login():
  data = request.get_json(force=True)
  username = data['username']
  password = data['password']
  try:
    user = get_user_by_username(username)
    token = '0'
    if password == decode(user.password):
      token = jwt.encode({"user_id": user.id}, jwt_secret, algorithm=jwt_algorithm)
    return jsonify({'token': token})
  except:
    return jsonify({'token': '0'}), 400