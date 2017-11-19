# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def mySearch(problem, frontier, explored):
    # while not frontier.isEmpty():
    #     current = frontier.pop()
    #     if problem.isGoalState(current[0]):
    #         return current[2]
    #     if (current[0] not in explored):
    #         explored.append(current[0])
    #     successors = problem.getSuccessors(current[0])
    #     for i in successors:
    #         if i[0] not in explored:
    #             frontier.push((i[0], i[1], current[2] + [i[1]]))
    # return []

    while not frontier.isEmpty():
        current = frontier.pop()
        for position, direction, _ in problem.getSuccessors(current[0]):
            if position not in explored:
                if problem.isGoalState(position):
                    return current[1] + [direction]
                frontier.push((position, current[1]+[direction], current[2]+[position]))
                current[2].append(position)
    return []


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    frontier = util.Stack()
    explored = []
    initial = (problem.getStartState(), [],[])
    frontier.push(initial)

    while not frontier.isEmpty():
    	current = frontier.pop()
    	if problem.isGoalState(current[0]):
    		return current[2]
    	if current[0] not in explored:
    		explored.append(current[0])
    	successors = problem.getSuccessors(current[0])
    	for i in successors:
    		if i[0] not in explored:
    			frontier.push((i[0], i[1], current[2] + [i[1]]))
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    explored = []
    initial = (problem.getStartState(), [],[])
    # explored.add(initial[0])
    explored.append(initial[0])
    frontier.push(initial)

    while not frontier.isEmpty():
        current = frontier.pop()
        if problem.isGoalState(current[0]):
            return current[2]
        successors = problem.getSuccessors(current[0])
        for i in successors:
            if i[0] not in explored:
                # explored.add(i[0])
                explored.append(i[0])
                frontier.push((i[0], i[1], current[2] + [i[1]]))

    return []


def uniformCostSearch(problem):
    frontier = util.PriorityQueue()
    nodes = {}
    explored = []
    explored.append(problem.getStartState())

    for s in problem.getSuccessors(problem.getStartState()):
        actions = []
        actions.append(s[1])
        cost = problem.getCostOfActions(actions)
        frontier.push(s[0], cost)
        nodes[s[0]] = [[s[1]], cost, [s[1]]]

    while not frontier.isEmpty():
        current = frontier.pop()
        if current not in explored:
            explored.append(current)
        path = nodes[current][0]
        if problem.isGoalState(current):
            return path
        successors = problem.getSuccessors(current)
        for i in successors:
            if i[0] not in explored:
                priority = problem.getCostOfActions(path+[i[1]])
                frontier.update(i[0], priority)
                if i[0] in nodes.keys():
                    if priority < nodes[i[0]][1]:
                        nodes[i[0]] = [path+[i[1]], priority, i[1]]
                else:
                    nodes[i[0]] = [path+[i[1]], priority, i[1]]

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    nodes = {}
    explored = []
    explored.append(problem.getStartState())

    for s in problem.getSuccessors(problem.getStartState()):
        actions = []
        actions.append(s[1])
        cost = problem.getCostOfActions(actions) + heuristic(s[0], problem)
        frontier.push(s[0], cost)
        nodes[s[0]] = [[s[1]], cost, [s[1]]]

    while not frontier.isEmpty():
        current = frontier.pop()
        if current not in explored:
            explored.append(current)
        path = nodes[current][0]
        if problem.isGoalState(current):
            return path
        successors = problem.getSuccessors(current)
        for i in successors:
            if i[0] not in explored:
                priority = problem.getCostOfActions(path+[i[1]]) + heuristic(i[0], problem)
                frontier.update(i[0], priority)
                if i[0] in nodes.keys():
                    if priority < nodes[i[0]][1]:
                        nodes[i[0]] = [path+[i[1]], priority, i[1]]
                else:
                    nodes[i[0]] = [path+[i[1]], priority, i[1]]

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
