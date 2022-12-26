import math
import random
import numpy


class Node:#A node class, any place in the graph that can be visited
    def __init__(self,board,level,Fval,heuristic=0,father=0): #Each node receives a board, steps it has already taken, Fval, its heuristic and the name of the previous node it came fromFval
        self.board=board #
        self.level=level #
        self.Fval=Fval # Fval=heuristic+level
        self.father=father
        self.heuristic=heuristic

    def all_kinges_moves(self,board, row, column): #A board method that accepts a coordinate and returns all legal moves to the king from that point
        possible_moves = []  # Here I will save all the possible steps in the form of coordinates
        row_possible = row - 1
        for i in range(3):  #King can only move in a 3x3 radius
            column_possible = column - 1
            for j in range(3):
                if row_possible >= 0 and row_possible < len(board) and column_possible >= 0 and column_possible < len(board) and board[row_possible][column_possible] == 0:  # Checking that the step is legal
                    possible_moves += [[row_possible, column_possible]]  #If the step is possible, it can be added to the list
                column_possible = column_possible + 1
            row_possible = row_possible + 1
        return possible_moves

    def all_bishopes_moves(self,board,row,column): #A board method that accepts a coordinate and returns all legal moves to the bishopes from that point
        possible_moves = [] # Here I will save all the possible steps in the form of coordinates
        row_possible = row
        column_possible = column
        while row_possible + 1 < len(board)  and column_possible - 1 >= 0 and board[row_possible + 1][column_possible - 1] == 0:  # A method for checking all possible steps in the down and left direction
            possible_moves += [[row_possible + 1, column_possible - 1]]
            row_possible = row_possible + 1
            column_possible = column_possible - 1
        row_possible = row
        column_possible = column
        while row_possible + 1 < len(board)  and column_possible + 1 < len(board)  and board[row_possible + 1][column_possible + 1] == 0:  # A method for checking all possible steps in the down and right direction
            possible_moves += [[row_possible + 1, column_possible + 1]]
            row_possible = row_possible + 1
            column_possible = column_possible + 1
        row_possible = row
        column_possible = column
        while row_possible - 1 >= 0 and column_possible - 1 >= 0 and board[row_possible - 1][column_possible - 1] == 0:   #  A method for checking all possible steps in the up and left direction
            possible_moves += [[row_possible - 1, column_possible - 1]]
            row_possible = row_possible - 1
            column_possible = column_possible - 1
        row_possible = row
        column_possible = column
        while row_possible - 1 >= 0 and column_possible + 1 < len(board) and board[row_possible - 1][column_possible + 1] == 0:  #  A method for checking all possible steps in the up and right direction
            possible_moves += [[row_possible - 1, column_possible + 1]]
            row_possible = row_possible - 1
            column_possible = column_possible + 1
        row_possible = row
        column_possible = column
        return possible_moves

    def copy(self, board): #A method for deep copying a board
        board_copy = []
        for i in board:
            t = []
            for j in i:
                t.append(j)
            board_copy.append(t)
        return board_copy

    def create_a_new_board(self,board,row,column,coordinates): #A function to create a new board from a coordinate and a step
        new_row = coordinates[0] #Coordinate X
        new_column = coordinates[1] #Coordinate Y
        board_copy=self.copy(board) #Create a new board
        solider_move=board_copy[new_row][new_column] #We will keep the soldier who moves
        board_copy[new_row][new_column]=board_copy[row][column] #We will replace the soldiers
        board_copy[row][column]=solider_move #We will replace the soldiers, again :)
        return board_copy


    def genererate_child(self): #We will create additional nodes from the given node by checking all the options for moving the tools (all the new modes)
        children = []  # I will enter here all the possible moves from a kings or bishopes after I create them
        for row in range(len(self.board)): #We will run all over the board and look for moveable soldiers
            for column in range(len(self.board)):
                moves_are_possible = []
                if self.board[row][column]==2: #A king on the game board is marked as 2
                    moves_are_possible+= self.all_kinges_moves(self.board, row, column) #Insert into possible moves to check all the moves of the tool
                if self.board[row][column]==3: #A bishopes on the game board is marked as 3
                    moves_are_possible+=self.all_bishopes_moves(self.board,row,column) #Insert into possible moves to check all the moves of the tool
                if moves_are_possible: #If we found legal steps, we will create a new game board for each step, we will mark a game board as a child
                    for move in moves_are_possible:
                        child = self.create_a_new_board(self.board,row,column,move)
                        child_node = Node(child,self.level+1,0) #For each newly created board, the step (G value) is equal to the step of the board that created it + one step (1 =the price for one move)
                        children.append(child_node)
        return children

class NodeForGenetic(Node):
    def __init__(self,board,level,Fval,heuristic,father,father2=0,probability=[0,0],mutation="no"):
        Node.__init__(self,board,level,Fval,heuristic,father)
        self.father2=father2
        self.probability=probability
        self.mutation=mutation

    def genererate_child(self,goal):
        children = []  # I will enter here all the possible moves from a kings or bishopes after I create them
        for row in range(len(self.board)): #We will run all over the board and look for moveable soldiers
            for column in range(len(self.board)):
                moves_are_possible = []
                if self.board[row][column]==2: #A king on the game board is marked as 2
                    moves_are_possible+= self.all_kinges_moves(self.board, row, column) #Insert into possible moves to check all the moves of the tool
                if self.board[row][column]==3: #A bishopes on the game board is marked as 3
                    moves_are_possible+=self.all_bishopes_moves(self.board,row,column) #Insert into possible moves to check all the moves of the tool
                if moves_are_possible: #If we found legal steps, we will create a new game board for each step, we will mark a game board as a child
                    for move in moves_are_possible:
                        child = self.create_a_new_board(self.board,row,column,move)
                        child_node = NodeForGenetic(board=child,level=self.level+1,Fval=self.Fval,heuristic=heuristic(child,goal),father=self.father,father2=self.father2,probability=[0,0]) #For each newly created board, the step (G value) is equal to the step of the board that created it + one step (1 =the price for one move)
                        children.append(child_node)
        return children


class A_star: #A function that simulates a board solution method using A-STAR
    def __init__(self):
        self.open=[] #All the open nodes that we haven't visited yet (will be sorted for retrieval according to F value)
        self.closed=[] #All the closed intersections we have already visited so that we will not visit them again

    def Fvaluecalculation(self,start_board, goal_board): #A function to calculate F
        heuristicValue=heuristic(start_board.board,goal_board) #A function to calculate H from node named "start_board" from ther we can get access to the board
        start_board.heuristic=heuristicValue #We will update the heuristic of the node
        return heuristicValue+start_board.level # F value=Heuristic+G (G=level)

    def checkIfVisitedBefore(self, child,listClosed):#A function that checks if we have already visited this node before
        for i in listClosed: #For each node that exists in the list of boards we visited
            if i.board==child.board: #If her board is the same as the board we just found
                return True #If we have visited before there is no point in visiting again
        return False

    def detail_output_true(self,board, flag_for_printing_heuristic):
        if (flag_for_printing_heuristic):  # If you are the first step print
            print("the heuris of the first board:", board.heuristic)

    def reverse_board(self,board, flag_for_printing_heuristic):  # Retrace your path to the final destination
        way = [board]
        while (board.father != 0):  # The diplative value of "father" for the node is 0
            way.append(board.father)
            board = board.father
        way.reverse()  # The path goes from the end to the beginning so we will perform a reverse operation
        for i in way:
            print("board:", i.level)
            printBoard(i)
            if (i.level == 1):
                self.detail_output_true(i, flag_for_printing_heuristic)

    def proces(self,board,goal,flag_for_printing_heuristic):
        flag_for_finding_solution=False #ישתנה רק אם נמצא פתרון לבעיהWill change only if a solution to the problem is found, otherwise we will print that no solution was found
        board=Node(board,0,0) #We will create a new node from the starting board
        Can_You_Be_Solved=are_you_possible_board(board.board,goal)
        board.Fval=self.Fvaluecalculation(board,goal) #Calculate the value board F and insert it into the node
        self.open.append(board) #Add the node to the list of boards to check
        the_best_board=self.open[0] #We would like to check later if our end node arrives with the best time, as a diplative value we will define the first node as the best path and we will make sure to rule out this possibility in the rest of the code
        the_first_board=self.open[0] #we will cheek if our best board isn't the firs board
        while len(self.open)>0 and Can_You_Be_Solved==True: #We will want to continue searching for a path as long as there are open nodes and its possible to solve the board
            checkBoard=self.open[0] #Extract the first node in the list ordered by F
            if(checkBoard.level>=the_best_board.Fval and flag_for_finding_solution==True):
                #If the first node in the list has already performed more steps (costing 1) than the total F of the best path, no improvement path is found in the list anymore
                break
            if(checkBoard.heuristic==0): #If you have reached the final board check if this is the best way
                flag_for_finding_solution=True #Confirmation that a path to the best board has been found
                if checkBoard.Fval < the_best_board.Fval or the_best_board==the_first_board: #check if this is the best way
                    the_best_board=checkBoard
            for child in checkBoard.genererate_child(): #We will create a node for each displacement option of the tested node
                if not self.checkIfVisitedBefore(child,self.closed): #We will check if we previously found a path to the intersection
                    child.Fval = self.Fvaluecalculation(child, goal)  #If we did not visit the intersection, the F value is considered
                    not_visited = True #Mark correctly that we have not yet visited the intersection
                    for i in self.open: #We would like to check for each intersection, whether there is currently an intersection with the same board in the open list
                        if i.board == child.board: #If we find it, we will check for a smaller F panel and leave it
                            not_visited = False #If we found an identical node, we do not need to create another such node
                            if i.Fval > child.Fval: #If the existing F is greater than the F value at the node, it will be deleted
                                self.open.remove(i)
                                child.father = checkBoard #We will define a creating node for it - father
                                self.open.append(child) #We will put the node in the list of open nodes to be checked
                    if not_visited==True:
                        child.father = checkBoard
                        self.open.append(child)
            self.closed.append(checkBoard) #We will move the checked node to nodes that do not need to be checked again
            del self.open[0] #Delete the tested node from the list of open nodes
            self.open.sort(key=lambda x: x.Fval , reverse=False) #We will arrange the list of open nodes according to F
        if(flag_for_finding_solution==False): #If we did not find a route to the end junction
            print("NO PATH FOUND")
        else: #If we found a route, we will restore it
            self.reverse_board(the_best_board,flag_for_printing_heuristic)

class hill_climbing:

    def __init__(self):
        self.open=[]

    def detail_output_true(self,board, flag_for_printing_heuristic):
        if (flag_for_printing_heuristic):  # If you are the first step print
            print("the heuris of the first board:", board.heuristic)

    def reverse_board(self,board, flag_for_printing_heuristic):  # Retrace your path to the final destination
        way = [board]
        while (board.father != 0):  # The diplative value of "father" for the node is 0
            way.append(board.father)
            board = board.father
        way.reverse()  # The path goes from the end to the beginning so we will perform a reverse operation
        for i in way:
            print("board:", i.level)
            printBoard(i)
            if (i.level == 1):
                self.detail_output_true(i, flag_for_printing_heuristic)

    def procces(self,board,goal,flag_for_printing_heuristic):
        board=Node(board,0,0) #We will create a new node from the starting board
        Can_You_Be_Solved=are_you_possible_board(board.board,goal) #We will check if the board is resolved
        board.heuristic=heuristic(board.board,goal) #We will update each board with its heuristics
        self.open.append(board)
        self.open=create_child(self.open,board,goal) #A function that creates possible boards from our board and inserts them into the open boards
        for  i in range(5): #We will run the algorithm up to 5 times
            checkBoard=self.open[round(random.random()*len(board.board))] #We will rand the next board from the available options
            while True and Can_You_Be_Solved: #do while loop
                self.open.clear() #From each board you can only advance to the next board and not back
                if(checkBoard.heuristic==0): #We will stop the run if the heuristic of the current board is equal to zero
                    break
                self.open=create_child(self.open,checkBoard,goal)
                self.open.sort(key=lambda x: x.heuristic, reverse=False) #We will arrange the boards according to heuristics
                if self.open[0].heuristic>=checkBoard.heuristic:
                    break
                checkBoard=self.open[0]
            if checkBoard.heuristic==0:#If we stopped the WHILE run because we found a solution, the FOR run can be stopped
                break
        if Can_You_Be_Solved==False:
            print("NO PATH FOUND")
        else:
            self.reverse_board(checkBoard, flag_for_printing_heuristic)

class Simulated_annealing:
    def __init__(self):
        self.open=[]
        self.temperature_schedule=100
        self.T0=0

    def take_a_step(self,check_Board,goal):
        self.temperature_schedule = self.temperature_schedule - 1
        self.open.clear()
        self.open.append(check_Board)
        self.open=create_child(self.open,check_Board,goal)

    def Temperature_calculation(self):
        if self.temperature_schedule > 100*2/3 :
            return self.T0/numpy.log(1+(100-self.temperature_schedule)) #logaritmic schedule
        if self.temperature_schedule< 100*2/3 and self.temperature_schedule> 100*1/3:
            return 0.95**(100-self.temperature_schedule)*self.T0 #geometric schedule
        return self.T0**((100-self.temperature_schedule)/100)

    def Risk_calculation(self,check_Board,current_board):
        delta=current_board.heuristic-check_Board.heuristic
        if(delta==0):
            return 0.5
        E=math.e
        Temperature=E**(delta/ self.Temperature_calculation())
        return Temperature

    def found_step(self,check_board,current_board,probability): #A function that checks and returns the step I took
        move=[]
        for row in range(len(check_board.board)):
            for column in range(len(check_board.board)):
                if current_board.board[row][column]!=check_board.board[row][column]:
                    move.append(row)
                    move.append(column)
        move.append(probability)
        return move

    def detail_output_true(self,steps):
          for i in steps:
              print ('(',i[0],',',i[1],')','->','(',i[2],',',i[3],')',';', 'probability:',i[4])


    def reverse_board(self,board,steps,flag_for_printing_heuristic):  # Retrace your path to the final destination
        way = [board]
        while (board.father != 0):  # The diplative value of "father" for the node is 0
            way.append(board.father)
            board = board.father
        way.reverse()  # The path goes from the end to the beginning so we will perform a reverse operation
        for everyboard in way:
            print("board:", everyboard.level)
            printBoard(everyboard)
            if (everyboard.level == 0 and flag_for_printing_heuristic):
                self.detail_output_true(steps)

    def proces(self,board,goal,flag_for_printing_heuristic):
        current_board=Node(board,0,0)
        steps=[] #all movement options that did not succeed until the first success
        counter_for_boards=0; #We would like to save the steps only for the 0 board
        Can_You_Be_Solved = are_you_possible_board(current_board.board, goal)  # We will check if the board is resolved
        current_board.heuristic=heuristic(current_board.board,goal) #Find the heuristic of the first board
        self.T0=current_board.heuristic
        self.open.append(current_board) #We will put the first board in the list of tests
        self.open=create_child(self.open,current_board,goal) #We will create new boards from the first board
        while Can_You_Be_Solved and self.temperature_schedule>0:
            check_Board = self.open[round(random.random() * len(current_board.board))]  # We will rand the next board from the available options
            if check_Board.heuristic<current_board.heuristic: #If the drawn board is better than ours we will move to it
                if counter_for_boards == 0: #If this is the first move, we will keep the options for moving
                    steps.append(self.found_step(check_Board, current_board, 1)) #A function that saves a specific shift with the chance and puts it in a list
                self.take_a_step(check_Board,goal) #A function that performs the step
                current_board=check_Board
            else:
                Risk_calculation=self.Risk_calculation(check_Board,current_board) #A function that calculates and returns the temperature
                if counter_for_boards == 0:
                    steps.append(self.found_step(check_Board, current_board,Risk_calculation))
                rand_num=random.random()
                if(rand_num<Risk_calculation): #If I drew a number lower than the temperature I will take the step
                    self.take_a_step(check_Board,goal)
                    current_board=check_Board
            counter_for_boards = counter_for_boards + 1
        if Can_You_Be_Solved == False:
            print("NO PATH FOUND")
        else:
            self.reverse_board(check_Board,steps,flag_for_printing_heuristic)

class Local_beam_search:
    def __init__(self):
        self.open=[]
        self.first3=[] #Saves the three options for movement in the first panel


    def findsolution(self,most_optional,middle_optional,random_board): #A function that checks whether a solution is found
        if most_optional.heuristic==0 or middle_optional.heuristic==0 or random_board.heuristic==0:
            return True
        else:
            return False

    def detail_output_true(self, flag_for_printing_heuristic): # If you need to print the detail output
        if (flag_for_printing_heuristic):
            numasci=97
            for i in self.first3:
                print("board 1",chr(numasci),':')
                printBoard(i)
                numasci=numasci+1

    def reverse_board(self, board, flag_for_printing_heuristic):  # Retrace your path to the final destination
        way = [board]
        while (board.father != 0):  # The diplative value of "father" for the node is 0
            way.append(board.father)
            board = board.father
        way.reverse()  # The path goes from the end to the beginning so we will perform a reverse operation
        for i in way:
            if (i.level == 1):
                self.detail_output_true(flag_for_printing_heuristic)
            print("board:", i.level)
            printBoard(i)



    def proces(self,board,goal,flag_for_printing_heuristic):
        flag_for_finding_solution = False  # Will change only if a solution to the problem is found, otherwise we will print that no solution was found
        current_board = Node(board, 0, 0)  # We will create a new node from the starting board
        Can_You_Be_Solved = are_you_possible_board(current_board.board, goal)
        current_board.heuristic = heuristic(current_board.board, goal)  # Find the heuristic of the first board
        self.open.append(current_board)
        self.open=create_child(self.open,current_board, goal)  # We will create new boards from the first board
        sol_found=False #I will check if one of the boards reached the target
        counter_of_moves=1
        while Can_You_Be_Solved and not sol_found:
            most_optional=self.open[0] #The board with the highest odds
            middle_optional=self.open[round(len(self.open)/2)] # The board with the middle chance
            random_board=self.open [round(random.random() *(len(self.open)))] #random board, who know whats will hapend :)
            self.open.clear()#The old boards are not interesting
            self.open=create_child(self.open,most_optional,goal)
            self.open = create_child(self.open,middle_optional,goal)
            self.open=create_child(self.open,random_board,goal)
            self.open.sort(key=lambda x: x.heuristic,reverse=False)  # We will arrange the list of open nodes according to the heuristic
            if(counter_of_moves==1):
                self.first3.append(most_optional)
                self.first3.append(middle_optional)
                self.first3.append(random_board)
            sol_found=self.findsolution(most_optional,middle_optional,random_board)
            counter_of_moves=counter_of_moves+1
        if(Can_You_Be_Solved==False):
            print("NO PATH FOUND")
        else:
            self.reverse_board(most_optional, flag_for_printing_heuristic)

class Genetic_Algorithm:
    def __init__(self):
        self.open=[]
        self.heuriisrticSum =0 #We will save the total heuristics in order to normalize the probability of the boards being selected
        self.nurmalizationSum=0 #will sum the:( heuristicSum - board.heuristic)^3

    def give_A_probability(self):#A function that outputs a range of probabilities for each board
        startProbability=0
        for i in range(len(self.open)):
            heuristic_value_for_probability=(self.heuriisrticSum-self.open[i].heuristic)**22 #We will increase the probability of choosing the board
            endProbability=startProbability+(heuristic_value_for_probability/self.nurmalizationSum) #A high probability is given to boards with low heuristics
            self.open[i].probability=[startProbability,endProbability]
            startProbability=endProbability

    def noramlization(self): #We will normalize the relations according to high probability to low heuristics
        self.nurmalizationSum = 0
        for i in range(len(self.open)):
            self.nurmalizationSum=self.nurmalizationSum+((self.heuriisrticSum-self.open[i].heuristic)**22)

    def create_child(self, board, goal):
        self.heuriisrticSum=0
        for child in board.genererate_child(goal):
            self.heuriisrticSum=self.heuriisrticSum+child.heuristic
            child.father = board  # We will define a creating node for it - father
            self.open.append(child)
        self.noramlization()
        self.give_A_probability()#A function that outputs a range of probabilities for each board

    def random_Board(self): #Draw a board according to the probability
        randNum=random.random()
        for i in range(len(self.open)):
            if self.open[i].probability[0]<=randNum and self.open[i].probability[1]>randNum:
                return self.open[i]

    def crate_Board(self,rand_board1,rand_board2,row_from_1):
        new_board=[]
        for i in range(len(rand_board1.board)):
            new_row=[]
            for j in range(len(rand_board1.board)):
                if(j<=row_from_1):
                    new_row.append(rand_board1.board[i][j])
                else:
                    new_row.append(rand_board2.board[i][j])
            new_board.append(new_row)
        return new_board

    def mix_board(self,rand_board1,rand_board2): #tempered boards
        sum_of_board=rand_board1.heuristic+rand_board2.heuristic
        board1_ratio=rand_board1.heuristic/sum_of_board #Calculate the relative part of the new board from the first board
        board1_range= round(len(rand_board1.board)*board1_ratio) #How many lines will I give to the first board
        new_board=self.crate_Board(rand_board1,rand_board2,board1_range) #I will create a new board according to the conditions above
        return new_board

    def are_you_child(self,create_A_board,rand_board1,rand_board2,goal):
        if isinstance(create_A_board,NodeForGenetic): #If I have already done the test I will not test again
            return create_A_board
        for i in rand_board1.genererate_child(goal):
            if i.board==create_A_board:
                new_board = NodeForGenetic(board=create_A_board, level=rand_board1.level + 1, Fval=0,heuristic=heuristic(create_A_board, goal), father=rand_board1,father2=rand_board2, probability=[0, 0], mutation="no")  # If the board resolves, we will create it as a new NODE
                return new_board
        return create_A_board #If I didn't find it, return the board

    def printBoard(self,way,flag_for_printing_heuristic):
        for i in range (len(way)-1,0,-1):
            if (way[i].level == 2):
                print("starting board 1 (probability of selection from population:",way[i].father.probability[1] - way[i].father.probability[0],")")
                printBoard(way[i].father)
                print("starting board 2 (probability of selection from population:",way[i].father2.probability[1] - way[i].father2.probability[0],")")
                printBoard(way[i].father2)
                print("result board (mutation happend:",way[i].mutation,")")
            print("board:", way[i].level)
            printBoard(way[i])

    def reverse_board(self, flag_for_printing_heuristic):
        self.open.sort(key=lambda x: x.heuristic, reverse=False)  # We will arrange the list of open nodes according to H
        board=self.open[0]
        way=[board]
        while board.father!=0:
            way.append(board.father)
            board=board.father
        self.printBoard(way,flag_for_printing_heuristic)

    def rand_Step(self, board, goal):
        children = board.genererate_child(goal)
        rand = round(random.random() * (len(children) - 1))
        return children[rand]

    def Try_to_produce_a_mutation(self,new_board,goal):
        randnum = random.random()
        if (randnum < 0.3): #We would like to create one mutation for 5 board
            save_father = new_board
            new_board = self.rand_Step(new_board, goal)
            new_board.father = save_father
            new_board.mutation = "yes"
        return new_board

    def proces(self,board,goal,flag_for_printing_heuristic):
        flag_for_finding_solution = False  # Will change only if a solution to the problem is found, otherwise we will print that no solution was found
        current_board = NodeForGenetic(board,0,0,0,0,[0,0],"no")  # We will create a new node from the starting board
        Can_You_Be_Solved = are_you_possible_board(current_board.board, goal)
        current_board.heuristic = heuristic(current_board.board, goal)  # Find the heuristic of the first board
        self.open.append(current_board)
        self.create_child(current_board, goal)  # We will create new boards from the first board
        counter_of_level=0
        while counter_of_level<20 and Can_You_Be_Solved and not flag_for_finding_solution:
            self.heuriisrticSum=0
            new_population=[] #We will keep the new population
            for i in range (10): #We will maintain a constant population size of 10
                found_sol=False
                added_panel=False #Beware of the unsolvable child board
                while(added_panel==False):
                    rand_board1=self.random_Board() #First father board in genetics
                    rand_board2=self.random_Board() #Second father board in genetics
                    while(rand_board1==rand_board2): #rule out the possibility that the boards is identical
                        rand_board2=self.random_Board()
                    new_board=self.mix_board(rand_board1,rand_board2) #A function that creates a new child
                    new_board=self.are_you_child(new_board,rand_board1,rand_board2,goal)
                    new_board=self.are_you_child(new_board,rand_board2,rand_board1,goal) #I'll double check only if I don't find at first and enforce it in a function
                    if isinstance(new_board,NodeForGenetic):
                        new_board=self.Try_to_produce_a_mutation(new_board,goal) #We will create a new mutation with a certain probability or return this board
                        self.heuriisrticSum=self.heuriisrticSum+new_board.heuristic
                        new_population.append(new_board)
                        added_panel=True
                        if new_board.heuristic==0: #For each created board we will check if it is the final board
                            flag_for_finding_solution=True
            self.open.clear() #We will empty the old population
            self.open=new_population
            self.noramlization()
            self.give_A_probability()
            counter_of_level=counter_of_level+1
        if Can_You_Be_Solved==False:
            print("NO PATH FOUND")
        else:
            self.reverse_board(flag_for_printing_heuristic)

def are_you_possible_board(board,goal):
    counterBishopes=0
    counterKings=0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]==2:
                counterKings=counterKings+1
                flag=Are_king_coould_move(i,j,board,goal)
                if flag==False:
                    return False
            if board[i][j]==3:
                counterBishopes=counterBishopes+1
                flag=Are_bishopes_coould_move(i,j,board,goal)
                if flag==False:
                    return False
    if counterBishopes!=counterKings:
        return False
    return True

def Are_king_coould_move(row,column,board,goal): #Checks whether a king is trapped between traps
    if board[row][column]==goal[row][column]:
        return True
    if row>0 and column>0 and board[row-1][column-1] !=1: #left and up
        return True
    if row>0 and board[row-1][column]!=1: #up
        return True
    if row>0 and column+1<len(board) and board[row-1][column+1]!=1: #right and up
        return True
    if column>0 and board[row][column-1]!=1: #left
        return True
    if column+1<len(board) and board[row][column+1]!=1: #right
        return True
    if row+1<len(board) and column>0 and board[row+1][column-1]!=1: #down and left
        return True
    if row+1<len(board) and board[row+1][column]!=1: #down
        return True
    if row+1<len(board) and column+1<len(board) and board[row+1][column+1]!=1: #down and right
        return True
    return False

def Are_bishopes_coould_move(row,column,board,goal): #Checks whether a bishopes is trapped between traps
        if board[row][column]==goal[row][column]:
            return True
        if row > 0 and column > 0 and board[row - 1][column - 1] != 1:  #left and up
            return True
        if row>0 and column+1<len(board) and board[row-1][column+1]!=1: #right and up
            return True
        if row+1<len(board) and column>0 and board[row+1][column-1]!=1: #down and left
            return True
        if row+1<len(board) and column+1<len(board) and board[row+1][column+1]!=1: #down and right
            return True
        if can_pishopes_neet==True:
            return True
        return False

def How_many_bishopes_in_even_and_odd_places(board):
    even = 0
    odd = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 3:
                if (i + j) % 2 == 0:
                    even = even + 1
                else:
                    odd = odd + 1
    return [even, odd]

def can_pishopes_neet(board,goal):
        bishopesInStartingBoard=How_many_bishopes_in_even_and_odd_places(board)
        bishopesInGoalBoard=How_many_bishopes_in_even_and_odd_places(goal)
        if bishopesInStartingBoard[0]==bishopesInGoalBoard[0] and bishopesInStartingBoard[1]==bishopesInGoalBoard[1]:
            return True
        else:
            return False

def heuristic(board, goal): #A function to calculate the heuristics of each board
    #    The heuristics: For each soldier that can be moved on the board, we will check who is the nearest target that is available
    #    We will define a target as a possible place for this type of soldier on the finish board (there are several options)
    #    As soon as we found it, the air distance (Pythagoras) from it is considered
    #    We will sum the amount for all the players
    heuristic_sum = 0 #If we did not find options to move, we are in the final panel and the heuristic is zero
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 2 or board[i][j] == 3:
                num = board[i][j]
                distance =howFar(num, i, j, board, goal) #A function that finds the best target and returns the distance from it
                heuristic_sum += distance #Sum up all distances
    return heuristic_sum

def howFar(num, row, column, board,goal):  #Calculates the best distance between the point and its nearest unmanned endpoint
    if goal[row][column] == num:
        return 0
    bestfar = 0  # The starting point is that the point is already at the best point
    for i in range(len(board)):
        for j in range(len(board)):
            if goal[i][j] == num:
                point1 = [row, column]
                point2 = [i, j]
                far = math.dist(point1, point2)
                if bestfar == 0 or far < bestfar:
                    bestfar = far
    return bestfar

def printBoard(Node): #A method for printing a board
    import sys
    for i in range(len(Node.board)):
        for j in range(len(Node.board)):
            if Node.board[i][j]==0:
                sys.stdout.write(' '+' ')
            if Node.board[i][j]==1:
                sys.stdout.write('@'+' ')
            if Node.board[i][j]==2:
                sys.stdout.write('*'+' ')
            if Node.board[i][j]==3:
                sys.stdout.write('&'+' ')
        print()

def find_path(starting_board,goal_board,search_method,detail_output):
    if(search_method==1):
        search_method=A_star()
        search_method.proces(starting_board,goal_board,detail_output)
    if(search_method==2):
        search_method=hill_climbing()
        search_method.procces(starting_board,goal_board,detail_output)
    if (search_method==3):
        search_method=Simulated_annealing()
        search_method.proces(starting_board,goal_board,detail_output)
    if (search_method==4):
        search_method=Local_beam_search()
        search_method.proces(starting_board,goal_board,detail_output)
    if (search_method==5):
        search_method=Genetic_Algorithm()
        search_method.proces(starting_board,goal_board,detail_output)

def create_child(open,board,goal):
    for child in board.genererate_child():
        child.heuristic = heuristic(child.board, goal)
        child.father = board  # We will define a creating node for it - father
        open.append(child)
    return open


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    starting_Board1 = [[0, 0, 2, 0,3 , 0], [0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],[3, 0, 0, 2, 0, 0], [0, 2, 0, 0, 0, 0]]
    goal_board2 = [[0, 0, 0, 2, 3, 0], [0, 2, 0, 0, 0, 3], [0, 0, 3, 0, 2, 0], [0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    starting_Board = [[2, 0, 2, 0, 3, 0], [0, 0, 0, 2, 1, 3], [1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0],[3, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0]]
    goal_board = [[0, 0, 0, 2, 3, 0], [0, 2, 0, 0, 1, 3], [1, 0, 3, 0, 2, 0], [0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0],[0, 1, 0, 0, 0, 0]]

    a=True
    b=False
    find_path(starting_Board,goal_board,1,a)





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
