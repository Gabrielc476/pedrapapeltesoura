import cv2
import tensorflow
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import random
import time

cap = cv2.VideoCapture(1)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

folder = "Data/C"

labels = ["Pedra", "Papel", "Tesoura"]

timer = 0
stateResult = False
startGame = False
resultado = ""
pontuacao = 0
pontoscomputador = 0
rodando = False
computador = ""
while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)

            imgResize = cv2.resize(imgCrop, (wCal, imgSize))

            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
        if startGame:
            if stateResult is False:
                timer = time.time() - initialtime
                print(timer)
                cv2.putText(imgOutput, str(int(timer)), (300, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            if timer > 3:
                timer = 0
                stateResult = True
                rodando = False
                #escolha do jogador
                jogador = labels[index]

                print(jogador)

                # Escolha aleatória do oponente
                computador = labels[random.randint(0, len(labels) - 1)]

                print(computador)
                # Verificar quem ganhou



                if jogador == computador:
                    resultado = 'Empate!'
                elif jogador == 'Pedra' and computador == 'Tesoura':
                    pontuacao += 1
                    resultado = 'Voce ganhou!'
                elif jogador == 'Papel' and computador == 'Pedra':
                    resultado = 'Voce ganhou!'
                    pontuacao += 1
                elif jogador == 'Tesoura' and computador == 'Papel':
                    resultado = 'Voce ganhou!'
                    pontuacao += 1
                else:
                    pontoscomputador += 1
                    resultado = 'Voce perdeu!'

                print(resultado)





        cv2.putText(imgOutput, labels[index], (x - 20, y - 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(imgOutput, resultado, (400, 150), cv2.FONT_HERSHEY_COMPLEX, 1 , (0, 0, 0), 2)
        if rodando == False:
            cv2.putText(imgOutput, "aperte s para comecar", (100, 30), cv2.FONT_HERSHEY_COMPLEX, 1 , (0, 0, 0), 2)
        cv2.putText(imgOutput, "player 1: ", (450, 100), cv2.FONT_HERSHEY_COMPLEX, 1 , (0, 0, 0), 2)
        cv2.putText(imgOutput, str(int(pontuacao)), (600, 100), cv2.FONT_HERSHEY_COMPLEX, 1 , (0, 0, 0), 2)
        cv2.putText(imgOutput, "computador: ", (10,100), cv2.FONT_HERSHEY_COMPLEX, 1 , (0, 0, 0), 2)
        cv2.putText(imgOutput, str(int(pontoscomputador)), (230, 100), cv2.FONT_HERSHEY_COMPLEX, 1 , (0, 0, 0), 2)
        cv2.putText(imgOutput, computador, (10, 150), cv2.FONT_HERSHEY_COMPLEX, 1 , (0, 0, 0), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset),
                      (x + w + offset, y + h + offset), (255, 0, 255), 4)

        #cv2.imshow("ImageCrop", imgCrop)
        #cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True;
        initialtime= time.time()
        stateResult = False
        rodando = True