import sys

import numpy as np
from matplotlib import style
import keyboard
import time
from PIL import Image
import cv2
import math

# import keras
# from keras import models
# from keras.layers import *
# from keras.callbacks import TensorBoard


style.use('ggplot')

SIZE = 30

SNAKE_N = 1
FOOD_N = 2
FIELD_N = 3

# model_parametres
OBSERVATION_SPACE_VALUE = (SIZE, SIZE, 3)

d = {1: (0, 0, 255),
     2: (0, 255, 0),
     3: (255, 255, 255)}


# class DQNAgent:
#
#     def __init__(self):
#         self.model = self.create_model()
#         self.target_mode = self.create_model()
#         self.target_mode.set_weights(self.model.get_weights())
#
#         self.replay_memory - deque(maxlen=REPLAY_MEMORY_SIZE)
#         self.tensorboard = ModifiedTensorboardBoard(log_dir="logs/{}-{}".format(MODEL_NAME, int(time.time())))
#         self.target_update_counter = 0
#
#     def create_model(self):
#         model = models.Sequential()
#         model.add(Conv2D(356, (3,3),input_shape=OBSERVATION_SPACE_VALUE))
#         model.add(Activation('relu'))
#         model.add(MaxPooling2D(pool_size=(2,2)))
#         model.add(Dropout(0.2))
#
#         model.add(Conv2D(256, (3,3)))
#         model.add(Activation('relu'))
#         model.add(MaxPooling2D(pool_size=(2,2)))
#         model.add(Dropout=0.2)
#
#         model.add(Flatten())
#         model.add(Dense(64))
#
#         model.add(Dense(4, activation='linear'))
#
#         model.compile(loss='mse', optimizer=Adam(lr=0.001), metrics=['accruacy'])
#         return model

class Cube:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Cube):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


done = False


class Snake:
    snake_body = []

    def __init__(self):
        self.head_x = np.random.randint(1, SIZE)
        self.head_y = np.random.randint(1, SIZE)
        self.snake_body.append(Cube(self.head_x, self.head_y))

    def detect_collision(self):
        for segment in self.snake_body:
            if self.snake_body[0] == segment:
                return True

    def action(self, choice, apple):
        if choice == 1:
            self.move(x=1, y=0, apple=apple)
        if choice == 2:
            self.move(x=-1, y=0, apple=apple)
        if choice == 3:
            self.move(y=1, x=0, apple=apple)
        if choice == 4:
            self.move(y=-1, x=0, apple=apple)

    def move(self, x=None, y=None, apple=None):

        if self.snake_body[0].get_x() + x == apple.get_x() and self.snake_body[0].get_y() + y == apple.get_y():
            self.snake_body = [Cube(apple.get_x(), apple.get_y())] + self.snake_body
            print("hey")



        if len(self.snake_body) > 1:
            for i in range(len(self.snake_body) - 1, 0, -1):
                self.snake_body[i] = self.snake_body[i - 1]

        self.snake_body[0] = Cube(self.snake_body[0].x+x, self.snake_body[0].y+y)

        if self.snake_body[0].get_y() > SIZE - 1:
            self.snake_body[0] = Cube(self.snake_body[0].get_x(), 0)
        elif self.snake_body[0].get_y() < 0:
            self.snake_body[0] = Cube(self.snake_body[0].get_x(), SIZE - 1)
        elif self.snake_body[0].get_x() > SIZE - 1:
            self.snake_body[0] = Cube(0, self.snake_body[0].get_y())
        elif self.snake_body[0].get_x() < 0:
            self.snake_body[0] = Cube(SIZE - 1, self.snake_body[0].get_y())

        if self.check_if_collided():
            sys.exit()

    def check_if_collided(self):
        for i in range(len(self.snake_body) - 1, 1, -1):
            if self.snake_body[0].get_x() == self.snake_body[i].get_x() and self.snake_body[0].get_y() == self.snake_body[i].get_y():
                sys.exit()



def get_image(snake, reward):
    env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)  # starts an rbg of our size

    env[reward.get_y()][reward.get_x()] = d[FOOD_N]  # sets the food location tile to green color
    for segment in snake.snake_body:
        env[segment.get_y()][segment.get_x()] = d[SNAKE_N]  # sets the player tile to blue
    img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = img.resize((300, 300))  # resizing so we can see our agent in all its glory.
    return img


def check_apple_position(snake, apple):
    if snake.snake_body[0].get_x() == apple.get_x() & snake.snake_body[0].get_y() == apple.get_y():
        return True
    return False




def main():
    snake = Snake()
    chosen_direction = 1
    apple = Cube(np.random.randint(0, SIZE), np.random.randint(0, SIZE))

    while check_apple_position(snake, apple):
        apple = Cube(np.random.randint(0, SIZE), np.random.randint(0, SIZE))

    while not done:
        if keyboard.is_pressed('down'):
            print("down")
            chosen_direction = 3
        elif keyboard.is_pressed('up'):
            print("up")
            chosen_direction = 4
        elif keyboard.is_pressed('right'):

            chosen_direction = 1
        elif keyboard.is_pressed('left'):
            chosen_direction = 2

        snake.action(chosen_direction, apple=apple)
        print("snake x: ", snake.snake_body[0].get_x())
        print('apple x: ', apple.get_x())
        print("snake y: ", snake.snake_body[0].get_y())
        print("apple y: ", apple.get_y())
        if snake.snake_body[0].get_x() == apple.get_x() and snake.snake_body[0].get_y() == apple.get_y():
            print("hello")
            apple = Cube(np.random.randint(0, SIZE), np.random.randint(0, SIZE))
            while check_apple_position(snake, apple):
                apple = Cube(np.random.randint(0, SIZE), np.random.randint(0, SIZE))

        img = get_image(snake, apple)
        cv2.imshow("image", np.array(img))  # show it!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.1)


main()
