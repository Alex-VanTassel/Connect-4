import random
import time
import math
from board import Board

def convert(state):
    '''
    Function to convert game states, represented by 2D lists, to tuples, so that we can use them as keys in our q table
    '''
    return tuple([tuple([str(char) for char in row]) for row in state])

class Agent:
    def __init__(self, name="Agent"):
        pass

    def move(self, board):
        pass

    def __str__(self):
        pass

class RandomAgent(Agent):
    def move(self, board):
        cols = board.moveable_cols()[:]
        random.shuffle(cols)
        return random.choice(cols)
    
    def __str__(self):
        return 'Random Agent'

class HumanAgent(Agent):
    def move(self, board):
        flag = True
        while flag:
            try:
                move = int(input("Please enter a column number to place a chip in (left col = 0, right col = 6): "))
                if move not in board.moveable_cols():
                    raise ValueError()
                flag = False
            except:
                print("Please enter an integer 0-6 inclusive that has room to place a chip")
        
        return move
    def __str__(self):
        return 'Human Agent'

class QlearningAgent(Agent):
    def __init__(self, limit, epsilon, learning_rate, lmbda, opp):
        self.limit = limit
        self.lmbda = lmbda
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.qtable = {} # to store state action pairs
        self.learning_rates = {}
        self.visits = {}
        self.opp = opp # Opposing agent the current agent is learning to

        self.learn()
        print("Done learning")
    
    def learn(self):
        board = Board()
        start = time.time()
        while start + self.limit > time.time():
            board.reset()
            while not board.check_game_over():
                board.update_moveable_cols()
                if convert(board.board) not in self.qtable:
                    self.qtable[convert(board.board)] = {col : 0.0 for col in board.moveable_cols()}
                action = None
                if random.random() < self.epsilon:
                    action = random.choice(board.moveable_cols())
                else:
                    action = max(self.qtable[convert(board.board)].keys(), key=self.qtable[convert(board.board)].get)
                
                next_pos = board.next_state(action, 0)
                new_board = Board(pos = next_pos)
                
                # Structuring rewards for the bot
                reward = None
                if new_board.check_game_over() and board.check_winner == 0:
                    reward = 3
                else:
                    reward = 0

                # Updating the Q table
                # First, checkt to see if the updated positon is in the Q table
                if convert(new_board.board) not in self.qtable:
                    self.qtable[convert(new_board.board)] = {col : 0.0 for col in new_board.moveable_cols()}
                learning_rate = None

                

                if convert(board.board) not in self.learning_rates:
                    self.learning_rates[convert(board.board)] = {col : self.learning_rate for col in range(7)}
                    # If the current state is not in our stored learnign rates, it is also not in our stored visit counts
                if convert(board.board) not in self.visits:
                    self.visits[convert(board.board)] = {col : 0 for col in range(7)}
                
                self.visits[convert(board.board)][action] += 1 # Not working
                self.learning_rates[convert(board.board)][action] *= .999 ** self.visits[convert(board.board)][action]
                learning_rate = self.learning_rates[convert(board.board)][action]

                # Updating the Q values in the table

                future_max = max(self.qtable[convert(new_board.board)].keys(), key=self.qtable[convert(new_board.board)].get)
                self.qtable[convert(board.board)][action] += learning_rate * (reward + future_max * self.lmbda - self.qtable[convert(board.board)][action])


                board.move(action, 0) # this steps the game board to the next position, since the next position was never saved to the game board before
                if board.check_game_over():
                    break
                
                # Simulate opponent playing a move
                board.update_moveable_cols()
                opp_action = self.opp.move(board)
                board.move(opp_action, 1)

                


    def move(self, board):
        if convert(board.board) in self.qtable:
            return max(self.qtable[convert(board.board)].keys(), key = self.qtable[convert(board.board)].get)
        else:
            return random.choice(board.moveable_cols())
    
    def __str__(self):
        return 'Q-learning Agent'
    
class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0
        self.action = action

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.moveable_cols())

    def best_child(self):
        for child in self.children:
            ucb = (child.reward / (child.visits + 1e-6)) + math.sqrt(2) * math.sqrt(
                math.log(self.visits + 1) / (child.visits + 1e-6))
            child.ucb = ucb
        return max(self.children, key=lambda c: c.ucb)

    def add_child(self, child_state, action):
        child = MCTSNode(child_state, parent=self, action=action)
        self.children.append(child)
        return child

class MCTSAgent(Agent):
    def __init__(self, search_time=1, rollout_limit=100):
        self.search_time = search_time
        self.rollout_limit = rollout_limit

    def move(self, board):
        root = MCTSNode(Board(pos=board.board))
        start_time = time.time()

        while time.time() - start_time < self.search_time:
            node = self._select(root)
            if not node.state.check_game_over():
                node = self._expand(node)
                reward = self._simulate(node)
                self._backpropagate(node, reward)
        
        return root.best_child().action

    def _select(self, node):
        while node.is_fully_expanded() and not node.state.check_game_over():
            node = node.best_child()
        return node

    def _expand(self, node):
        if node.is_fully_expanded():
            return node

        untried_actions = [col for col in node.state.moveable_cols() if col not in [child.action for child in node.children]]
        action = random.choice(untried_actions)
        next_state = Board(pos=node.state.next_state(action, 0))
        return node.add_child(next_state, action)

    def _simulate(self, node):
        board = Board(pos=node.state.board)
        token = 1
        for _ in range(self.rollout_limit):
            if board.check_game_over():
                break
            action = random.choice(board.moveable_cols())
            board.move(action, token)
            token = 1 - token

        winner = board.check_winner()
        if winner == 0:
            return 1
        elif winner == 1:
            return -1
        return 0

    def _backpropagate(self, node, reward):
        while node:
            node.visits += 1
            node.reward += reward
            node = node.parent

    def __str__(self):
        return 'MCTS Agent'