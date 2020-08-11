# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newGhostPos = successorGameState.getGhostPositions()
        returnScore=0
        width=newFood.width
        height=newFood.height
       
        xy1 = newPos
        maxGDis=0
        for pos in newGhostPos:
          xy2 = pos
          if ((abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1]))>maxGDis):
            maxGDis=abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
        
        returnScore+=successorGameState.getScore()
        minFoodList=[];
        for x in range(width):
          for y in range(height):
            if newFood[x][y]:
              xy2=(x, y)
              minFoodList+=[(abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1]))]
        if minFoodList!=[]:
          minFood=min(minFoodList)
        else:
          minFood=0
       
        returnScore-=(minFood)
        scared=False
        if (min(newScaredTimes)>0):
          scared=True
        if not scared:
          returnScore+=maxGDis
          for pos in newGhostPos:
            if (pos ==newPos):
              returnScore=-100000
          
        
        return returnScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        actionDic={}
        MinMaxList=[]
        playerNum = gameState.getNumAgents()
        searchLimit=self.depth*playerNum
        nextAction = gameState.getLegalActions(0)
        for action in nextAction:
          state = gameState.generateSuccessor(0, action)
          MaxVals = MinMaxFunc(state, 1, playerNum, searchLimit, self.evaluationFunction)
          MinMaxList+=[MaxVals]
          actionDic[MaxVals] = action
        return actionDic[max(MinMaxList)]


def MinMaxFunc(gameState, searchCount, playerNum, searchLimit, evalFunc):
    if gameState.isLose() or gameState.isWin() or (searchCount==searchLimit):
      return evalFunc(gameState)
    agentNum=searchCount%playerNum
    if agentNum==0:
      MaxVal = float("-inf")
      nextActions = gameState.getLegalActions(0)
      for action in nextActions:
        nextState = gameState.generateSuccessor(0,action)
        MaxVal = max(MaxVal, MinMaxFunc(nextState, searchCount+1, playerNum, searchLimit, evalFunc))
      return MaxVal
    else:
      MinVal = float("inf")
      nextActions = gameState.getLegalActions(agentNum)
      for action in nextActions:
        nextState = gameState.generateSuccessor(agentNum ,action)
        MinVal = min(MinVal, MinMaxFunc(nextState, searchCount+1, playerNum, searchLimit, evalFunc))
      return MinVal




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        actionDic={}
        MinMaxList=[]
        playerNum = gameState.getNumAgents()
        searchLimit=self.depth*playerNum
        nextAction = gameState.getLegalActions(0)
        alpha=float("-inf")
        for action in nextAction:
          state = gameState.generateSuccessor(0, action)
          MaxVals = MinMaxWithPruning(state, 1, playerNum, searchLimit, self.evaluationFunction,alpha, float("inf"))
          MinMaxList+=[MaxVals]
          actionDic[MaxVals] = action
          alpha=max(alpha, MaxVals)
        return actionDic[max(MinMaxList)]


def MinMaxWithPruning(gameState, searchCount, playerNum, searchLimit, evalFunc, alpha, beta):
    if gameState.isLose() or gameState.isWin() or (searchCount==searchLimit):
      return evalFunc(gameState)
    agentNum=searchCount%playerNum
    if agentNum==0:
      MaxVal = float("-inf")
      nextActions = gameState.getLegalActions(0)
      for action in nextActions:
        nextState = gameState.generateSuccessor(0,action)
        MaxVal = max(MaxVal, MinMaxWithPruning(nextState, searchCount+1, playerNum, searchLimit, evalFunc,alpha, beta))
        if MaxVal>beta:
          return MaxVal
        alpha=max(alpha, MaxVal)
      return MaxVal
    else:
      MinVal = float("inf")
      nextActions = gameState.getLegalActions(agentNum)
      for action in nextActions:
        nextState = gameState.generateSuccessor(agentNum ,action)
        MinVal = min(MinVal, MinMaxWithPruning(nextState, searchCount+1, playerNum, searchLimit, evalFunc,alpha, beta))
        if MinVal<alpha:
          return MinVal
        beta=min(beta, MinVal)
      return MinVal
      

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        actionDic={}
        MinMaxList=[]
        playerNum = gameState.getNumAgents()
        searchLimit=self.depth*playerNum
        nextAction = gameState.getLegalActions(0)
        for action in nextAction:
          state = gameState.generateSuccessor(0, action)
          MaxVals = ExpecFunc(state, 1, playerNum, searchLimit, self.evaluationFunction)
          MinMaxList+=[MaxVals]
          actionDic[MaxVals] = action
        return actionDic[max(MinMaxList)]


def ExpecFunc(gameState, searchCount, playerNum, searchLimit, evalFunc):
    if gameState.isLose() or gameState.isWin() or (searchCount==searchLimit):
      return evalFunc(gameState)
    agentNum=searchCount%playerNum
    if agentNum==0:
      MaxVal = float("-inf")
      nextActions = gameState.getLegalActions(0)
      for action in nextActions:
        nextState = gameState.generateSuccessor(0,action)
        MaxVal = max(MaxVal, ExpecFunc(nextState, searchCount+1, playerNum, searchLimit, evalFunc))
      return MaxVal
    else:
      MinVal = 0
      count=0
      nextActions = gameState.getLegalActions(agentNum)
      for action in nextActions:
        nextState = gameState.generateSuccessor(agentNum ,action)
        MinVal += ExpecFunc(nextState, searchCount+1, playerNum, searchLimit, evalFunc)
        count+=1
      return float(MinVal)/float(count)
      
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    GhostPos = currentGameState.getGhostPositions()
    returnScore=0
    width=Food.width
    height=Food.height
    if currentGameState.isWin():
      return 9999999
    if currentGameState.isLose():
      return -9999999   
    xy1 = Pos
    maxGDis=0
    for pos in GhostPos:
      xy2 = pos
      if ((abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1]))>maxGDis):
        maxGDis=abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])   
    returnScore+=currentGameState.getScore()
    minFoodList=[];
    for x in range(width):
      for y in range(height):
        if Food[x][y]:
          xy2=(x, y)
          minFoodList+=[(abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1]))]
    if minFoodList!=[]:
      minFood=min(minFoodList)
    else:
      minFood=0
      
    returnScore+=10/float(minFood)
    scared=False
    if (min(ScaredTimes)>0):
      scared=True
      returnScore+=100

    if not scared:
      returnScore+=float(maxGDis)/float(10)
          
        
    return returnScore
    
# Abbreviation
better = betterEvaluationFunction

