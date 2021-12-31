

# GIOVANNA SOUZA TEODORO
# 1916080065
# POR FAVOR, LEIA O README 

# --------------------- IMPORTES --------------------- #
import numpy as np
import face_recognition as fr
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import bleedfacedetector as fd

# ---------------------- FACES ---------------------- #
nicolascage_image = fr.load_image_file("./Imagens/Pessoas/nicolascage.png")
nicolascage_face_encoding = fr.face_encodings(nicolascage_image)[0]
jimin_image = fr.load_image_file("./Imagens/Pessoas/jimin.png")
jimin_face_encoding = fr.face_encodings(jimin_image)[0]
giovanna_image = fr.load_image_file("./Imagens/Pessoas/giovanna.png")
giovanna_face_encoding = fr.face_encodings(giovanna_image)[0]
zuckerberg_image = fr.load_image_file("./Imagens/Pessoas/zuckerberg.png")
zuckerberg_face_encoding = fr.face_encodings(zuckerberg_image)[0]
homemaranha_image = fr.load_image_file("./Imagens/Pessoas/homemaranha.png")
homemaranha_face_encoding = fr.face_encodings(homemaranha_image)[0]
faces_conhecidas = [nicolascage_face_encoding, jimin_face_encoding,
                    giovanna_face_encoding, zuckerberg_face_encoding, homemaranha_face_encoding]
faces_conhecidas_nomes = ["Nicolas Cage", "Jimin",
                          "Giovanna", "Mark Zuckerberg", "Homem-Aranha"]


# ---------------------- INICIO DA CAPTURA ---------------------- #
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 640)
video_capture.set(4, 480)
# ---------------------- CONSTANTES PARA AS EMOÇÕES ---------------------- #
net = cv2
model = './emotion-ferplus-8.onnx'
net = cv2.dnn.readNetFromONNX(model) # leitura do modelo

def declara_emocoes(model="./emotion-ferplus-8.onnx"):
    global net, emocoes
    emocoes = ['Neutro', 'Feliz', 'Surpreso','Triste', 'Raivoso', 'Enojado', 'Assustado', 'Contente']
    net = cv2.dnn.readNetFromONNX(model)
declara_emocoes()

def descobre_emocao(image):
    img_copy = image.copy()
    faces = fd.ssd_detect(img_copy, conf=0.2)
    padding = 3
    for x, y, w, h in faces:
        face = img_copy[y-padding:y+h+padding, x-padding:x+w+padding]
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        resized_face = cv2.resize(gray, (64, 64))
        processed_face = resized_face.reshape(1, 1, 64, 64)
        net.setInput(processed_face)
        Output = net.forward()
        expanded = np.exp(Output - np.max(Output))
        probablities = expanded / expanded.sum()
        prob = np.squeeze(probablities)
        predicted_emotion = emocoes[prob.argmax()]
        cv2.putText(img_copy, '{}'.format(predicted_emotion), (x, y+h-x),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),2, cv2.LINE_AA)
    return img_copy
  

# ---------------------- CONSTANTES PARA O BACKGROUND ---------------------- #
segmentor = SelfiSegmentation()
fpsReader = cvzone.FPS()
listImg = os.listdir("./Imagens/Background")
imgList = []
for imgPath in listImg:
    img = cv2.imread(f'./Imagens/Background/{imgPath}')
    imgList.append(img)
indexImg = 0

while True:
    # ---------------------- RECONHECIMENTO DE FACES ---------------------- #
    ret, frame = video_capture.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)
    for (topo, direita, base, esquerda), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(faces_conhecidas, face_encoding)
        nome = "DESCONHECIDO"
        face_distances = fr.face_distance(faces_conhecidas, face_encoding)
        melhor_match_index = np.argmin(face_distances)
        if matches[melhor_match_index]:
            nome = faces_conhecidas_nomes[melhor_match_index]
        cv2.rectangle(frame, (esquerda, topo), (direita, base), (0, 0, 255), 2)
        cv2.rectangle(frame, (esquerda, base - 35),
                      (direita, base), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, nome, (esquerda + 6, base - 6),
                    font, 1.0, (255, 255, 255), 1)

    # ---------------------- EXPRESSÃO FACIAL ------------------------ #
    expressao = descobre_emocao(frame)
    # --------------------------- CROMAKEY --------------------------- #
    imgOut = segmentor.removeBG(expressao, imgList[indexImg], threshold=0.8)
    key = cv2.waitKey(1)
    if key == ord('a'):
        if indexImg > 0:
            indexImg -= 1
    elif key == ord('d'):
        if indexImg < len(imgList)-1:
            indexImg += 1
    cv2.imshow('Webcam', imgOut)
    if key == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

