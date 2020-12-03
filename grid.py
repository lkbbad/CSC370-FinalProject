'''
Class creates grid with initial board state
formed by reverse walking legal button presses 
from a finished board.
Authors: Lindy Bustabad and Jenny Zhong
'''

import random
import copy
import numpy as np
from copy import deepcopy

RANDOMIZATION_NUMBER = 15

class LightsOutGrid():
    def __init__(self, size):
        self.state = []
        for _ in range(size):
            self.row = []
            for _ in range(size):
                self.row.append(0)
            self.state.append(self.row)
        self.size = size
        self.steps = 0

    def __cmp__(self, other):
        value = np.sum(self.state)
        o_value = np.sum(other.state)
        if value < o_value:
            return -1
        elif value > o_value:
            return 1
        else:
            return 0

    def __eq__(self, other):
        for row in range(self.size):
            for col in range(self.size):
                if self.state[row][col] is not other.state[row][col]:
                    return False
        return True

    def __lt__(self, other):
        value = np.sum(self.state)
        o_value = np.sum(other.state)
        return value < o_value

    '''
    Class function that returns a representation of the current state of the grid.
    '''
    def __repr__(self):
        res = ''
        for row in range(self.size):
            res += ' '.join(map(str, self.state[row]))
            res += '\r\n'
        return res

    '''
    Returns grid self with the light (x, y) toggled, and all neighbors toggled as well.
    '''
    def toggle(self, row, col):
        if self.state[row][col] == 1:
            self.state[row][col] = 0
        else:
            self.state[row][col] = 1

        if row > 0:  # is there a light above the chosen light?
            if self.state[row-1][col] == 1:
                self.state[row-1][col] = 0
            else:
                self.state[row-1][col] = 1
        if row < self.size-1:  # is there a light below the chosen light?
            if self.state[row+1][col] == 1:
                self.state[row+1][col] = 0
            else:
                self.state[row+1][col] = 1
        if col > 0:  # is there a light to the left of the chosen light?
            if self.state[row][col-1] == 1:
                self.state[row][col-1] = 0
            else:
                self.state[row][col-1] = 1
        if col < self.size-1:  # is there a light to the right of the chosen light?
            if self.state[row][col+1] == 1:
                self.state[row][col+1] = 0
            else:
                self.state[row][col+1] = 1
        return self

    '''
    Returns list of all possible next moves from current state.
    '''
    def possibleMoves(self):
        nodes = []
        for row in range(self.size):
            for col in range(self.size):
                updated_grid = copy.deepcopy(self)  # make a copy of state
                if updated_grid.state[row][col] == 1:
                    updated_grid.state[row][col] = 0
                else:
                    updated_grid.state[row][col] = 1

                if row > 0:  # is there a light above the chosen light?
                    if updated_grid.state[row-1][col] == 1:
                        updated_grid.state[row-1][col] = 0
                    else:
                        updated_grid.state[row-1][col] = 1
                if row < updated_grid.size-1:  # is there a light below the chosen light?
                    if updated_grid.state[row+1][col] == 1:
                        updated_grid.state[row+1][col] = 0
                    else:
                        updated_grid.state[row+1][col] = 1
                if col > 0:  # is there a light to the left of the chosen light?
                    if updated_grid.state[row][col-1] == 1:
                        updated_grid.state[row][col-1] = 0
                    else:
                        updated_grid.state[row][col-1] = 1
                if col < updated_grid.size-1:  # is there a light to the right of the chosen light?
                    if updated_grid.state[row][col+1] == 1:
                        updated_grid.state[row][col+1] = 0
                    else:
                        updated_grid.state[row][col+1] = 1
                nodes.append(updated_grid)
        return nodes
    
    '''
    Returns an iterable of all actions which can be taken from this state (for MCTS)
    '''
    def getPossibleActions(self):
        possibleActions = []
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                possibleActions.append(Action(x=i, y=j))
        return possibleActions
    
    '''
    Returns the state which results from taking an action (for MCTS)
    '''
    def takeAction(self, action):
        newState = deepcopy(self)
        newState.toggle(action.x, action.y)
        return newState
    
    '''
    Returns whether this state is a terminal state (for MCTS)
    '''
    def isTerminal(self):
        if(np.sum(self.state) == 0):
            return True
        else:
            return False
    
    '''
    Returns the reward for this state. Only needed for terminal states (for MCTS)
    '''
    def getReward(self):
        #return np.sum(self.state)
        if(self.isTerminal()):
            return True
        else:
            return False
    
    '''
    Returns the heuristic value of a board
    '''
    def heuristic(self):
        return np.sum(self.state) / 5



class Action():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))



'''
Function that uses a randomized number of iterations to return the initial
state of the grid by turning on lights starting from a finished state.
'''
def initGrid(grid):
    iterations = random.randint(4, RANDOMIZATION_NUMBER)
    # print("Minimum Number of Moves: ", iterations)
    for _ in range(iterations):
        rand_row = random.randint(0, grid.size-1)
        rand_col = random.randint(0, grid.size-1)
        grid = grid.toggle(rand_row, rand_col)
    return grid



if __name__ == '__main__':
    grid = LightsOutGrid(5)
#    print(grid)
#    print(toggle(grid,3,4))
#    print(toggle(grid,4,4))
#    print(toggle(grid,3,2))
#    print(toggle(grid,4,3))
    initState = initGrid(grid)
    print(initState)
    print(initState.possibleMoves())




