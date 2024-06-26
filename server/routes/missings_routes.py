import os
from flask import Blueprint, request, jsonify
from database.crud_operations import list_missing_persons, update_missing_person, create_missing_person, get_missing_person_by_id
from uitlities import auth, encodeIMGs, delete_image

missing_routes = Blueprint('missing_routes', __name__)

@missing_routes.route('/missing/', methods=['GET'])
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
  data = list_missing_persons(search=search, page=page)
  return jsonify({
    'persons': [missing.to_dict() for missing in data['persons']], 
    'count': data['count']
    })

@missing_routes.route('/missing/solved', methods=['POST'])
def solved():
  data = request.get_json(force=True)
  token = data['token']
  if (not auth(token)):
    return jsonify({'token': 0}), 400
  try:
    id = data['person_id']
    person = get_missing_person_by_id(id)
    delete_image('server/'+person.image_path)
    update_missing_person(person_id=id, solved=True, image_path='')
    encodeIMGs()
    return jsonify({"message": "Operação sucedeu."})
  except:
    return jsonify({"message": "Operação falhou."}), 400

IMAGE_UPLOADS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static/images")

if not os.path.exists(IMAGE_UPLOADS):
    os.makedirs(IMAGE_UPLOADS)
@missing_routes.route('/missing/', methods=['POST'])
def register():
  try:
      # Dados do formulário
      name = request.form['name']
      birthday = request.form['birthday']
      bi = request.form['bi']
      family_contact = request.form['family_contact']
      date = request.form['date']

      # Arquivo de imagem
      image = request.files['image']

      # Variável para armazenar o caminho da imagem
      image_path = None

      if image:
          # Caminho para salvar a imagem
          image_path = os.path.join(IMAGE_UPLOADS, f"{bi}.jpg")
          image.save(image_path)

      relative_image_path =  f'/static/images/' + f"{bi}.jpg"
      create_missing_person(name, birthday, bi, family_contact, date, relative_image_path)
      encodeIMGs()

      # Resposta de sucesso incluindo o caminho da imagem
      response = {
          "message": "Registro realizado com sucesso!",
          "data": {
              "name": name,
              "birthday": birthday,
              "bi": bi,
              "family_contact": family_contact,
              "date": date,
              "image_path": relative_image_path
          }
      }
      return jsonify(response), 200
  except Exception as e:
      # Resposta de erro
      return jsonify({"error": str(e)}), 400