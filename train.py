import tensorflow as tf
from tensorflow.keras.layers import InputLayer, Dense
import numpy as np
import random
from collections import deque 
from Action import Action
from PokerAI import PokerAI
from GameState import GameState
import matplotlib.pyplot as plt
from utils import plot, plot_bars
import pygame 
import time



pygame.init()


def array_to_action(array):
    if array == [1, 0, 0]:
        action = Action.CALL
    elif array == [0, 1, 0]:
        action = Action.RAISE
    else:
        action = Action.FOLD
    return action

def action_to_array(action):
    if action == Action.CALL:
        action = [1, 0, 0]
    elif action == Action.RAISE:
        action = [0, 1, 0]
    else:
        action = [0, 0, 1]
    return action



class DeepPoker(tf.keras.Model):
    def __init__(self, num_actions, num_states, **kwargs):
        super(DeepPoker, self).__init__()
        self.input_layer = InputLayer(input_shape=(num_states))
        self.hidden_layers = [
            Dense(16, activation='tanh'),
            Dense(64, activation='tanh'),
            Dense(256, activation='tanh'),
            Dense(256, activation='tanh'),
            Dense(512, activation='tanh'),
            Dense(512, activation='tanh'),
            Dense(128, activation='tanh'),
        ]
        self.output_layer = Dense(num_actions, activation='linear')

    def call(self, inputs):
        x = self.input_layer(inputs)
        for layer in self.hidden_layers:
            x = layer(x)
        return self.output_layer(x)

    def assign_new_weights(self, model_from):
        old_variables = self.trainable_variables
        new_variables = model_from.trainable_variables
        for v1, v2 in zip(new_variables, old_variables):
            v1.assign(v2.numpy())


class DQL_Model():
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=self.lr)
        self.loss = tf.keras.losses.mean_squared_error

    def train_step(self, state, action, reward, next_state, done):
        state = np.array(state, dtype=np.float32)
        next_state = np.array(next_state, dtype=np.float32)

        action = np.array(action, dtype=np.float32)
        reward = np.array(reward, dtype=np.float32)


        if len(state.shape) == 1:
            state = np.expand_dims(state, axis=0)
            next_state = np.expand_dims(next_state, axis=0)
            action = np.expand_dims(action, axis=0)
            reward = np.expand_dims(reward, axis=0)
            done = (done, )


        pred = self.model.predict(state, verbose=0)

        target = pred.copy()


        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * np.max(self.model(np.expand_dims(next_state[idx], axis=0)))

            target[idx][np.argmax(action[idx])] = Q_new

        optimizer = tf.keras.optimizers.Adam(learning_rate=self.lr)

        with tf.GradientTape() as tape:
            logits = self.model(state) 
            loss_value = self.loss(target, logits)

        grads = tape.gradient(loss_value, self.model.trainable_weights)

        optimizer.apply_gradients(zip(grads, self.model.trainable_weights))


class Agent:
    def __init__(self, max_memory, learning_rate):
        self.n_games = 0
        self.epsilon = 0 
        self.gamma = 0.9
        self.memory = deque(maxlen=max_memory)
        self.lr = learning_rate
        self.model = DeepPoker(3, 9)
        self.trainer = DQL_Model(self.model, lr=self.lr, gamma=self.gamma)


    def get_state(self, game):
        players_money = game.agent.money
        money_to_call = game.agent.get_money_to_call(game.biggest_call)

        hand = [card.token for card in game.agent.hand]
        
        table_cards = [card.token if card else 0 for card in game.table_cards]

        state = [
            players_money,
            money_to_call,

            *hand,
            *table_cards
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self, batch_size):
        print("Training long memory")


        if len(self.memory) > batch_size:
            mini_sample = random.sample(self.memory, batch_size)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        print("Training short memory")
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            print("TAKING RANDOM ACTION")
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            print("PREDICTING ACTION")
            state = np.array(state, dtype=np.float32)
            prediction = self.model.predict(np.expand_dims(state, axis=0), verbose=0)
            move = np.argmax(prediction)
            final_move[move] = 1
            print("PREDICTED ACTION: ", array_to_action(final_move))

        return array_to_action(final_move)


if __name__ == '__main__':
    learning_rate = 0.001
    batch_size = 32
    gamma = 0.99
    memory_size = 100000
    num_games = 1000
    plot_balance = []
    plot_mean_win = []
    total_income = 0
    biggest_win = 0
    agent = Agent(memory_size, learning_rate)
    game = PokerAI()

    plt.ion()

    state_old = None
    state_new = None

    taken_actions = []

    foo = -1

    while True:
        
        if game.gameState in [GameState.SHOW_PLAYERS, GameState.DEALING]:
            reward, done, agent_player, win = game.game_step(None)
            pygame.display.flip()
            continue

        if game.players_move == game.agent and not game.agent_folded:
            # if state_old
            state_old = agent.get_state(game)
            
            final_move = agent.get_action(state_old)

            taken_actions.append(final_move)
                
            reward, done, agent_player, win = game.game_step(final_move)

        
            state_new = agent.get_state(game)


            if game.gameState != GameState.DEALING:
                final_move = action_to_array(final_move)

                agent.train_short_memory(state_old, final_move, reward, state_new, done)

                agent.remember(state_old, final_move, reward, state_new, done)
                
        else:
            final_move = Action.CALL
            reward, done, agent_player, win = game.game_step(final_move)


        if done:
            foo = -1
            agent.n_games += 1
            print(f"========= GAME {agent.n_games} ========")
            print("win: ", win)
            print("reward: ", reward)

            agent.train_long_memory(32)

            if agent.n_games % 100 == 0:
                agent.model.save('models/')

            plot_balance.append(agent_player.money)
            total_income += win
            mean_income = total_income / agent.n_games
            plot_mean_win.append(mean_income)
            plot(plot_balance, plot_mean_win)
            # plot_bars(taken_actions)

        # time.sleep(0.3)

        pygame.display.flip()


