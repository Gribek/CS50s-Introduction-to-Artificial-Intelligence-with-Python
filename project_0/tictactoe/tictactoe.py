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
    # count x and o in the board
    board_1d = flat_board(board)
    number_of_x = board_1d.count(X)
    number_of_o = board_1d.count(O)

    # return which player's turn it is
    if number_of_x > number_of_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check if action is valid
    if board[action[0]][action[1]] is not None:
        raise Exception('Not a valid action')

    # return new board with player's move marked on it
    result_board = board[:]
    player_mark = player(board)
    result_board[action[0]][action[1]] = player_mark
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check if there is no empty places on board
    board_1d = flat_board(board)
    if None not in board_1d:
        return True

    # check winning conditions
    # winning rows
    winning_threes = board[:]
    # winning columns
    for i in range(3):
        three = []
        for row in board:
            three.append(row[i])
        winning_threes.append(three)
    # winning diagonals
    winning_threes.append([board[0][0], board[1][1], board[2][2]])
    winning_threes.append([board[0][2], board[1][1], board[2][0]])

    # check for three in a row
    for three in winning_threes:
        three_set = set(three)
        if len(three_set) == 1 and None not in three_set:
            return True

    return False


def flat_board(board):
    board_1d = [elem for row in board for elem in row]
    return board_1d


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
