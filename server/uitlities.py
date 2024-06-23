import cv2
import face_recognition
import pickle
import os
import base64
import jwt

jwt_secret = "AFDASG#@#%$33"
jwt_algorithm = "HS256"
secret = 'fashgfkhkf4324fds^'

def auth(token):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=jwt_algorithm)
        user_id = payload['user_id']
        user_id = int(user_id)
        return True
    except:
        return False

def encode(msg, key=secret):
    enc = []
    for i in range(len(msg)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(msg[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(enc, key=secret):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def encodeIMGs():
    # importing the students images
    folderPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "server/static/images")
    pathList = os.listdir(folderPath)
    imgList = []
    personBIs = []
    for path in pathList:
      imgList.append(cv2.imread(os.path.join(folderPath, path)))
      personBIs.append(path.split('.')[0])
      #print(path.split('.')[0])
      #print(personBIs)

    def findEncodings(imagesList):
      encodeList = []
      for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
      return encodeList

    print('Encoding Started ...')
    #print(pathList)
    encodeListKnow = findEncodings(imgList)
    encodeListKnowWithIds = [encodeListKnow, personBIs]
    print('Encoding Complete')

    directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "server/static/encodes")
    file_path = os.path.join(directory, 'EncodeFile.p')
    with open(file_path, 'wb') as file:
        pickle.dump(encodeListKnowWithIds, file)

    print('File Saved')