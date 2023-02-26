The game below simulates a chess board using special moves that are solved by algorithms from the field of artificial intelligence.

The game:
In order to commemorate the upcoming British coronation, I have created a function that starts from one board and tries to reach another using only legal moves. Specifically, I will be using 6x6 boards that are represented as two-dimensional arrays.
A value of 0 indicates an empty space, while a value of 1 indicates a force field that blocks advancement (marked in the output by "@"). 
A value of 2 indicates a king - K agent, located at that position (marked in the output by "*"). The king agent moves (as the chess piece K) on straight lines (forward/back or left/right) or diagonally a distance of 1 per turn.
A value of 3 indicates a bishop - B agent, located at that position (marked in the output by "&"). The bishop agent moves (as the chess piece B) on diagonal lines only, any distance it wants.

To find the solution to this game, I will employ the following search methods:

A*-heuristic search.
Hill climbing algorithm, which will be restarted five times if it doesn't find the answer.
Simulated annealing, using a chosen temperature function.
Local beam search, with the number of beams (k) set to 3.
Genetic algorithm, using a population size of 10.
The starting board is a two-dimensional array populated with the values 0, 1, 2, and 3, as explained above. 

The goal board is the board I want to reach from the starting board through the process, which is also a two-dimensional array populated with the values 0, 1, 2, and 3, as explained above.

For example:
Board 1 (starting position):
1 2 3 4 5 6
1:* * &
2: * @ &
3:@
4: @ @
5:&
6: @
-----
Board 2:
1 2 3 4 5 6
1:* * &
2: * @ &
3:@ &
4: @ @
5:
6: @
-----
Board 3:
1 2 3 4 5 6
1:* * &
2: @ &
3:@ & *
4: @ @
5:
6: @
-----
Board 4:
1 2 3 4 5 6
1:* * &
2: @ &
3:@ & *
4: @ @
5:
6: @
-----
Board 5 (goal position):
1 2 3 4 5 6
1: * &
2: * @ &
3:@ & *
4: @ @
5:
6: @
-----
