the game:
To commemorate the upcoming British coronation, we will bring kings to meet bishops, to crown them.
More specifically, in this exercise you will build a function that starts from one board and tries to reach another using only a chain of legal moves. We will use 6 × 6 boards which you will receive as a 2 dimensional array, in
which a value of 0 indicates the place is empty, and the value of 1 indicates there is a forcefield there,
blocking your advance (marked in the output by @).
A value of 2 indicates you have a king K agent in that location (marked in the output by *).
The king agent moves (as the chess piece K) on straight lines (forward/back or left/right) or diagonally a distance of 1 each turn.
A value of 3 indicates you have a bishop B agent in that location (marked in the output by &).
The bishop agent moves (as the chess piece B) on diagonal lines only any distance it wants. A piece can disappear if it makes a move to go beyond 
the final (6th) line, i.e., an agent making a forward move in line 6 will disappear.

search method This will be an integer. This is just from the previous exercise, it won’t be checked for correctness.
1. A*-heuristic search. You choose the heuristic.
2. A hill climbing algorithm. It should be restarted 5 times (if it didn’t find the answer).
3. Simulated annealing. You choose the temperature function.
4. A local beam search, with the number of beams (k) being 3.
5. A genetic algorithm. Population size is 10.

starting board: 
This is the beginning of your search. This is a 2-dimensional array populated with the values 0,1,2 and 3 as explained above. You can assume
this is a valid board

goal board: This is the board you wish to reach from the starting board via the process.
This is a 2-dimensional array populated with the values 0, 1, 2 and 3 as explained above.
You can assume this is a legal board, with the forcefields in the same location 

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
