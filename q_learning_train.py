import numpy as np
import random
import json

# Q-learning parameters
alpha = 0.1
gamma = 0.9
epsilon = 0.1
q_table = {}

def get_state(board):
    return ''.join(map(str, board.flatten()))  # Chuyển board thành chuỗi để lưu

def choose_action(state, available_actions):
    if np.random.rand() < epsilon:
        return random.choice(available_actions)
    q_values = [q_table.get((state, a), 0) for a in available_actions]
    return available_actions[np.argmax(q_values)]

def update_q_table(state, action, reward, next_state):
    old_value = q_table.get((state, action), 0)
    next_max = max([q_table.get((next_state, a), 0) for a in range(9)], default=0)
    q_table[(state, action)] = old_value + alpha * (reward + gamma * next_max - old_value)

def train():
    for episode in range(10000):
        board = np.zeros(9, dtype=int)
        done = False
        while not done:
            state = get_state(board)
            available_actions = [i for i in range(9) if board[i] == 0]
            action = choose_action(state, available_actions)

            board[action] = 1
            reward = check_reward(board)

            next_state = get_state(board)
            update_q_table(state, action, reward, next_state)

            if reward != 0 or len(available_actions) == 1:
                done = True

    # Chuyển Q-table thành dạng string để lưu thành JSON
    q_table_str = {f"{k[0]}{k[1]}": v for k, v in q_table.items()}
    with open('q_table.json', 'w') as f:
        json.dump(q_table_str, f)

def check_reward(board):
    winning_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] != 0:
            return 1 if board[a] == 1 else -1
    return 0

train()
