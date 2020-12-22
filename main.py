#!/usr/bin/env python3

from cv2 import cv2
import numpy as np
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--video_source', dest='video_source',
                    help="Arquivo de origem do vídeo ou índice da câmera alvo", default="video.mp4")
parser.add_argument('-f', '--fps', dest='fps',
                    help="Quadros por segundo do vídeo", default=30)
parser.add_argument('-mh', '--min_height', dest='min_height',
                    help="Altura mínima para validar uma caixa limitante como pertencente a um carro", default=80)
parser.add_argument('-mw', '--min_width', dest='min_width',
                    help="Largura mínima para validar uma caixa limitante como pertencente a um carro", default=80)
args = parser.parse_args()


def get_center(x, y, w, h):
    return x + int(w/2), y + int(h/2)


cap = cv2.VideoCapture(args.video_source)

# Lê o primeiro quadro
success, img = cap.read()

# Cria uma caixa limitante com o input do mouse
bounding_box = cv2.selectROI("Classica", img, False)
cx, cy, cw, ch = (bounding_box[i] for i in range(4))

subtraction = cv2.bgsegm.createBackgroundSubtractorMOG()
vehicle_counter = 0

while True:
    # Lê um frame
    success, img = cap.read()

    # Desenha um retângulo branco na região de interesse
    cv2.rectangle(img, (cx, cy), (cx + cw, cy + ch), (255, 255, 255), 2)

    cropped = img[cy: cy + ch, cx: cx + cw]

    # Aplica um delay
    delay = float(1 / args.fps)
    sleep(delay)

    # Pré-processa a imagem
    # Converte para escala de cinza
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # Aplica um desfoque gaussiano para suavização
    blur = cv2.GaussianBlur(gray, (3, 3), 5)
    # Aplica sutração de fundo
    img_sub = subtraction.apply(blur)
    # Dilata a imagem para aplicação de um filtro morfológico
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    # Pega a estrutura morfológica da imagem
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # Aplica operações morfológicas
    # Mais detalhes em: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    dilated = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    contours, image = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    is_car = False

    for (i, c) in enumerate(contours):
        # Cria caixas limitantes
        (x, y, w, h) = cv2.boundingRect(c)

        # Valida o contorno
        validate_contour = (w >= args.min_width and h >= args.min_height)
        if not validate_contour:
            continue

        is_car = True

        center = get_center(cx + x, cy + y, w, h)

        # Desenha um retângulo verde na região de interesse
        cv2.rectangle(img, (cx, cy), (cx + cw, cy + ch), (0, 255, 0), 2)

        # Desenha um retângulo azul com um ponto vermelho na região de detecção
        cv2.rectangle(img, (cx + x, cy + y),
                      (cx + x + w, cy + y + h), (255, 0, 0), 2)
        cv2.circle(img, center, 4, (0, 0, 255), -1)

    if is_car:
        cv2.putText(img, "Carro", (25, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(img, "Outro", (25, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Classica", img)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()
