"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None
INFINITY = 1e3


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

    X starts the game.
    """
    # Count the number of X's and O's on the board
    x_moves = sum(row.count("X") for row in board)
    o_moves = sum(row.count("O") for row in board)

    # Return the next player based on who has made fewer moves
    return "O" if o_moves < x_moves else "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    An available in this game refers to a position on board where no X nor O is
    chosen yet.
    """
    action_set = set()
    for row_index, row in enumerate(board):
        for col_index, value in enumerate(row):
            if value not in (X, O):
                action_set.add((row_index, col_index))

    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.

    Cannot overwrite values.
    """
    # create a new board
    new_board = []
    for row in board:
        new_row = row.copy()
        new_board.append(new_row)

    # whose turn it is now? result will be either X or O
    current_player = player(board)

    row_index, col_index = action
    new_board[row_index][col_index] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check for consecutive positioning
    # assume square board
    BOARD_SIZE = len(board)

    # row-wise
    for each_row in board:
        if each_row.count(X) == BOARD_SIZE:
            return X
        if each_row.count(O) == BOARD_SIZE:
            return O

    # column-wise
    for col_index in range(BOARD_SIZE):
        column = [row[col_index] for row in board]
        if column.count(X) == BOARD_SIZE:
            return X
        if column.count(O) == BOARD_SIZE:
            return O

    # diagonal-wise
    # main diagonal i = j
    main_diagonal = [board[i][i] for i in range(BOARD_SIZE)]
    # anti diagonal i = len(matrix) -1 -j
    anti_diagonal = [board[BOARD_SIZE - 1 - i][i] for i in range(BOARD_SIZE)]
    if main_diagonal.count(X) == BOARD_SIZE \
            or anti_diagonal.count(X) == BOARD_SIZE:
        return X
    if main_diagonal.count(O) == BOARD_SIZE \
            or anti_diagonal.count(O) == BOARD_SIZE:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # the game is over when X or O is the winner
    if winner(board) in (X, O):
        return True

    # or if there are no EMPTY anymore
    if not any(map(lambda x : EMPTY in x, board)):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    """
    # If the board is in a terminal state, return None
    if terminal(board):
        return None

    # Determine the current player
    current_player = player(board)

    # If the current player is X, we want to maximize the score
    if current_player == X:
        # Initialize the candidate outcome to the lowest possible value
        candidate_outcome = -INFINITY
        # Loop through all possible actions on the board
        for action in actions(board):
            # Calculate the resulting board from the current action
            possible_board = result(board, action)
            # Calculate the minimum value that the opponent can get from this action
            opponents_utility = min_value(possible_board)
            # If the opponent's minimum utility is higher than the current candidate outcome,
            # update the candidate outcome and the action that produced it
            if opponents_utility > candidate_outcome:
                candidate_outcome = opponents_utility
                candidate_action = action

    # If the current player is O, we want to minimize the score
    elif current_player == O:
        # Initialize the candidate outcome to the highest possible value
        candidate_outcome = INFINITY
        # Loop through all possible actions on the board
        for action in actions(board):
            # Calculate the resulting board from the current action
            possible_board = result(board, action)
            # Calculate the maximum value that the opponent can get from this action
            opponents_utility = max_value(possible_board)
            # If the opponent's maximum utility is lower than the current candidate outcome,
            # update the candidate outcome and the action that produced it
            if opponents_utility < candidate_outcome:
                candidate_outcome = opponents_utility
                candidate_action = action

    # Return the action that produced the best outcome
    return candidate_action


def max_value(board):
    """
    The maximizing player picks action a in set of actions that
    produces the highest value of min_value(result(state, action)).
    """
    if terminal(board):
        return utility(board)

    return max(min_value(result(board, action)) for action in actions(board))


def min_value(board):
    """
    The minimizing player picks action a in set of actions that
    produces the lowest value of max_value(result(state, actions)).
    """

    v = INFINITY
    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v