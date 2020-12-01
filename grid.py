'''
Class creates grid with initial board state
formed by reverse walking legal button presses 
from a finished board.
Authors: Lindy Bustabad and Jenny Zhong
'''
import random
import copy
import numpy as np

RANDOMIZATION_NUMBER = 15

class LightsOutGrid():
    def __init__(self, size):
        self.size = size
        self.state = []
        for _ in range(size):
            self.row = []
            for _ in range(size):
                self.row.append(0)
            self.state.append(self.row)

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
