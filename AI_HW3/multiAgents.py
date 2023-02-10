from util import manhattanDistance
from game import Directions
import random, util
from game import Agent
import math

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        '''
        Three functions:
        minimax:  If runs recursion depth * agentNum times or win/lose state:
                    Return score of state
                  Else:
                    Determine whether goes recursive to maxAgent or minAgent depending on agentIndex
                    0: go recursion of maxAgent
                    others: go recursion of minAgent

        maxAgent: Find maxScore, bestAction among scores got from taking each legal actions by calling minimax with nextAgent 
                  and what depth it would be when going to nextAgent 
                  Return maxScore and bestAction

        minAgent: Find minScore, bestAction among scores got from taking each legal actions by calling minmax with nextAgent 
                  and what depth it would be when going to nextAgent
                  Return minScore and bestAction

        Then call maxAgent in getAction() with parameters of gameState, agentIndex = 0, and currentDepth = 0
        Only return bestAction returned from maxAgent function
        '''
        def minimax(state, agentIndex, currentDepth):
            if currentDepth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            elif agentIndex == 0:
                bestScore, bestAction = maxAgent(state, agentIndex, currentDepth)  
                return bestScore           
            else:
                bestScore, bestAction = minAgent(state, agentIndex, currentDepth)  
                return bestScore 

        def maxAgent(state, agentIndex, currentDepth):
            legalMoves = state.getLegalActions(agentIndex)
            scores = [(minimax(state.getNextState(agentIndex, move), agentIndex+1, currentDepth), move) for move in legalMoves]
            bestScore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices)
            return scores[chosenIndex]
        
        def minAgent(state, agentIndex, currentDepth):      
            scores = []
            legalMoves = state.getLegalActions(agentIndex)
            if agentIndex == gameState.getNumAgents() - 1:
                scores = [(minimax(state.getNextState(agentIndex, move), 0, currentDepth+1), move) for move in legalMoves]
            else:
                scores = [(minimax(state.getNextState(agentIndex, move), agentIndex+1, currentDepth), move) for move in legalMoves]
            bestScore = min(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices)
            return scores[chosenIndex]
        
        bestScore, bestAction = maxAgent(gameState, 0, 0)
        return bestAction
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        '''
        Three functions:
        alphaBeta: If runs recursion depth * agentNum times or win/lose state:
                      Return score of state
                   Else:
                      Determine whether goes recursive to maxAgent or minAgent depending on agentIndex
                      0: go recursion of maxAgent
                    others: go recursion of minAgent

        maxAgent: Initialize value to -inf
                  Find the scores of taking each legal action by calling alphaBeta with nextAgent 
                  and what depth it would be when going to nextAgent within a for loop
                  In the loop:
                    Update value if score > value then compare value to beta
                    If value >= beta, no need to look for childStates anymore because the previous 
                    minAgent is looking for childState value smaller than its beta
                    Thus could directly return value because it won't be chosen by previous minAgent
                  Return maxScore and bestAction

        minAgent: Initialize value to inf
                  Find the scores of taking each legal action by calling alphaBeta with nextAgent 
                  and what depth it would be when going to nextAgent within a for loop
                  In the loop:
                    Update value if score < value then compare value to alpha
                    If value <= alpha, no need to look for childStates anymore because the previous 
                    maxAgent is looking for childState value bigger than its alpha
                    Thus could directly return value because it won't be chosen by previous maxAgent
                  Return minScore and bestAction

        Then call maxAgent in getAction() with parameter of gameState, agentIndex = 0,
        currentDepth = 0, alpha initialized to -inf and beta initialized to inf
        Only return bestAction returned from maxAgent function
        '''
        def alphaBeta(state, agentIndex, currentDepth, alpha, beta):
            if currentDepth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            elif agentIndex == 0:
                bestScore, bestAction = maxAgent(state, agentIndex, currentDepth, alpha, beta)  
                return bestScore           
            else:
                bestScore, bestAction = minAgent(state, agentIndex, currentDepth, alpha, beta)  
                return bestScore 

        def maxAgent(state, agentIndex, currentDepth, alpha, beta):
            legalMoves = state.getLegalActions(agentIndex)
            scores = []
            value = -math.inf
            for move in legalMoves:
                nextValue = alphaBeta(state.getNextState(agentIndex, move), agentIndex+1, currentDepth, alpha, beta)
                scores.append((nextValue, move))
                value = max(value, nextValue)
                if value > beta:
                    return (value, move)   #for min agent, min(v, successor, alpha, beta) = v if value > beta
                alpha = max(alpha, value)
                
            bestScore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices)
            return scores[chosenIndex]
        
        def minAgent(state, agentIndex, currentDepth, alpha, beta):
            
            legalMoves = state.getLegalActions(agentIndex)
            scores = []
            value = math.inf
            for move in legalMoves:
                nextValue = 0
                if agentIndex == gameState.getNumAgents() - 1:
                    nextValue = alphaBeta(state.getNextState(agentIndex, move), 0, currentDepth+1, alpha, beta)
                else:
                    nextValue = alphaBeta(state.getNextState(agentIndex, move), agentIndex+1, currentDepth, alpha, beta)

                scores.append((nextValue, move))
                value = min(value, nextValue)
                if value < alpha:
                    return (value, move)
                beta = min(beta, value)

            bestScore = min(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices)
            return scores[chosenIndex]

        alpha = -math.inf
        beta = math.inf
        bestScore, bestAction = maxAgent(gameState, 0, 0, alpha, beta)
        return bestAction
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        '''
        Three functions:
        expectimax: If runs recursion depth * agentNum times or win/lose state:
                      Return score of state
                    Else:
                      Determine whether goes recursive to maxAgent or minAgent depending on agentIndex
                      0: go recursion of maxAgent
                      others: go recursion of minAgent

        maxAgent: Find maxScore, bestAction by calling expectimax with nextAgent 
                  and the depth it would be when going to nextAgent
                  Return maxScore and bestAction

        randomAgent: Find score, action of taking each legal action by calling expectimax with nextAgent 
                     and what depth it would be when going to nextAgent
                     Take average of the scores (because it chooses uniformly at random => equal probability of 1/len(scores))
                     Return a random action and the expectedScore

        Then call maxAgent in getAction() with parameter of gameState, agentIndex = 0, and currentDepth = 0
        Only return bestAction returned from maxAgent function
        '''
        def expectimax(state, agentIndex, currentDepth):
            if currentDepth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            elif agentIndex == 0:
                bestScore, bestAction = maxAgent(state, agentIndex, currentDepth)  
                return bestScore           
            else:
                bestScore, bestAction = randomAgent(state, agentIndex, currentDepth)  
                return bestScore 

        def maxAgent(state, agentIndex, currentDepth):
            legalMoves = state.getLegalActions(agentIndex)
            scores = [(expectimax(state.getNextState(agentIndex, move), agentIndex+1, currentDepth), move) for move in legalMoves]
            bestScore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices)
            return scores[chosenIndex]
        
        def randomAgent(state, agentIndex, currentDepth):
            scores = []
            legalMoves = state.getLegalActions(agentIndex)
            if agentIndex == gameState.getNumAgents() - 1:
                scores = [(expectimax(state.getNextState(agentIndex, move), 0, currentDepth+1), move) for move in legalMoves]
            else:
                scores = [(expectimax(state.getNextState(agentIndex, move), agentIndex+1, currentDepth), move) for move in legalMoves]
    
            expectedScore = sum(scores[i][0] for i in range(len(scores))) / len(scores)
            chosenMove = random.choice(legalMoves)
            return (expectedScore, chosenMove)
        
        bestScore, bestAction = maxAgent(gameState, 0, 0)
        return bestAction
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    '''
    I consider five parameter: orignal score, capsule distance, food distance, ghost distance, scardGhost num

    Original score: score get from evaluation function
    Capsule score: for each capsule left, consider if pacman is the closest to the capsule
                   if yes, add 1/dist to capsule_score, else no
                   if capsule is at the same position of pacman, then add 500 to capsule_score
    Food score: consider the closest food distance, the closer to the food, the higher for the score, so I use 
                1/closestFoodDist to be food_score, if minimum distance of not scared ghost and closest food < 2
                then set food_score to 0 
    Ghost score: consider how close is pacman and not scared ghost, if too close, score higher, if not too close score lower,
                 so I add 1/ghostDist to ghost_score for each not scared ghost
                 if ghost is at the same position of pacman, then add 100 to ghost_score
    Ghost scared score: consider how close is pacman and scared ghost, if too close, score higher, if not too close score lower,
                        so I add 1/ghostDist to scaredGhost_score for each scard ghost
                        if scaredghost is at the same position of pacman, then add 500 to scaredGhost_score
    
    Give each score a coefficient to make a linear combination => [+1, +1000, +10, -4, +2500] to get higher score from the game
    The result of coefficients gets the highest through trying different coefficients for linear combinations
    '''
    pacmanPos = currentGameState.getPacmanPosition()
    ghostsPos = currentGameState.getGhostPositions()
    capsulesPos = currentGameState.getCapsules()
    foodPos = currentGameState.getFood().asList()
    
    ghostDist = [manhattanDistance(pacmanPos, ghostPos) for ghostPos in ghostsPos]
    capsuleToGhost = [ [manhattanDistance(ghostPos, capsulePos) for ghostPos in ghostsPos] for capsulePos in capsulesPos]
    capsuleDist = [manhattanDistance(pacmanPos, capsulePos) for capsulePos in capsulesPos]

    # five parameter: score, capsule, food, ghost, scaredGhost_score
    game_score = 0
    capsule_score = 0
    food_score = 0
    ghost_score = 0
    scaredGhost_score = 0

    game_score = currentGameState.getScore()
     
    for i in range(len(capsuleDist)):
        if capsuleDist[i] < min(capsuleToGhost[i]):
            capsule_score += 1.0/capsuleDist[i] if capsuleDist[i] > 0 else 500

    closestFoodDist = min([manhattanDistance(pacmanPos, food) for food in foodPos]) if len(foodPos) > 0 else math.inf
    food_score = 1.0 / closestFoodDist

    minGhostDist = math.inf
    ghostStates = currentGameState.getGhostStates()
    ghostScared = [True if ghostState.scaredTimer > 0 else False for ghostState in ghostStates]
    for i in range(len(ghostDist)):
        if ghostScared[i]:
            scaredGhost_score += 1.0/ghostDist[i] if ghostDist[i] > 0 else 500
        else:
            ghost_score += 1.0/ghostDist[i] if ghostDist[i] > 0 else 100
            minGhostDist = min(ghostDist[i], minGhostDist)

    if minGhostDist < 2:
        food_score = 0

    totalScore = game_score + capsule_score*1000 + food_score*10 + ghost_score*(-4) + scaredGhost_score*2500
    return totalScore
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
