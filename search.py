'''
Implementation of Greedy Best-First Search algorithm to solve Lights Out! game.
Authors: Lindy Bustabad and Jenny Zhong
'''

import grid
import sys
import copy
import numpy as np
from queue import PriorityQueue
import pandas

NUMBER_OF_TRIALS = 5

'''
Returns the number of lights that are currently still on in the passed grid state.
'''
def gridSum(game):
    ret = 0
    for row in range(game.size):
        for col in range(game.size):
            ret += game.state[row][col]
    return ret

'''
Recursive backtracking implementation of greedy best-first search.
Searches nodes that turn off the most lights.
Recursively backtracks after hitting a dead end.
'''
def greedyRec(state, numMoves):
    mySum = gridSum(state)
    if mySum == 0:
        return (True, numMoves)
    visited.append(state)
    possibleMoves = state.possibleMoves()
    frontier = PriorityQueue()

    for move in possibleMoves:
        new = gridSum(move) - mySum
        frontier.put((new, move))

    while (not frontier.empty()):
        best = frontier.get()
        if best[1] not in visited:
            visited.append(best[1])
            ans = greedyRec(best[1], numMoves+1)
            if ans[0]:
                return (True, ans[1])
    return (False, float('inf'))


if __name__ == '__main__':
    size = int(sys.argv[1])
    greedy_nodes = []
    min_nodes = []

    for x in range(NUMBER_OF_TRIALS):
        visited = []
        start = grid.LightsOutGrid(size)

        # print("--------------------")
        initState = grid.initGrid(start)
        # print('Starting state is: \n')
        # print(initState)
        new_state = initState
        # print("--------------------")

        try:
            final = greedyRec(initState, 0)
        except:
            final = (False, float('inf'))
        print(final)
        if (final[0]):
            # min_nodes.append(min_moves)
            greedy_nodes.append(final[1])
            
# export trial results to csv
df = pandas.DataFrame(data={"greedy nodes visited": greedy_nodes})
df.to_csv("./greedyresults" + str(size)+ "x" + str(size) + ".csv", sep=',', index=False)