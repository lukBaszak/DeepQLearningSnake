import sys

import numpy as np
from matplotlib import style
import keyboard
import time
from PIL import Image
import cv2
import math
from Snake_agent import DQNAgent

# import keras
# from keras import models
# from keras.layers import *
# from keras.callbacks import TensorBoard


style.use('ggplot')

SIZE = 20

SNAKE_N = 1
FOOD_N = 2
FIELD_N = 3

games_iteration = 1000

# model_parametres
OBSERVATION_SPACE_VALUE = (SIZE, SIZE, 3)

d = {1: (0, 0, 255),
     2: (0, 255, 0),
     3: (255, 255, 255)}


class Game:

    def __init__(self, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height
        self.crash = False
        self.player = Snake(self)
        self.food = Apple(game=self)
        self.score = 0


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


class Apple(Cube):

    def __init__(self, game):
        self.x = np.random.randint(0, game.game_width)
        self.y = np.random.randint(0, game.game_height)


class Snake:


    def __init__(self):
        self.head_x = np.random.randint(1, SIZE)
        self.head_y = np.random.randint(1, SIZE)
        self.snake_body = []
        self.snake_body.append(Cube(self.head_x, self.head_y))


    def detect_collision(self):
        for segment in self.snake_body:
            if self.snake_body[0] == segment:
                return True

    def action(self, choice, apple):

        # right
        if choice == 1:
            self.move(x=1, y=0, apple=apple)
        # left
        if choice == 2:
            self.move(x=-1, y=0, apple=apple)
        # down
        if choice == 3:
            self.move(y=1, x=0, apple=apple)
        # up
        if choice == 4:
            self.move(y=-1, x=0, apple=apple)

    def move(self, x=None, y=None, apple=None):

        if self.snake_body[0].get_x() + x == apple.get_x() and self.snake_body[0].get_y() + y == apple.get_y():
            self.snake_body = [Cube(apple.get_x(), apple.get_y())] + self.snake_body
        else:
            if len(self.snake_body) > 1:
                for i in range(len(self.snake_body) - 1, 0, -1):
                    self.snake_body[i] = self.snake_body[i - 1]
            self.snake_body[0] = Cube(self.snake_body[0].x + x, self.snake_body[0].y + y)

    #
    #     if self.check_if_collided():
    #         sys.exit()
    #
    # def check_if_collided(self):
    #     for i in range(len(self.snake_body) - 1, 1, -1):
    #         if self.snake_body[0].get_x() == self.snake_body[i].get_x() and self.snake_body[0].get_y() == \
    #                 self.snake_body[i].get_y():
    #             sys.exit()




def get_image(game):
    env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)  # starts an rbg of our size

    env[game.apple.get_y()][game.apple.get_x()] = d[FOOD_N]  # sets the food location tile to green color
    for segment in game.snake.snake_body:
        env[segment.get_y()][segment.get_x()] = d[SNAKE_N]  # sets the player tile to blue
    img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = img.resize((300, 300))  # resizing so we can see our agent in all its glory.
    return img


def check_apple_position(snake, apple):
    for segment in snake.snake_body:
        if segment.get_x() == apple.get_x() and segment.get_y() == apple.get_y():
            return True
    return False





def initialize_game(game, agent):
    state_init1 = agent.get_state(game)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]

    game.snake.action(1)
    state_init2 = agent.get_state(game)
    reward1 = agent.get_state(game.player, game.crash)
    agent.remember(state_init1, 1, reward1, state_init2, game.crash)
    agent.replay_new(agent.memory)

def run():


    snake = Snake()
    chosen_direction = 1
    apple = Cube(np.random.randint(0, SIZE), np.random.randint(0, SIZE))

    while True:
        while check_apple_position(snake, apple):
            apple = Cube(np.random.randint(0, SIZE), np.random.randint(0, SIZE))


            snake.action(snake=snake, choice=chosen_direction, apple=apple)

            if snake.snake_body[0].get_x() == apple.get_x() and snake.snake_body[0].get_y() == apple.get_y():
                apple = Cube(np.random.randint(0, SIZE), np.random.randint(0, SIZE))

            while check_apple_position(snake, apple):
                apple = Cube(np.random.randint(0, SIZE), np.random.randint(0, SIZE))

            img = get_image(snake, apple)
            cv2.imshow("image", np.array(img))  # show it!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.1)




    #
    # agent = DQNAgent()
    # games_counter = 0
    # record = 0
    #
    # while games_counter < games_iteration_max:
    #     game = Game(20, 20)
    #     snake = game.player
    #     food = game.food
    #
    #     initialize_game(game, agent)
    #
    #     show_image()







run()
