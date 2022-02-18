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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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

#a function that tracks the actions taken to reach the goal from start 
#returns a list of actions
def reconstruct_path(state , parent_action_dict) :
    actions = []
    parent , action = parent_action_dict[state]
    while parent != None:
        actions.append(action)
        parent , action = parent_action_dict[parent]
    return actions[::-1]

#in all functions i changed the early exit from what was presented in class to pass the autograder
#all use a parent - action  dictionary to track the actions
#astar also uses a cost dict


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    stack = util.Stack()
    visited = set()
    start = problem.getStartState()
    parent = {start: (None , ' ')}
    stack.push(start)

    while not stack.isEmpty():
        state = stack.pop()
        
        visited.add(state)
        if problem.isGoalState(state):
            return reconstruct_path(state  , parent)

        for next_state , action , cost in problem.expand(state):
            if next_state not in visited : #only check for visited in dfs to change the parent
                parent[next_state] = (state, action)
                stack.push(next_state)
                
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = util.Queue()
    visited = set()
    start = problem.getStartState()
    parent = {start: (None , ' ')}
    queue.push(start)
    
    while not queue.isEmpty():
        state = queue.pop()
        
        visited.add(state)
        if problem.isGoalState(state):
            return reconstruct_path(state , parent)

        for next_state , action , cost in problem.expand(state):
            #check if the next state has already been visited or if is to be visited by a faster path
            if next_state not in visited and next_state not in parent:
                parent[next_state] = (state, action)
                queue.push(next_state)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"


    #cost dict holds the actual costs
    #A state is pushed in the frontier if it hasen't been discovered yet (not in cost dict) or if its cost is less than the one already in the cost dict
    #(i decided to use the actual cost g here other than g+h after doing several tests and reading articles on A* performance and 
    #found that this way i save a lot of calculations while my results are still correct thus increasing performance)
    
    frontier = util.PriorityQueue()
    start = problem.getStartState()
    parent_action = {start : (None , ' ')}
    cost = {start : 0}
    frontier.push(start  , 0 + heuristic(start , problem))

    while not frontier.isEmpty():
        state = frontier.pop()

        if problem.isGoalState(state):
            return reconstruct_path(state , parent_action)
            
        for next_state , action , new_cost in problem.expand(state):
            total = cost[state] + new_cost
            if next_state not in cost or cost[next_state] > total: 
                cost[next_state] = total
                frontier.push(next_state , total  + heuristic(next_state , problem) )
                parent_action[next_state] = (state , action)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
