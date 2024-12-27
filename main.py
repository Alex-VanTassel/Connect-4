'''
Script to actually run the Connect 4 game between different kinds of agents
'''

from game import Game
from agents import RandomAgent, HumanAgent, QlearningAgent, MCTSAgent
from board import Board

p1 = MCTSAgent(.1, 100)
p2 = QlearningAgent(10, .25, .25, .999, p1)
#           agent1, agent2, cols, rows, display

p1_wins = 0
p2_wins = 0
k = 50 # number of game iterations
for i in range(k):
    game = Game(p1, p2, display = True)
    game.run()
    if game.get_winner() == 0:
        p1_wins += 1
    elif game.get_winner() == 1:
        p2_wins += 1

print(f"{p2} win rate: {p2_wins/k}")
print(f"{p1} win rate: {p1_wins/k}")