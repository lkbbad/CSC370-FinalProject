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
from mcts import mcts
mcts = mcts(timeLimit=1000)

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

'''
Implementation of A* heuristic search.
The heuristic value is the number of lights remaining on divided by 5, since 5 is the max number of lights that can be turned off with one button
Frontier is sorted from lowest to highest by the number of lights remaining (not divided by 5 for the sake of code simplicity)
'''
def aStar(initial):
    frontier = []
    frontier.append(initial)
    visited_aStar = []
    
    while(len(frontier) > 0):
        frontier.sort()
        best = frontier.pop(0)
        numOn = gridSum(best)
        if numOn == 0:
            return (True, best.steps)
        visited_aStar.append(best)
        
        possibleMoves = best.possibleMoves()
        for move in possibleMoves:
            if (move not in visited_aStar) and (move not in frontier):
                frontier.append(move)
                move.steps = best.steps + 1
    
    return (False, float('inf'))

'''
The MCTS package provides a simple way of using Monte Carlo Tree Search in any perfect information domain.
'''
def mctree(state):
    curState = state
    numMoves = 0
    while(True):
        try:
            print("start")
            action = mcts.search(initialState=curState)
            print(action)
            curState = curState.takeAction(action)
            print(curState)
            numMoves += 1
            print(numMoves)
        except:
            break
    return numMoves



if __name__ == '__main__':
    #size = int(sys.argv[1])
    size = 2
    greedy_nodes = []
    aStar_nodes = []
    mcts_nodes = []

    for x in range(NUMBER_OF_TRIALS):
        visited = []
        start = grid.LightsOutGrid(size)

        # print("--------------------")
        initState = grid.initGrid(start)
        # print('Starting state is: \n')
        print(initState)
        # print("--------------------")

        try:
            final1 = greedyRec(initState, 0)
        except:
            final1 = (False, float('inf'))
        
        '''
        try:
            final2 = aStar(initState)
        except:
            final2 = (False, float('inf'))
        '''
        
        print(final1)
        #print(final2)
        final3 = mctree(initState)
        print(final3)
        print("\n")
        
        if (final1[0]):
            # min_nodes.append(min_moves)
            greedy_nodes.append(final1[1])
        '''  
        if (final2[0]):
            # min_nodes.append(min_moves)
            aStar_nodes.append(final2[1])
        '''
        mcts_nodes.append(final3)
# export trial results to csv
#df = pandas.DataFrame(data={"greedy nodes visited": greedy_nodes, "aStar nodes visited": aStar_nodes})
#df.to_csv("./searchresults" + str(size)+ "x" + str(size) + ".csv", sep=',', index=False)
df = pandas.DataFrame(data={"greedy nodes visited": greedy_nodes, "mcts nodes visited": mcts_nodes})
df.to_csv("./mctsresults" + str(size)+ "x" + str(size) + ".csv", sep=',', index=False)
