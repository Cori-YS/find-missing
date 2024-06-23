import cv2
import numpy as np
import requests

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def get_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    image = np.array(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    #image = cv2.resize(image, (414, 633))
    image = image_resize(image, 414, 633)
    return image

def send_recognition_to_server(person_bi, location, camera):
    api_url = 'http://localhost:5000/found/'
    data = {
        'person_bi': person_bi,
        'location': location,
        'camera': camera,
    }
    # Enviar solicitação POST para a API
    requests.post(api_url, json=data)