"""
Tic Tac Toe Player
"""

import math
import copy

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
    for i in range(3):
        for j in range(3):
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
    result_board = copy.deepcopy(board)
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
    # check if there are empty places on board
    board_1d = flat_board(board)
    if None not in board_1d:
        return True

    # check if there is a winner of the game
    game_winner = winner(board)
    if game_winner is not None:
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
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if current state is a terminal state
    if terminal(board):
        return None

    # Check current player
    current_player = player(board)
    # Create a dict with moves and values of the resulting states
    moves = {}

    # Find the optimal move
    # MAX player
    if current_player == X:
        for action in actions(board):
            moves[action] = min_value(result(board, action))
        optimal_move = max(moves, key=moves.get)
    # MIN player
    else:
        for action in actions(board):
            moves[action] = max_value(result(board, action))
        optimal_move = min(moves, key=moves.get)

    return optimal_move


def max_value(state):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, min_value(result(state, action)))
    return v


def min_value(state):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, max_value(result(state, action)))
    return v
