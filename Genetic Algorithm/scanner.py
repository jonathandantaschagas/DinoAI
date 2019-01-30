from PIL import Image, ImageDraw
from datetime import datetime
import os
from mss import mss
import cv2
import numpy as np
dino_color = (83, 83, 83, 255)

def screenshot(x, y, w, h, name):
    sct = mss()

    coordinates = {
        'top': x,
        'left': y,
        'width': w,
        'height': h,
    }

    img = np.array(sct.grab(coordinates))
    img = img[::,75:615]
    #img = cv2.Canny(img, threshold1=100, threshold2=200)
    cv2.imwrite('tmp_{}.png'.format(name), img)

    img = Image.open('tmp_{}.png'.format(name))
    return img

def is_dino_color(pixel):
    return pixel == dino_color

def obstacle(distance, length, speed, time):
    return { 'distance': distance, 'length': length, 'speed': speed, 'time': time }

class Scanner:
    def __init__(self):
        self.dino_start = (0, 0)
        self.dino_end = (0, 0)
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False

    def find_game(self):
        image = screenshot(312, 300, 700, 92, 'game')
        size = image.size
        pixels = []
        for y in range(0, size[1], 1):
            for x in range(0, size[0], 1):
                color = image.getpixel((x, y))
                if is_dino_color(color):
                    pixels.append((x, y))

        if not pixels:
            raise Exception("Jogo não encontrado! Você está em www.chromedino.com ?")

        self.__find_dino(pixels)

    def __find_dino(self, pixels):
        start = pixels[0]
        end = pixels[1]
        for pixel in pixels:
            if pixel[0] < start[0] and pixel[1] > start[1]:
                start = pixel
            if pixel[0] > end[0] and pixel[1] > end[1]:
                end = pixel
        self.dino_start = start
        self.dino_end = end
        print('Dino start {}'.format(start))
        print('Dino end {}'.format(end))

    def find_next_obstacle(self):
        image = screenshot(303, 300, 700, 92, 'obstacle') # (top, left, width, height)
        dist = self.__next_obstacle_dist(image)
        # print(dist)
        if dist <= 100 and not self.__change_fitness:
            self.__current_fitness += 1
            self.__change_fitness = True
        elif dist > 100:
            self.__change_fitness = False

        time = datetime.now()
        delta_dist = 0
        speed = 0

        if self.last_obstacle:
            delta_dist = self.last_obstacle['distance'] - dist
            speed = (delta_dist / ((time - self.last_obstacle['time']).microseconds)) * 10000

        self.last_obstacle = obstacle(dist, 1, speed, time)

        return self.last_obstacle

    def __next_obstacle_dist(self, image):
        pix = 0
        for row in range(0, 10, 1):
            for col in range(0, 540, 1):
                color = image.getpixel((col, row))
                if(color == dino_color):
                    pix += 1
                    # print('row: {}, col: {}'.format(row,col))
                    draw = ImageDraw.Draw(image)
                    draw.rectangle(((col, row), (col, row)), fill="red")
                    #image.save('Pixel.png')
        if(pix > 500):
            # image.save('Pixel.png')
            # print('Pix: {}'.format(pix))
            raise Exception


        for x in range(100, 540, 5):
            for y in range(10, 75, 5):
                color = image.getpixel((x, y))
                if (is_dino_color(color)):
                    return x
        return 1000000

    def reset(self):
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False

    def get_fitness(self):
        return self.__current_fitness
