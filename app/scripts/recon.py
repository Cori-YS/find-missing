import sys
import time
import logging
import io
import os
import cv2
import pickle
import face_recognition
import numpy as np
import requests
from recon_utils import get_image_from_url, send_recognition_to_server

# Configure logging
logging.basicConfig(filename='app/logs/script.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def main(camera, show=None):
    logging.info(f"Iniciando script com argumentos: {camera}, {show}")
    logging.info(f"Script rodando para {camera}, {show}...")
    try:
        cap = cv2.VideoCapture(camera)
        cap.set(3, 640)
        cap.set(4, 480)

        imgBackground = cv2.imread('app/resources/background.png')

        # URL of the pickle file
        url = 'http://127.0.0.1:5000/static/encodes'

        # Download the pickle file from URL
        response = requests.get(url)

        if response.status_code == 200:
            # Load pickle file from the response content
            encondeListKnownWithIds = pickle.load(io.BytesIO(response.content))
            encodeListKnown, personIds = encondeListKnownWithIds
            logging.info("Encode File Loaded")
        else:
            logging.info(f"Failed to fetch the encodes file from URL. Status code: {response.status_code}")
        logging.info("Encode File Loaded")

        # Dictionary to keep track of the last seen time for each face
        last_seen = {}

        # Time interval in seconds (5 minutes = 300 seconds)
        time_interval = 300

        while True:
            success, img = cap.read()

            imgS = cv2.resize(img, (0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
              matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
              faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
              matchIndex = np.argmin(faceDistance)

              if matches[matchIndex]:
                logging.info("Know Face Detected")
                logging.info(personIds[matchIndex])

                # Draw rectangle around the face
                top, right, bottom, left = faceLoc
                top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4  # Scale back to original size
                cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(img, personIds[matchIndex], (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                
                imgUrl = f'http://127.0.0.1:5000/static/images/{personIds[matchIndex]}.jpg'
                image = get_image_from_url(imgUrl)
                height, width, channel = image.shape
                imgBackground[159:159+height, 808:808+width] = get_image_from_url(imgUrl)

                current_time = time.time()
                if personIds[matchIndex] in last_seen:
                    elapsed_time = current_time - last_seen[personIds[matchIndex]]
                    if elapsed_time > time_interval:
                        send_recognition_to_server(personIds[matchIndex], location="Morro Bento", camera=camera)
                else:
                    send_recognition_to_server(personIds[matchIndex], location="Morro Bento", camera=camera)
                last_seen[personIds[matchIndex]] = current_time

            imgBackground[162:162+480, 55:55+640] = img

            if show == 'show':
                cv2.imshow("Reconhecimento Facial", imgBackground)
                cv2.waitKey(1)
    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <arg1> [<arg2>]")
        logging.error("Uso incorreto do script: argumentos insuficientes.")
        sys.exit(1)
    
    arg1 = sys.argv[1]
    arg2 = sys.argv[2] if len(sys.argv) > 2 else None
    main(arg1, arg2)

