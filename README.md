# othello
An implementation of the board game Othello.

To play, first ensure that you have Python 3.6 installed. If you have conda, one way to do this is by running ```conda env create -f environment.yml``` followed by ```source activate othello```. The code does not use any external packages.

In order to play the game, run

```python play_game.py n```

Where `n` is the size of the board you want to use. If you leave out the `n`, it will default to a board size of 8. You can use a smaller board size to easily test out end-game mechanics.

You will see the current state of the board, as well a prompt where you can alternately enter actions for each player. Player 0 is the black player and Player 1 is the white player. Please enter actions in the following format:

Each action is a pair of characters which specify the position where you want to put the current player's disk. The first character should be the letter for the row, and the second should be the number for the column. You can see the labelling of the rows and columns on the board which gets printed to stdout. It uses the same labelling scheme as in the spec.

So for example, if it is Player 0's turn, and you want to put their piece on f5, you would type ```f5``` and press Enter.

The sample_game.in file contains sample moves which runs a game of size 4 to completion. If you want to watch the game, you can run:

```python play_game.py 4 < sample_game.in```

A note on the terminology I used in my code:
- I used the word 'action' to refer to a move made by a player. Basically, an action is just a square on the board. However, in situations where I was validating the input format, I used the term 'position' instead, so that I didn't have to overload some of my method names.
- I used the word 'sequence' to refer to a series of positions starting from one position and going in one direction along a row, column, or diagonal. So each square on the board can have up to 8 associated 'sequences' (less if it is a corner square). I check for outflanking by looking at each of the sequences for the action (read: position) proposed by the user, and checking if outflanking occurs in that direction.