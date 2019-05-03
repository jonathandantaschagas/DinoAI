from keras.models import load_model
import selenium
from mss import mss
import cv2
import numpy as np
import time

# Carrega o modelo treinado
model = load_model('./network/dino_ai_weights_post_train.h5')

# Inicia o tempo
start = time.time()

# Predição
def predict(game_element):

    # Configurando o corte da imagem do jogo. Vai variar de acordo com o tamanho da tela
    sct = mss()
    coordinates = {
        'top': 180,
        'left': 315,
        'width': 600,
        'height': 150,
    }

    # Capturar a imagem
    img = np.array(sct.grab(coordinates))

    # Adaptando a imagem para ajustar melhor ajuste ao meu modelo
    img = img[::,75:615]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.Canny(img, threshold1=100, threshold2=200)
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    img = img[np.newaxis, :, :, np.newaxis]
    img = np.array(img)

    # predição
    y_prob = model.predict(img)
    prediction = y_prob.argmax(axis=-1)

    # Se a previção for 1
    if prediction == 1:
        # Pular
        game_element.send_keys(u'\ue013')
        print('JUMP')
        time.sleep(.07)

    # Se a previsão for 0
    if prediction == 0:
        # Não faz nada
        print('NOTHING')
        pass
    # Se a previsão for 2 
    if prediction == 2:
        # Abaixar
        print('DOWN')
        # Down
        game_element.send_keys(u'\ue015')
