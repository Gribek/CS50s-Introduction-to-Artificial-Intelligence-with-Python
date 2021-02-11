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
    possible_actions = set()
    for i in range(2):
        for j in range(2):
            if board[i][j] is None:
                possible_actions.add((i, j))
    return possible_actions


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
    # get list of winning rows
    threes = winning_threes(board)

    # check for the winner
    for three in threes:
        if None in three:
            continue
        if len(set(three)) == 1:
            return three[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check if there is no empty places on board
    board_1d = flat_board(board)
    if None not in board_1d:
        return True

    # get list of vertical, horizontal and diagonal rows
    threes = winning_threes(board)

    # check for three in a row
    for three in threes:
        if None in three:
            continue
        if len(set(three)) == 1:
            return True

    return False


def winning_threes(board):
    # winning rows
    threes = board[:]
    # winning columns
    for i in range(3):
        three = []
        for row in board:
            three.append(row[i])
        threes.append(three)
    # winning diagonals
    threes.append([board[0][0], board[1][1], board[2][2]])
    threes.append([board[0][2], board[1][1], board[2][0]])
    return threes


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
