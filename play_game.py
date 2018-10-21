import sys
from OthelloGame import OthelloGame

if __name__ == "__main__":
	if len(sys.argv) > 1:
		length = int(sys.argv[1])
	else:
		length = 8
	
	othello_game = OthelloGame(length=length)
	print('Welcome to this game of Othello!')
	othello_game.run_game()