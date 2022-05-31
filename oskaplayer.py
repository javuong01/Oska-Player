## oskaplayer.py
import copy
from random import randint
from tkinter import scrolledtext




# This is the original function that starts the process. It calls minMax and returns the next best move
def oskaplayer(board, first, foresight):
    bestMove = minMax(board, first, foresight, 0, 0, first)
    return bestMove


# Below is the move generator given on piazza
"""
Copyright (C) 2022 "ECS 170 Spring 2022"
All rights reserved.
Do not distribute or open-source.
"""

from collections import defaultdict
def print_board(state):
    """
    A function to print your board
    """
    output_str = "\n"
    j=1
    output_str += '--' * len(state)
    output_str += "\n"
    for i,row in enumerate(state):
        if i<=len(state)//2 and i>0: j+=1
        else: j-=1
        output_str+= ' '*j
        for c in row:
            output_str+='|'+c
        output_str+='|\n'
        output_str+='--' * len(state)
        output_str+= "\n" 
    print(output_str)
    return output_str

def movegen(state, player):
    """
    A function to get a list of next states
    """
    
    # Find locations of all pieces and store it in dictionary
    location = defaultdict(list)
    for x,row in enumerate(state):
        for y,char in enumerate(row):
            location[char].append([x,y])
    # Go through all of player's pieces to look for possible moves.
    opponent = 'b' if player=='w' else 'w'
    next_states = []
    for piece in location[player]:
        # Make a copy of current state and remove the piece at current position.
        next_state = [[c for c in row] for row in state]
        next_state[piece[0]][piece[1]] = '-'
        next_row = piece[0]+1 if player=='w' else piece[0]-1
        if next_row<len(state) and next_row>=0:
            # Figure out what the next moves are for this current piece.
            # Two different cases: Next row is longer or it is shorter.
            if len(state[next_row])>len(state[piece[0]]):
                neighbors = [x for x in [piece[1]+1,piece[1]] if x>=0 and x<len(state[next_row])]
            else:
                neighbors = [x for x in [piece[1]-1,piece[1]] if x>=0 and x<len(state[next_row])]
            # Go through possible moves for this current piece
            for n in neighbors:
                tmp = [[c for c in row] for row in next_state]
                # If there is a opponent's piece in our way, then we need to check if we can jump
                if [next_row,n] in location[opponent]:
                    diag_row = next_row+1 if player=='w' else next_row-1
                    if diag_row<len(state) and diag_row>=0:
                        # Where are we landing?
                        # Three cases: Jumping at the middle rows, jumping into longer row, jumping into shorter row
                        if len(state[piece[0]])==len(state[diag_row]):
                            diag = piece[1]+1 if n==piece[1] else n
                        elif len(state[diag_row])>len(state[next_row]):
                            diag = n+1 if n>piece[1] else piece[1]
                        else:
                            diag = n-1 if n<piece[1] else piece[1]
                        # Now we check if the landing spot is empty.
                        if [diag_row,diag] in location['-']:
                            tmp[next_row][n] = '-'
                            tmp[diag_row][diag] = player
                            next_states.append(tmp)
                # If the next move is empty, then this move is possible.
                elif [next_row,n] in location['-']:
                    tmp[next_row][n] = player
                    next_states.append(tmp)
    # Convert all next states into correct format
    return [[''.join(row) for row in next_state] for next_state in next_states]

# turnnum goes in at 0
# don't forget to include something for turn skip if no legal moves available

#to do list: win/loss/draw/skip calculator
# static eval
# 

# This is minMax algorithm
# If the board is a winning/losing state, it will return the board given
# If the turn number is lower than the foresight, then it will generate new boards
# IF turn number is greater than foresight, then each new board is a leaf and have their boards evaluated. The best score min or max is returned
# If turn number is not greater than foresight, then each board is recursively recalling minmax to gen new boards until leaf. scores from branches propogate upwards
def minMax(board, first, foresight, turnNum, stallNum, playingFor):
    
    # checks if given board is in a win state
    if turnNum == 0:
        if first == 'w':
            prev = 'b'
        else:
            prev = 'w'
        if winEval(board, prev, turnNum) != None:
            return board

    # Move generator
    turnNum +=1
    if turnNum <= foresight:
        newBoards = movegen(board, first)

        # if not a win, but no playable move
        if not newBoards:
            if turnNum == 1:
                return board
            if stallNum == 1:
                if turnNum == 2:
                    return board
                if turnNum % 2 == 1:
                    return -9998
                else:
                    return 9998
            stallNum+=1
            if first == 'w':
                skip = 'b'
            else:
                skip = 'w'
            if turnNum == foresight:
                return "empty"
            return minMax(board, skip, foresight, turnNum, stallNum, playingFor)
    
    stallNum = 0

    # Apply state eval on each board

    # Best eval  + board = recursive function
    # if reach forseight limit or limiting move, state eval and return best move + state eval
    # else compare boards and state evals and return state eval and board
    # % 2 = 1 is max and = 0 is min


    bestScore = None

    if turnNum == foresight:
        for state in newBoards:
            score = winEval(state, turnNum)
            if score == None:
                score = stateEval(state, playingFor)

            if bestScore == None:
                bestScore = score
                continue
            if turnNum % 2 == 1:
                if score > bestScore:
                    bestScore = score
                else:
                    continue
            else:
                if score < bestScore:
                    bestScore = score
                else:
                    continue
        return bestScore


    if first == 'w':
        nextColor = 'b'
    else:
        nextColor = 'w'

    

    for state in newBoards:        
        childScore = winEval(state, turnNum)
        if childScore == None:
            childScore = minMax(state, nextColor, foresight, turnNum, stallNum, playingFor)
            if type(childScore) == str:
                childScore = stateEval(state, playingFor)
        if bestScore == None:
            if turnNum == 1:
                bestMove = copy.deepcopy(state)
            bestScore = childScore
            continue
        if turnNum % 2 == 1:
            if childScore > bestScore:
                bestScore = childScore
                if turnNum == 1:
                    bestMove = copy.deepcopy(state)
            else:
                continue
        else:
            if childScore < bestScore:
                bestScore = childScore
                if turnNum == 1:
                    bestMove = copy.deepcopy(state)
            else:
                continue
    
    if turnNum == 1:
        return bestMove
    return bestScore


# This function is the static state evaluation. 
# It favors having pieces over the halfway mark, in the enemy goal, and having less pieces than the other player.
# Being over the halfway mark, pieces gain more value. The enemy goal is worth a lot as well, but worth less with more pieces
# Being below the half line, pieces are worth even less. Pieces that have not moved are negative points. 
# The points are gathered for the side you are playing for and subtracted by the other color's points.
# Points are designed to scale for different sized boards
def stateEval(board, turn):



    wPieces = 0 
    bPieces = 0
    wGoal = 0   
    bGoal = 0
    wForward = 0
    bForward = 0
    wBack = 0
    bBack = 0
    wHome = 0
    bHome = 0
    for row in range(0, len(board)):
        for tile in range(0,len(board[row])):
            if board[row][tile] == 'w':
                if row == len(board)-1: 
                    wGoal += 1
                else:
                    wPieces += 1
                    if row >= ((len(board)-1)/2):
                        wForward += 3*row/4
                    else:
                        if row == 0:
                            wHome += 1
                        wBack += row/2
            if board[row][tile] == 'b':
                if row == 0: 
                    bGoal += 1
                else:
                    bPieces += 1
                    if row <= ((len(board)-1)/2):
                        bForward += 3*(len(board)-1-row)/4
                    else:
                        if row == len(board)-1:
                            bHome += 1
                        bBack += (len(board)-1-row)/2
    
    
        wScore = wGoal * len(board[0]) * (len(board[0])-wGoal)/len(board[0])
        wScore += (wPieces - bPieces) * len(board[0]) * 0.8
        wScore -= wHome * len(board[0])/2
        wScore += wForward + wBack

        bScore = bGoal * len(board[0]) * (len(board[0])-bGoal)/len(board[0])
        bScore += (bPieces - wPieces) * len(board[0]) * 0.8
        bScore -= bHome * len(board[0])/2
        bScore += bForward + bBack

    if turn == 'w':
        score = wScore - bScore
    else:
        score = bScore - wScore



    return score

# Takes the positions of pieces on the board and evaluates a win, loss, or draw. 
# Wins and losses are assigned points. Draws are also treated almost as unfavorable as a loss.
def winEval(board,startTurn):

    # basic win and losses from counting how many pieces on the board and goal rows
    # Correct is pieces in goal row, wrong is pieces in non-goal row
    correctB = 0
    wrongB = 0
    correctW = 0
    wrongW = 0
    for row in range(0, len(board)):
        for tile in range(0,len(board[row])):
            if board[row][tile] == 'w':
                if row == len(board)-1: 
                    correctW += 1
                else:
                    wrongW += 1
            if board[row][tile] == 'b':
                if row == 0: 
                    correctB += 1
                else:
                    wrongB += 1
    
    # tie
    if correctW > 0 and correctB > 0 and wrongW == 0 and wrongB == 0 and correctW == correctB:
            return -9998


    # all white in end goal. and if black is also in end goal, then white wins if greater pieces in end goal
    if correctW > 0 and wrongW == 0:
        if wrongB > 0 or correctW > correctB:
            if startTurn == 'w':
                return 9999
            else:
                return -9999
        else:
            if startTurn == 'w':
                return -9999
            else:
                return 9999
    # white wins is there are no more black
    if correctB + wrongB == 0:
        if startTurn == 'w':
            return 9999
        else:
            return -9999
    # white loses when there are no more white
    if correctW + wrongW == 0:
        if startTurn == 'w':
            return -9999
        else:
            return 9999
# if turn == 'b':
    if correctB > 0 and wrongB == 0:
        if wrongW > 0 or correctB > correctW:
            if startTurn == 'b':
                return 9999
            else:
                return -9999
        else:
            if startTurn == 'b':
                return -9999
            else:
                return 9999
    # black wins is there are no more white
    if correctW + wrongW == 0:
        if startTurn == 'b':
            return 9999
        else:
            return -9999
    # black loses when there are no more black
    if correctB + wrongB == 0:
        if startTurn == 'b':
            return -9999
        else:
            return 9999

    return None
