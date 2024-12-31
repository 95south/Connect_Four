import math
import random

from variables import ROW_COUNT, COLUMN_COUNT, PLAYER_PIECE, AI_PIECE
from functions import is_valid_location, game_over_check, get_next_open_row, drop_piece
from score_ai import score_position

# Getting valid locations for AI
def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

# Checking for terminal nodes
def is_terminal_node(board):
    return game_over_check(board, PLAYER_PIECE) or game_over_check(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# Implimenting minimax algorithm
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)

    if isTerminal := is_terminal_node(board): # Check if the current board state is a terminal node or if the search depth is zero. 
        if game_over_check(board, AI_PIECE): #If it is a terminal node, return the appropriate score (math.inf, -math.inf, or 0). 
            return (None, math.inf) # If the maximizing player wins, return positive infinity.
        elif game_over_check(board, PLAYER_PIECE): #
            return (None, -math.inf) # If the minimizing player wins, return negative infinity.
        else: 
            return (None, 0)
    elif depth == 0: #If depth is zero, return the board's score for the AI piece.
        return (None, score_position(board, AI_PIECE)) 

    if maximizing_player: #If the maximizing player is the current player, set the value to negative infinity and the column to a random valid location.
        value = -math.inf
        column = random.choice(valid_locations)

        for c in valid_locations: #Iterate through each valid location.
            r = get_next_open_row(board, c) #Get the row where the piece will be placed.
            temp_board = board.copy() #Copy the board.
            drop_piece(temp_board, r, c, AI_PIECE) #Drop the piece in the copied board.
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1] #Recursively call minimax with the copied board, the depth decremented by one, and the maximizing player set to False.

            if new_score > value: #If the new score is greater than the current value, update the value and column.
                value = new_score 
                column = c 
            
            alpha = max(alpha, value) #Update alpha to the maximum of alpha and value.

            if alpha >= beta: 
                break

    # Minimizing player
    else: #recursive call for minimizing player calculates
        value = math.inf
        column = random.choice(valid_locations) #Set the value to positive infinity and the column to a random valid location.

        for c in valid_locations: #Iterate through each valid location.
            r = get_next_open_row(board, c) 
            temp_board = board.copy()
            drop_piece(temp_board, r, c, PLAYER_PIECE) 
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]

            if new_score < value: #If the new score is less than the current value, update the value and column.
                value = new_score 
                column = c 

            beta = min(beta, value) #Update beta to the minimum of beta and value.

            if alpha >= beta: 
                break
            
    return column, value