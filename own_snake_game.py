import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import keyboard
import time
from PIL import Image
import cv2

style.use("ggplot")

SIZE = 15

MOVE_PENALTY = 1
HIT_PENALTY = 300
APPLE_REWARD = 25
epsilon = 0.5
EPS_DECAY = 0.9999

start_q_table = None

LEARNING_RATE = 0.1
DISCOUNT = 0.95

SNAKE_N = 1
FOOD_N = 2

d = {2: (0, 0, 255),
     1: (0, 255, 0)}


class Cube(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Snake(object):
    body = []

    def __init__(self):
        self.start_x = np.random.randint(1, SIZE - 1)
        self.start_y = np.random.randint(1, SIZE - 1)
        self.body.append(Cube(self.start_x, self.start_y))

    def __str__(self):
        return f"{self.start_x}, {self.start_y}"

    def action(self, choice):
        if choice == 0:
            self.move(x=1)
        elif choice == 1:
            self.move(x=-1)
        elif choice == 2:
            self.move(y=1)
        elif choice == 3:
            self.move(y=-1)

    def move(self, x=False, y=False):
        if y:
            print("y")
            if len(self.body) > 1:

                for i in range(0, len(self.body) - 1):

                    self.body[i + 1] = self.body[i]

            self.body[0] = Cube(self.body[0].x - y, self.body[0].y)

        if x:
            print("x")
            if len(self.body) > 1:
                for i in range(0, len(self.body)-1):
                    self.body[i + 1] = self.body[i]
            self.body[0] = Cube(self.body[0].x, self.body[0].y - x)

    def add_body(self, snake, direction):
        if len(snake.body) > 1:
            tail = snake.body[-1]

            print("tail.x", tail.x)
            print("tail.y", tail.y)

            print("2_tail.x", snake.body[-2].x)
            print("2_tail.y", snake.body[-2].y)
            if tail.x == snake.body[-2].x and tail.y > self.body[-2].y:
                self.body.append(Cube(tail.x, self.body[-1].y + 1))
                print("1")

            elif tail.x == self.body[-2].x and tail.y < self.body[-2].y:
                self.body.append(Cube(tail.x, self.body[-1].y - 1))
                print("2")

            elif tail.y == self.body[-2].y and tail.x > self.body[-2].x:
                self.body.append(Cube(tail.x + 1, tail.y))
                print("3")

            elif tail.y == self.body[-2].y and tail.x > self.body[-2].x:
                self.body.append(Cube(tail.x - 1, tail.y))
                print("4")
        else:
            if direction == 'down':
                print(len(snake.body))
                snake.body.append(Cube(snake.body[0].x - 1, snake.body[0].y))
                print(len(snake.body))
            if direction == 'up':
                snake.body.append(Cube(snake.body[0].x + 1, snake.body[0].y))
            if direction == 'left':
                snake.body.append(Cube(snake.body[0].x, snake.body[0].y + 1))
            if direction == 'right':
                snake.body.append(Cube(snake.body[0].x, snake.body[0].y + 1))
        return snake


class Apple:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)


def draw_snake(size=SIZE, snake=False, apple=False):
    table = np.zeros((size, size))
    for segment in snake.body:
        table[segment.get_x(), segment.get_y()] = 1

    table[apple.x, apple.y] = 3

    return table

def check_apple_position(snake, apple):
    apple = apple
    for segment in snake.body:
        if (apple.y==segment.y|apple.x==segment.x):
            apple = Apple()
            check_apple_position(snake, apple)
    return apple



def main():
    snake = Snake()

    reward = Apple()
    reward = check_apple_position(snake, reward)

    chosen_direction = 1
    while True:

        snake.action(chosen_direction)

        if keyboard.is_pressed('down'):
            print("down")
            chosen_direction = 3
        if keyboard.is_pressed('up'):
            print("up")
            chosen_direction = 2
        if keyboard.is_pressed('right'):
            chosen_direction = 1
        if keyboard.is_pressed('left'):
            chosen_direction = 0

        if snake.body[0].x == reward.x and snake.body[0].y == reward.y:
            snake = snake.add_body(direction=chosen_direction, snake= snake)

            reward = check_apple_position(snake, Apple())


        img = get_image(reward, snake)
        cv2.imshow("image", np.array(img))  # show it!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.1)


def get_image(reward, snake):
    env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)  # starts an rbg of our size
    env[reward.x][reward.y] = d[FOOD_N]  # sets the food location tile to green color
    for segment in snake.body:
        env[segment.x][segment.y] = d[SNAKE_N]  # sets the player tile to blue
    img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = img.resize((300, 300))  # resizing so we can see our agent in all its glory.
    return img


main()
