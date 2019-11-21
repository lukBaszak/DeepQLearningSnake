from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy as np
import pandas as pd
from operator import add
import math


class DQNAgent():
    def __init__(self):
        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.learning_rate = 0.0005
        self.model = self.network()
        self.epsilon = 0
        self.actual = []
        self.memory = []

    def get_state(self, game):

        distance = math.sqrt(
            pow(game.snake.snake_body[0].get_x() - game.apple.get_x(), 2) + pow(game.snake.snake_body[0].get_y() - game.apple.get_y(), 2))



        apple_quarter_position = 0
        if game.apple.get_x() >= game.snake.snake_body[0].get_x() == game.apple.get_y() <= game.snake.snake_body[0].get_y():
            apple_quarter_position = 1
        if game.apple.get_x() <= game.snake.snake_body[0].get_x() == game.apple.get_y() <= game.snake.snake_body[0].get_y():
            apple_quarter_position = 2
        if game.apple.get_x() <= game.snake.snake_body[0].get_x() == game.apple.get_y() >= game.snake.snake_body[0].get_y():
            apple_quarter_position = 3
        if game.apple.get_x() >= game.snake.snake_body[0].get_x() == game.apple.get_y() >= game.snake.snake_body[0].get_y():
            apple_quarter_position = 4

        left_obstacle = 0
        right_obstacle = 0
        up_obstacle = 0
        down_obstacle = 0

        for segment in game.snake.snake_body:
            if (segment.get_x() + 1 == game.snake.snake_body[0].get_x()) and (segment.get_y() == game.snake.snake_body[0].get_y()):
                left_obstacle = 1
            if (segment.get_x() - 1 == game.snake.snake_body[0].get_x()) and (segment.get_y() == game.snake.snake_body[0].get_y()):
                right_obstacle = 1
            if (segment.get_x() == game.snake.snake_body[0].get_x()) and (segment.get_y() + 1 == game.snake.snake_body[0].get_y()):
                down_obstacle = 1
            if (segment.get_x() + 1 == game.snake.snake_body[0].get_x()) and (segment.get_y() - 1 == game.snake.snake_body[0].get_y()):
                up_obstacle = 1

        if game.snake.snake_body[0].get_x()-1()<0:
            left_obstacle = 1
        if game.snake.snake_body[0].get_x()+1()>=game.game_width:
            right_obstacle = 1
        if game.snake.snake_body[0].get_y()-1()<0:
            down_obstacle = 1
        if game.snake.snake_body[0].get_y()+1()>=game.game_height:
            up_obstacle = 1

        return [apple_quarter_position, left_obstacle, right_obstacle, up_obstacle, down_obstacle]




    def get_reward(self, old_game, new_game, crash):
        old_distance = math.sqrt(
            pow(old_game.snake.get_x() - old_game.apple.get_x(), 2) + pow(old_game.snake.get_y() - old_game.apple.get_y(), 2))
        new_distance = math.sqrt(
            pow(new_game.snake.get_x() - new_game.apple.get_x(), 2) + pow(new_game.snake.get_y() - new_game.apple.get_y(), 2))

        if new_distance > old_distance:
            self.reward = self.reward + 1
        if crash:
            self.reward = self.reward - 20
        if new_distance == 0:
            self.reward = self.reward + 20



    def network(self, weights=None):

        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim=11))
        model.add(Dropout(0.2))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(output_dim=3, activation= 'softmax'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))

    # def remember

