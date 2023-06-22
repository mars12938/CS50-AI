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

def get_mask(number, board):
    mask_int = 0

    for i in range(len(board)):
        if board[i] != number:
            continue
        n = len(board) - i - 1
        x = 1 << n
        mask_int |= x
    return mask_int


'''def find_winner(board, symbol):

    W = symbol
    e = "e"
    win_states = [[[W, W, W],
                   [e, e, e],
                   [e, e, e]], 
                  [[e, e, e],
                   [W, W, W],
                   [e, e, e]], 
                  [[e, e, e],
                   [e, e, e],
                   [W, W, W]], 
                  [[W, e, e],
                   [W, e, e],
                   [W, e, e]], 
                  [[e, W, e],
                   [e, W, e],
                   [e, W, e]], 
                  [[e, e, W],
                   [e, e, W],
                   [e, e, W]], 
                  [[W, e, e],
                   [e, W, e],
                   [e, e, W]],
                  [[e, e, W],
                   [e, W, e],
                   [W, e, e]]]
    

    
    for state in win_states:  
        counter = 0
        for row in range (0, 3):
            for col in range (0, 3):
                if state[row][col] == W:
                    if board[row][col] == W:   # if the board matches W, increase counter
                        counter+=1
        if counter == 3:                       # if counter = 3, then we have a win since each win_state has 3 W's
            return True
        else:                                  # else the board is not in that particular configuration, meaning we have to check the rest
            counter = 0
    
    return False                               # if we got to the end and true wasn't returned, board is not in a winning state

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if find_winner(board, X):
        return X
    elif find_winner(board, O):
        return O
    else:
        return None '''

                    

def winner(board):    
    conv_board = convert_board(board)
    board_x = get_mask(1, conv_board)
    board_o = get_mask(2, conv_board)
    
    # generates mask for each of the win states
    if len(win_states_mask) == 0:
        for i in range(len(win_states)):
            mask = get_mask(1, win_states[i])
            win_states_mask.append(mask)

    for i in range(len(win_states_mask)):
        mask = win_states_mask[i]
        mask_b_x = mask & board_x
        mask_b_o = mask & board_o

        if mask == mask_b_x:
            return X
        elif mask == mask_b_o:
            return O
    
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

    # board must be terminal
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_val(state):
    
    v = -math.inf

    if terminal(state):
        return utility(state)
    for action in actions(state):
        v = max(v, min_val(result(state, action)))
    return v


def min_val(state):

    v = math.inf

    if terminal(state):
        return utility(state)
    for action in actions(state):
        v = min(v, max_val(result(state, action)))
    return v


def board_key_gen(board):

    key = 0
    for i in range(0, 9):
        key += math.pow(10, i) * board[i]
    return int(key)

cache_x = {}
def actions_x(board, action):

    new_board = convert_board(result(board, action))

    board_key_x = board_key_gen(new_board)
    # If the board already exists in cache_x, no need to do calculation since it was calculated previously
    if cache_x and board_key_x in cache_x.keys():
        return cache_x[board_key_x]

    #if board_key_x in cache_x:
        #print(True)
    
    # else do the calculation, and add the board as a key and its new value
    best_x = min_val(result(board, action))
    cache_x[board_key_x] = best_x
    print("CACHE_X: ", cache_x)
    return best_x

cache_o = {}
def actions_o(board, action):

    new_board = convert_board(result(board, action))
    #print(new_board)

    board_key_o = board_key_gen(new_board)

    #print("board-key: ", board_key_o)
    if cache_o and board_key_o in cache_o.keys():
        return cache_o[board_key_o]
    #if board_key_o in cache_o:
        #None
    #    return cache_o[board_key_o]
    
    best_o = max_val(result(board, action))
    cache_o[board_key_o] = best_o
    #print("CACHE_O: ", cache_o)

    return best_o


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
            # takes the best of the minimum values, temp keeps track of the max of those so far
            
            #best = min_val(result(board, action))
            best = actions_x(board, action)

            if temp <= best:
                temp = best
                temp_action = action

        return temp_action
    
    elif player(board) == O:
        temp = 1
        temp_action = None
        for action in actions(board):
            # takes the best of the maximum values, temp keeps track of the min of those so far

            #best = max_val(result(board, action))
            best = actions_o(board, action)

            if temp >= best:
                temp = best
                temp_action = action

        return temp_action
    

           
        


