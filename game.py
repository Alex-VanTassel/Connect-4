from board import Board

class Game():
    def __init__(self, agent1, agent2, cols = 7, rows = 6, display = False):
        self.board = Board(cols, rows)
        self.player0 = agent1
        self.player1 = agent2
        self.display = display
        self.turn = 0
    def run(self):
        while not self.board.check_game_over():
            if self.display:
                print(f"Turn: {self.turn + 1}")
                print(self.board)
                print(self.board.moveable_cols())
            if self.turn % 2 == 0:
                desired_col = self.player0.move(self.board)
                self.board.move(desired_col, 0)
            else:
                desired_col = self.player1.move(self.board)
                self.board.move(desired_col, 1)
            self.turn += 1
        
        print(self.board)
        result = self.board.check_winner()
        if result == 0:
            print(f"{self.player0} wins")
        elif result == 1:
            print(f"{self.player1} wins")
        else:
            print("Tie")

    def get_winner(self):
        return self.board.check_winner()