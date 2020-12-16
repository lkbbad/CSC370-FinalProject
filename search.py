'''
Implementation of Greedy Best-First Search algorithm to solve Lights Out! game.
Authors: Lindy Bustabad and Jenny Zhong
'''

import grid
import sys
import copy
import numpy as np
import math
from queue import PriorityQueue
import pandas
from mcts import mcts


NUMBER_OF_TRIALS = 10

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
The heuristic value is the number of lights remaining on divided by 5,
since 5 is the max number of lights that can be turned off with one button
Frontier is sorted from lowest to highest by the number of lights remaining.
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

We adapted Paul Sinclair's "mcts" Python package for the basis of this implementation: https://pypi.org/project/mcts/.
'''


def mctree(mcts, state):
    curState = state
    numMoves = 0
    visited = []
    while(True):
        visited.append(curState)
        if curState.isTerminal():
            break
        action = mcts.search(initialState=curState)
        curState = curState.takeAction(action)
        mcts.add(curState)

        numMoves += 1

    print(numMoves)
    return numMoves

'''
Matplotlib setup for result charts.
'''


def make_bar_graph(greedy, aStar, mcts, title, ylabel, xlabel):
    import matplotlib.pyplot as plt

    labels = ['2', '3', '4', '5']  # , '6', '7']  # '8', '9', '10']

    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, greedy, width, label='Greedy')
    rects2 = ax.bar(x + width, aStar, width, label='A Star')
    rects3 = ax.bar(x, mcts, width, label='MCTS')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xlabel('Board Size')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.legend()
    plt.show()


def make_bar_graph_cs(mcts, c):
    import matplotlib.pyplot as plt

    labels = c  # , '4', '5', '6', '7', '8', '9', '10']

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    rects3 = ax.bar(x, mcts, width, label='MCTS')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Nodes Expanded")
    ax.set_xlabel("C")
    ax.set_title("Nodes Expanded for different C values on a 3x3 Board")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.show()


if __name__ == '__main__':
    avg_greedy = []
    avg_astar = []
    avg_mcts = []
    for size in range(2, 6):
        greedy_nodes = []
        aStar_nodes = []
        mcts_nodes = []
        for x in range(NUMBER_OF_TRIALS):
            mcts_obj = mcts(
                iterationLimit=25, explorationConstant=1 / math.sqrt(2))
            visited = []
            start = grid.LightsOutGrid(size)
            initState = grid.initGrid(start)

            try:
                final1 = greedyRec(initState, 0)
            except:
                final1 = (False, float('inf'))

            try:
                final2 = aStar(initState)
            except:
                final2 = (False, float('inf'))
            final3 = mctree(mcts_obj, initState)

            if (final1[0]):
                # min_nodes.append(min_moves)
                greedy_nodes.append(final1[1])

            if (final2[0]):
                # min_nodes.append(min_moves)
                aStar_nodes.append(final2[1])

            mcts_nodes.append(final3)
        avg_greedy.append(np.average(greedy_nodes))
        avg_astar.append(np.average(aStar_nodes))
        avg_mcts.append(np.average(mcts_nodes))

    make_bar_graph(avg_greedy, avg_astar, avg_mcts,
                   "Average Path Length to Solution", "Path Length", "Board Size")
    cs = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4]
    avg_mcts = []
    size = 3
    for c in cs:
        mcts_nodes = []
        for x in range(NUMBER_OF_TRIALS):
            mcts_obj = mcts(iterationLimit=25, explorationConstant=c)
            start = grid.LightsOutGrid(size)

            initState = grid.initGrid(start)
            final3 = mctree(mcts_obj, initState)

            mcts_nodes.append(final3)
        avg_mcts.append(np.average(mcts_nodes))
    make_bar_graph_cs(avg_mcts, cs)
