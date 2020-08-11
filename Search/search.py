# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    start=problem.getStartState()
    successors= problem.getSuccessors(start)
    closed= set()
    closed.add(start)
    fringe=Stack()
    path=[]
    moveStack=Stack()
    if problem.isGoalState(start) or len(successors)==0:
        return []
    for x in successors:
        fringe.push(x)
    while (not fringe.isEmpty()):
        curNode=fringe.pop()
        
        if problem.isGoalState(curNode[0]):
            path.append(curNode[1])
            while not moveStack.isEmpty():
                pathNode=moveStack.pop()
                path.insert(0,pathNode[1])
            return path
            break
        else:
            nodeSuccessors= problem.getSuccessors(curNode[0])
            closed.add(curNode[0])
            nodeCount=0
            for nodes in nodeSuccessors:
                if (not (nodes[0] in closed)):
                    nodeCount+=1
                    fringe.push(nodes)
            if nodeCount==0:
                haveChildren=False
                while (not moveStack.isEmpty()) and (not haveChildren):
                    backNode=moveStack.pop()
                    backSuccessors=problem.getSuccessors(backNode[0])
                    for nodes in backSuccessors:
                        if not(nodes[0] in closed):
                            haveChildren=True
                            moveStack.push(backNode)
                            break
                if not haveChildren:
                    if fringe.isEmpty():               
                        return []
            else:
                moveStack.push(curNode)

                
    return []


            

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    from util import Queue
    from util import Stack
    start=problem.getStartState()
    successors= problem.getSuccessors(start)
    closed= set()
    closed.add(start)
    fringe=Queue()
    path=[]
    moveStack=Stack()
    successorDic={}   
    if problem.isGoalState(start) or len(successors)==0:
        return []
    for x in successors:
        fringe.push(x)
        closed.add(x[0])
    while (not fringe.isEmpty()):
        curNode=fringe.pop()
        if problem.isGoalState(curNode[0]):
            
            path.append(curNode[1])
            "closed.add(curNode[0])"
            while not moveStack.isEmpty():
                pathNode=moveStack.pop()
                pathSuccessors=successorDic[pathNode[0]]
                for nodes in pathSuccessors:
                    if nodes[0] in closed and nodes==curNode:
                        path.insert(0,pathNode[1])
                        curNode=pathNode
            return path
            break
        else:
            nodeSuccessors= problem.getSuccessors(curNode[0])
            "closed.add(curNode[0])"
            nodeCount=0
            for nodes in nodeSuccessors:
                if (not (nodes[0] in closed)):
                    nodeCount+=1
                    fringe.push(nodes)
                    closed.add(nodes[0])
            if nodeCount!=0:
                moveStack.push(curNode)
                successorDic[curNode[0]]=nodeSuccessors

                
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    from util import Stack
    start=problem.getStartState()
    successors= problem.getSuccessors(start)
    closed= set()
    closed.add(start)
    fringe=PriorityQueue()
    path=[]
    moveStack=Stack()
    successorDic={}   
    distance={}
    distance[start]=0
    if problem.isGoalState(start) or len(successors)==0:
        return []
    for x in successors:
        fringe.push(x,x[2])
        distance[x[0]]=x[2]
        closed.add(x[0])
    while (not fringe.isEmpty()):
        curNode=fringe.pop()
        if problem.isGoalState(curNode[0]):
            path.append(curNode[1])
            "closed.add(curNode[0])"
            while not moveStack.isEmpty():
                pathNode=moveStack.pop()
                pathSuccessors=successorDic[pathNode[0]]
                for nodes in pathSuccessors:
                    if nodes[0] in closed and nodes==curNode:
                        path.insert(0,pathNode[1])
                        curNode=pathNode
            return path
            break
        else:
            nodeSuccessors= problem.getSuccessors(curNode[0])
            closed.add(curNode[0])
            nodeCount=0
            for nodes in nodeSuccessors:
                if (not (nodes[0] in closed)):
                    nodeCount+=1
                    closed.add(nodes[0])
                    fringe.push(nodes,nodes[2]+distance[curNode[0]])
                    distance[nodes[0]]=nodes[2]+distance[curNode[0]]
                elif (distance[nodes[0]]>(nodes[2]+distance[curNode[0]])):
                    distance[nodes[0]]=nodes[2]+distance[curNode[0]]
                    nodeCount+=1
                    fringe.push(nodes,nodes[2]+distance[curNode[0]])
            if nodeCount!=0:
                moveStack.push(curNode)
                successorDic[curNode[0]]=nodeSuccessors

                
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    from util import PriorityQueueWithFunction
    from util import Stack
    start=problem.getStartState()
    successors= problem.getSuccessors(start)
    closed= set()
    closed.add(start)
    fringe=PriorityQueue()
    path=[]
    moveStack=Stack()
    successorDic={}   
    distance={}
    distance[start]=0
    if problem.isGoalState(start) or len(successors)==0:
        return []
    for x in successors:
        fringe.push(x,x[2]+heuristic(x[0],problem))
        distance[x[0]]=x[2]
        closed.add(x[0])
    while (not fringe.isEmpty()):
        curNode=fringe.pop()
        if problem.isGoalState(curNode[0]):
            path.append(curNode[1])
            "closed.add(curNode[0])"
            while not moveStack.isEmpty():
                pathNode=moveStack.pop()
                pathSuccessors=successorDic[pathNode[0]]
                for nodes in pathSuccessors:
                    if nodes[0] in closed and nodes==curNode:
                        path.insert(0,pathNode[1])
                        curNode=pathNode
            return path
            break
        else:
            nodeSuccessors= problem.getSuccessors(curNode[0])
            closed.add(curNode[0])
            nodeCount=0
            for nodes in nodeSuccessors:
                if (not (nodes[0] in closed)):
                    nodeCount+=1
                    closed.add(nodes[0])
                    fringe.push(nodes,nodes[2]+distance[curNode[0]]+heuristic(nodes[0], problem))
                    distance[nodes[0]]=nodes[2]+distance[curNode[0]]
                elif (distance[nodes[0]]>(nodes[2]+distance[curNode[0]])):
                    distance[nodes[0]]=nodes[2]+distance[curNode[0]]
                    nodeCount+=1
                    fringe.push(nodes,nodes[2]+distance[curNode[0]]+heuristic(nodes[0],problem))
            if nodeCount!=0:
                moveStack.push(curNode)
                successorDic[curNode[0]]=nodeSuccessors

                
    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
