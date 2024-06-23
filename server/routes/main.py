import os
from flask import Blueprint, send_from_directory
from routes.user_routes import user_routes
from routes.found_routes import found_routes
from routes.missings_routes import missing_routes, IMAGE_UPLOADS

routes = Blueprint('routes', __name__)

@routes.route('/static/images/<path:filename>', methods=['GET'])
def serve_image(filename):
  return send_from_directory(IMAGE_UPLOADS, filename)

@routes.route('/static/encodes', methods=['GET'])
def serve_encodings():
  ENCODE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static/encodes")
  print(ENCODE_PATH)
  return send_from_directory(ENCODE_PATH, 'EncodeFile.p')

routes.register_blueprint(user_routes)
routes.register_blueprint(found_routes)
routes.register_blueprint(missing_routes)