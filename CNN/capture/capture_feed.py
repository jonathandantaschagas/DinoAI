import cv2
from mss import mss
import numpy as np
import keyboard
import os

def preprocessing(img):
    img = img[::,75:615]
    img = cv2.Canny(img, threshold1=100, threshold2=200)
    return img
def start():
    sct = mss()

    coordinates = {
        'top': 302,
        'left': 300,
        'width': 600,
        'height': 180,
    }

    with open('actions.csv', 'w') as csv:

        x = 0

        if not os.path.exists(r'images'):
            os.mkdir(r'./images')

        while True:
            img = preprocessing(np.array(sct.grab(coordinates)))

            if keyboard.is_pressed('up arrow'):
                cv2.imwrite('images/frame_{0}.jpg'.format(x), img)
                csv.write('1\n')
                print('Jump')
                x += 1

            if keyboard.is_pressed('down arrow'):
                cv2.imwrite('images/frame_{0}.jpg'.format(x), img)
                csv.write('2\n')
                print('Down')
                x += 1

            if keyboard.is_pressed('t'):
                cv2.imwrite('images/frame_{0}.jpg'.format(x), img)
                csv.write('0\n')
                print('Nothing')
                x += 1

            if cv2.waitKey(25) & 0xFF == ord('q'):
                csv.close()
                cv2.destroyAllWindows()
                break
