"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def print_board(board):
    for row in board:
        print(row)

win_states = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1],
                [1, 0, 0, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1],
                [0, 0, 1, 0, 1, 0, 1, 0, 0]]

win_states_mask = []


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
    o_count = 0
    x_count = 0

    for row in board:
        for cell in row:
            if cell == O:
                o_count += 1
            elif cell == X:
                x_count += 1

    if x_count == o_count:     # Since X starts, o_count will always match x_count on O's turn
        return X               # at the start, they're both at 0, so X will go first
    else:                      # Otherwise, x_count has the be bigger in which case it must be O's turn
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    choices = set()
   
    for row in range(0, 3):
        for cell in range(0, 3):
            if board[row][cell] == EMPTY:
                choices.add((row, cell))
    
    return choices


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action:
        (row, col) = action
    
        if board[row][col] != EMPTY:
            raise Exception
        else:
            board_cpy = copy.deepcopy(board)
            board_cpy[row][col] = player(board)
        
        return board_cpy
    else:
        raise Exception

# convert board to an array size 9 of 0s, 1s and 2s
def convert_board(board):
    new_board = []
    for row in board:
        for col in row:
            if col == EMPTY:
                new_board.append(0)
            elif col == X:
                new_board.append(1)
            else:
                new_board.append(2)
    return new_board

# will generate a bit mask for either 1s (Xs) or 2s (Os)
def get_mask(number, board):
    mask_int = 0

    for i in range(len(board)):
        if board[i] != number:
            continue
        n = len(board) - i - 1
        x = 1 << n
        mask_int |= x
    return mask_int


def winner(board):    
    conv_board = convert_board(board)

    # generate a bit mask for Xs and Os
    board_x = get_mask(1, conv_board)
    board_o = get_mask(2, conv_board)
    
    # generates mask for each of the win states, add them to the array win_states_mask
    if len(win_states_mask) == 0:
        for i in range(len(win_states)):
            mask = get_mask(1, win_states[i])
            win_states_mask.append(mask)

    #traverse through the win state masks, and compare them to the generated mask for X and O
    for i in range(len(win_states_mask)):
        mask = win_states_mask[i]
        mask_b_x = mask & board_x
        mask_b_o = mask & board_o

        # if a win state matches with either mask, we have a winner
        if mask == mask_b_x:
            return X
        elif mask == mask_b_o:
            return O
    
    # if none match return None
    return None
      

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # either somebody won
    if winner(board) == X or winner(board) == O:
        return True
    
    # checking if board still has empty spaces
    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

# convert a board into an integer, for example a converted board [2, 1, 0, 0, 2, 1, 0, 0, 0]
#   would become 210021000
def board_key_gen(board):
    key = 0
    for i in range(0, 9):
        key += math.pow(10, i) * board[i]
    return int(key)

# create a dictionary to store board keys and their respective values
cache_max = {}
def max_val(state):
    
    # if a particular board is found, simply return its value
    board_key = board_key_gen(convert_board(state))
    if cache_max and board_key in cache_max.keys():
        return cache_max[board_key]
    
    v = -math.inf
    if terminal(state):
        return utility(state)
    for action in actions(state):
        v = max(v, min_val(result(state, action)))
    
    # else calculate the board's value and store 
    cache_max[board_key] = v
    return v

cache_min = {}
def min_val(state):

    board_key = board_key_gen(convert_board(state))
    if cache_min and board_key in cache_min.keys():
        return cache_min[board_key]

    v = math.inf
    if terminal(state):
        return utility(state)
    for action in actions(state):
        v = min(v, max_val(result(state, action)))
    
    cache_min[board_key] = v
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        temp = -1               
        temp_action = None
        for action in actions(board):
            best = min_val(result(board, action))
            
            if temp <= best:
                temp = best
                temp_action = action

        return temp_action
    
    elif player(board) == O:
        temp = 1
        temp_action = None
        for action in actions(board):
            best = max_val(result(board, action))

            if temp >= best:
                temp = best
                temp_action = action

        return temp_action
    

           
        


