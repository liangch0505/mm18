# Micromouse 2018 OSU
# Author: Chen Liang
from direction import Directions
from sensor import getSensorReading
from cell import Cell
from findPathTo import findCell
from findPathTo import findPathToCell
from movement import listMove
import operator
import time
#from dataProcess import importStoredValue

#   complete process of exploring the maze, which includes
#   explore maze, back to start point, find and goto the
#   destination.
def main():
    # STEP 1: Explore the maze
    # current position of mouse and facing direction
    #data=importStoredValue()
    print('Program started: ')
    #time.sleep(5)

    startCell = Cell((0, 0))
    #data[(0,0)]=startCell
    carState = [startCell, Directions.NORTH]
    visited = []
    checkList = []
    firstRun = True
    potentialGoals = []
    goalFound=[]
    checkCandidate=False
    checkNumber=0
    cCell=None
    lastReading=[]
    maze={(0,0):startCell}
    while True:
        print(visited)
        visited.append(carState[0].position)
        sensorReading = getSensorReading()
        # Double check if this is correct
        isCandidate = numOfValidDirections(sensorReading) == 2
        if checkCandidate:
            if checkNumber == 0:
                checkNumber+=1
                lastReading=sensorReading
            elif checkNumber==2:
                goalFound.append(cCell)
            else:
                if lastReading==sensorReading:
                    checkNumber+=1
                else:
                    checkCandidate=False

        if isCandidate:
            checkCandidate=True
            checkNumber=0
            cCell=carState[0]

        candidateSuccessors = []
        for i in range(0, 3):
            if sensorReading[i] == False:
                nextPosition = dirToNewTuple(carState, i)
                if i == 0:
                    nextDir = Directions.LEFT[carState[1]]
                elif i == 2:
                    nextDir = Directions.RIGHT[carState[1]]
                else:
                    nextDir=carState[1]
                if nextPosition not in visited:
                    newCell=Cell(nextPosition)
                    if nextPosition in maze:
                        newCell=maze[(nextPosition)]
                    else:
                        maze[(nextPosition)]=newCell
                    carState[0].successors[nextDir] = newCell
                    carState[0].successors[nextDir].successors[Directions.REVERSE[nextDir]] = carState[0]
                    cellToCheck=carState[0].successors[nextDir]
                    addToCheckList=True
                    positionToCheck=cellToCheck.position
                    for c in checkList:
                        if c.position==positionToCheck:
                            addToCheckList=False
                            break
                    if addToCheckList and cellToCheck.position not in visited:
                        checkList.append(cellToCheck)
                    if isCandidate:
                        candidateSuccessors.append(carState[0].successors[nextDir])
                # else:
                #    if carState[0].successors[nextDir] is None:
                #        carState[0].successors[nextDir] = Cell(findCell(nextPosition,carState[0]))
        if isCandidate and len(candidateSuccessors) == 2:
            potentialGoals.append([carState[0], candidateSuccessors])
        if not firstRun and len(checkList) == 0:
            break
        for q in checkList:
            print('CheckList: ',q.position)
        firstRun = False
        nextCell = checkList.pop()
        dirToNextCell = findPathToCell(carState[0], nextCell)
        print('Next pos: ',nextCell.position)
        print('Steps: ',dirToNextCell)
        #time.sleep(3)
        print ('DIR:',dirToNextCell)
        if len(dirToNextCell)!=0:
            listMove(carState, dirToNextCell)  # carState will be updated in listMove


    # STEP 2: Back to start point
    dirToStart = findPathToCell(carState[0], startCell)
    listMove(carState, dirToStart)
    printTree(startCell)
    # TODO: Reverse the facing direction of car? Needed?

    # STEP 3: Find the goal position
    # goalCell = None
    # hasFoundGoal = False
    # for candidate in potentialGoals:
    #     candidateCell = candidate[0]
    #     candidateSuccessors = candidate[1]
    #     Level2Successors = []
    #     for c in candidateSuccessors:
    #         for direction, successor in c.successors.items():
    #             if successor is not None:
    #                 successorPos = successor.position
    #                 if successorPos != candidateCell.position:
    #                     Level2Successors.append(successorPos)
    #     for direction, successor in candidateSuccessors[1].successors.items():
    #         if successor is not None and successor.position in Level2Successors:
    #             goalCell = candidateCell
    #             hasFoundGoal = True
    #             break
    #     if hasFoundGoal:
    #         break

    # STEP 4: Go to the goal
    dirToGoal = findPathToCell(carState[0], goalFound[0])
    listMove(carState,dirToGoal)
    time.sleep(5)
    # END


# count the number of valid directions (e.g. not wall)
# @param    sensorResult - sensor readings, a list of length 3
# @return   number of valid directions - an int
def numOfValidDirections(sensorResult):
    result = 0
    for dir in sensorResult:
        if not dir:
            result += 1
    return result


# return the coordinate of next tuple in the given direction
# based on the current position
# @param    carState - a list containing current position and
#           facing direction
# @param    index - an int indicating the next direction, where
#           0 is left, 1 is front, 2 is right
# @return   a tuple indicating the position of next cell
def dirToNewTuple(carState, index):
    numbers = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    addon = 0
    if carState[1] == Directions.EAST:
        addon = 1
    elif carState[1] == Directions.SOUTH:
        addon = 2
    elif carState[1] == Directions.WEST:
        addon = 3
    result=tuple(map(operator.add, carState[0].position, numbers[(index + addon) % 4]))
    print(result)
    return result
def printTree(startCell):
    
    successor=[]
    successor.append(startCell)
    visited=[]
    
    for e in successor:
        print('@Cell ',e.position)
        if e in visited:
            continue
        visited.append(e)
        for dir,c in e.successors.items():
            if c is not None:
                print('   ',dir,' ',c.position)
                successor.append(c)
            else:
                print('   ', dir, ' None')
if __name__ == '__main__':
    main()
