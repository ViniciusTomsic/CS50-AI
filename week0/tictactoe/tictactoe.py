"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    number_X= 0
    number_O= 0
    for row in board:
        for col in row:
            if col== 'X':
                number_X += 1
            if col == 'O':
                number_O += 1
    if number_X== 0 and number_O==0:
        return 'X'
    if number_X== 5:
        return None
    if number_X > number_O:
        return 'O'
    if number_O == number_X:
        return 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions= set()
    for i in range(3):
        for j in range(3):
            if board[i][j]== None:
                actions.add((i,j))
    return actions

def result(board, action):
    for i in action:
        if i < 0:
            raise Exception
    # Return a new board state after applying the action
    if board[action[0]][action[1]] is not None:
        raise Exception('Invalid move')
    new_board = [row[:] for row in board]  # Make a deep copy of the board
    new_board[action[0]][action[1]] = player(board)  # Apply the action
    return new_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        for col in row:
            if col== None:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)== None:
        return 0
    if winner(board)== 'X':
        return 1
    else:
        return -1


def minimax1(board):
    """
    Returns the optimal action for the current player on the board.
    """
    turn= player(board)

    check_winner= winner(board)
    if check_winner is not None:
        return utility(board)

    if terminal(board) == True:
        return utility(board)

    if turn=='X':
        best_score= -float('inf')
        for action in actions(board):
            new_board = result(board,action)
            score= minimax1(new_board)
            best_score= max(score,best_score)
        return best_score
    else:
        best_score= float('inf')
        for action in actions(board):
            new_board = result(board,action)
            score= minimax1(new_board)
            best_score= min(score, best_score)
        return best_score

def minimax(board):
    if terminal(board):
        return None
    turn= player(board)

    if turn== 'X':
        best_move= None
        best_score= -float('inf')
        for action in actions(board):
            new_board = result(board,action)
            score= minimax1(new_board)
            if terminal(new_board):
                return None
            if score > best_score:
                best_score = score
                best_move= action
        return best_move

    if turn== 'O':
        best_move= None
        best_score= float('inf')
        for action in actions(board):
            new_board = result(board,action)
            score= minimax1(new_board)
            if terminal(new_board):
                return None
            if score < best_score:
                best_score = score
                best_move= action
        return best_move

