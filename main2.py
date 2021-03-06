#!/usr/bin/env python
"""
OSU Micromouse - SAC 2019
Author: Chen Liang
"""
from direction import Directions
from sensor import getSensorReading
from cell import Cell
from findPathTo import findCell
from findPathTo import findPathToCell
from movement import listMove
import operator
import time
def main():
    # STEP 1: Explore the maze
    # current position of mouse and facing direction
    #data=importStoredValue()


    startCell = Cell((0, 0))
    #data[(0,0)]=startCell
    carState = [startCell, Directions.NORTH]
    visited = []
    checkList = []
    firstRun = True
    potentialGoals = []
    while True:
        print(visited)
        visited.append(carState[0].position)
        sensorReading = getSensorReading()
        # Double check if this is correct
        isCandidate = numOfValidDirections(sensorReading) == 2
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
                    carState[0].successors[nextDir] = Cell(nextPosition)
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
        time.sleep(3)
        print ('DIR:',dirToNextCell)
        if len(dirToNextCell)!=0:
            listMove(carState, dirToNextCell)  # carState will be updated in listMove

    # STEP 2: Back to start point
    dirToStart = findPathToCell(carState[0], startCell)
    listMove(carState, dirToStart)
    # TODO: Reverse the facing direction of car? Needed?

    # STEP 3: Find the goal position
    goalCell = None
    hasFoundGoal = False
    for candidate in potentialGoals:
        candidateCell = candidate[0]
        candidateSuccessors = candidate[1]
        Level2Successors = []
        
        for direction, successor in candidateSuccessors[0].successors.items():
            if successor is not None:
                successorPos = successor.position
                if successorPos != candidateCell.position:
                    Level2Successors.append(successorPos)
        for direction, successor in candidateSuccessors[1].successors.items():
            if successor is not None and successor.position in Level2Successors:
                goalCell = candidateCell
                hasFoundGoal = True
                break
        if hasFoundGoal:
            break

    # STEP 4: Go to the goal
    dirToGoal = findPathToCell(carState[0], goalCell)
    listMove(carState,dirToGoal)
    # END

def numOfValidDirections(sensorResult):
    """
    Count the number of valid (e.g. not wall) directions for the given sensor reading
    :param sensorResult:  a list of 3 booleans in the format of [left, mid, right]
    :return:  number of valid directions
    """
    result = 0
    for dir in sensorResult:
        if not dir:
            result += 1
    return result

def dirToNewTuple(carState, index):
    """
    Given current state and direction of next movement, calculate the coordinate of next position
    :param carState: current car state, a list containing current position and facing direction
    :param index:  index of next direction, where 0 - left, 1 - front, 2 - right
    :return:  a tuple of coordinate of next position
    """
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

if __name__ == '__main__':
    main()
