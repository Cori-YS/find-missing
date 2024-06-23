from flask import Blueprint, request, jsonify
from database.crud_operations import list_founds, create_found, get_missing_person_by_bi
from uitlities import auth

found_routes = Blueprint('found_routes', __name__)

@found_routes.route('/found/', methods=['GET'])
def list():
  data = request.get_json(force=True)
  token = data['token']
  if (not auth(token)):
    return jsonify({'token': 0}), 400
  page = data['page']
  try:
    search = data['search']
  except:
    search = None
  data = list_founds(search=search, page=page)
  return jsonify({
    'founds': [found.to_dict() for found in data['founds']], 
    'count': data['count']
    })

@found_routes.route('/found/', methods=['POST'])
def register():
  try:
      # Dados do json
      data = request.get_json(force=True)
      person_bi = data['person_bi']
      location = data['location']
      camera = data['camera']

      missing_person = get_missing_person_by_bi(person_bi)
      create_found(missing_person, location, camera)

      response = {
          "message": "Registro realizado com sucesso!",
      }
      return jsonify(response), 200
  except Exception as e:
      # Resposta de erro
      return jsonify({"error": str(e)}), 400