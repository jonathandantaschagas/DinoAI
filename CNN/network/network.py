import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn import preprocessing
import cv2

import os

# seed weights
np.random.seed(3)

X = []
Y = []

with open ('../actions.csv', 'r') as f:
    for line in f:
        Y.append(line.rstrip())


all_images = []
img_num = 0
print(len(os.listdir('../images')))
print(len(Y))
while img_num < len(os.listdir('../images')):
        img = cv2.imread(r'../images/frame_{0}.jpg'.format(img_num), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        img = img[:, :, np.newaxis]
        all_images.append(img)
        img_num += 1

X = np.array(all_images)
print(X[0].shape)

# Dividir dataset em train set e test set
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=.2, random_state=5)

## Definindo a dimensão das images
img_x, img_y = 90, 262
input_shape = (img_x, img_y, 1)

# Converter os vetores para matrizes binárias para utilizar o cross_entropy
# Numero de classificações é 3. Queremos obter 3 status diferente. 0 (Pular), 1 (Nada), 2(Abaixar)
classifications = 3
y_train = keras.utils.to_categorical(y_train, classifications)
y_test = keras.utils.to_categorical(y_test, classifications)

# Model CNN (Convolutional Neural Network)
model = Sequential()
model.add(Conv2D(100, kernel_size=(2, 2), strides=(2, 2), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(250, activation='relu'))
model.add(Dense(classifications, activation='softmax'))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])

# Capturando dados do Tensorboard
tbCallBack = keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)

model.fit(x_train, y_train, batch_size=250, epochs=22, validation_data=(x_test, y_test), callbacks=[tbCallBack])

# Salvar a aprendizagem para utilizar depois.
model.save('dino_ai_weights_post_train.h5')