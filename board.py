'''
This file will contain an implementation of Conenct 4
'''

import numpy as np

class Board():
    def __init__(self, cols = 7, rows = 6, pos = None):
        self.rows = rows
        self.cols = cols
        if not pos:
            self.board = [['.' for i in range(self.cols)] for k in range(self.rows)]
        else:
            self.board = pos
        self.available_cols = [i for i in range(self.cols)]
    
    def update_moveable_cols(self):
        for i in range(len(self.board[0])):
            if self.board[0][i] != '.' and i in self.available_cols:
                self.available_cols.remove(i)
    
    def next_state(self, col, token):
        '''
        Function that returns the next state of the board given a certain action
        '''
        if col not in self.available_cols:
            raise ValueError("Cannot get future game state; Cannot place chip in this column")
        

        reversed_board = self.board[::-1] # Reverses the board to help with move logic
        for row in reversed_board:
            if row[col] == '.':
                row[col] = token
                return reversed_board[::-1]

    
    def move(self, col, token):
        '''
        Method to simulate a single move in Connect 4

        col: the column the player would like to place a token into
        token: a unique identifier (single string character) that marks each of the players tokens

        Updates the game board with the placed token for the player
        '''
        if col not in self.available_cols:
            raise ValueError("Cannot place chip in this column")

        reversed_board = self.board[::-1] # Reverses the board to help with move logic
        i = 0
        for row in reversed_board:
            i += 1
            if row[col] == '.':
                if i == self.rows:
                    self.available_cols.remove(col)
                row[col] = token
                self.board = reversed_board[::-1]
                return

        self.update_moveable_cols()
            
    def moveable_cols(self):
        '''
        Returns a list of integers coresponding to columns on the game board that are not yet full
        '''
        return self.available_cols

    def _check_win(self, token):
            '''
            Method to check if the game is over

            token: the unique identifier for each of a players chips on the game board

            Returns True if a player has won the game, False otherwise

            NOTE: this method does NOT return whether or not the game is OVER. It is possible to tie the game of Connect 4, and in this event this function will still return False
            '''
            # Horizontal check
            for r in range(self.rows):
                for c in range(self.cols - 3):
                    if all(self.board[r][c + i] == token for i in range(4)):
                        return True
            
            # Vertical check
            for r in range(self.rows - 3):
                for c in range(self.cols):
                    if all(self.board[r + i][c] == token for i in range(4)):
                        return True
            
            # Diagonal check (down-right)
            for r in range(self.rows - 3):
                for c in range(self.cols - 3):
                    if all(self.board[r + i][c + i] == token for i in range(4)):
                        return True

            # Diagonal check (up-right)
            for r in range(3, self.rows):
                for c in range(self.cols - 3):
                    if all(self.board[r - i][c + i] == token for i in range(4)):
                        return True

            return False

    
    def check_game_over(self):
        '''
        Method to indicate whether or not a game of Connect 4 has finished. Returns True if the game is over, False otherwise
        '''
        if self._check_win(0) or self._check_win(1):
            return True
        elif all(self.board[0][c] != '.' for c in range(self.cols)):
            return True
        else:
            return False

    
    def check_winner(self):
        '''
        Method to determine the winner of the game (if there is a winner)
        '''
        if self._check_win(1):
            return 1
        elif self._check_win(0):
            return 0
        else:
            return 2 # Indicates a tie between the 2 players
    
    def reset(self):
        self.board = [['.' for i in range(self.cols)] for k in range(self.rows)]
        self.available_cols = [i for i in range(self.cols)]
    
    def __str__(self):
        str = ''
        str += ' -----------------------------\n'
        for row in self.board:
            str += ' | '
            for char in row:
                if char == 1 or char == 0:
                    str += f'{char}'
                else:
                    str += char
                str += ' | '
            str += '\n'
        str += ' -----------------------------'
        return str  
