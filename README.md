# tictactoe
Tic Tac Toe Game vs AI (Test Bed)
by Azahar Machwe

Tic Tac Toe test-bed to test out your AI players! 
Allows for 2 Human Players to play together or vs some provided AI Brains.

## Running the Program ##
For player vs computer, computer goes first (O) and player goes second (X):

> python tictactoe.py

For player vs player:
 
> python tictactoe.py --pvp

To start first (be O instead of X):

> python tictactoe.py --start_first



Requires numpy, argparse.


## AI Brain ##

The AI brain examples are in 'ttt_brain.py'. Each brain must provide a 'play' method that accepts the current state (in form of the tic tac toe grid). Given the simple nature of the game it is easy to supply current state information.

PatternBrain is the one used by default. It has (as knowledge) good and bad patterns. It then for each current state calculates the weight of each empty cell based on good and bad pattern activations. It attempts to maximise good patterns and minimize bad pattern matches with the next move.
