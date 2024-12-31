import random
import math
from variables import ROW_COUNT, COLUMN_COUNT, PLAYER_PIECE, AI_PIECE
from functions import get_valid_locations, is_valid_location, game_over_check, get_next_open_row, drop_piece, create_board
from minmax_ai import minimax
from score_ai import score_position

ROWS = 6
COLS = 7

# Function to initialize a random strategy random values ranging from 1-7 for 
def initialize_strategy(): 
    return [random.randint(0, COLS - 1) for _ in range(20)]  # 20 moves per strategy

# Function to evaluate fitness of a strategy        FITNESS FUNCTION
def evaluate_strategy(strategy):
    # Consider more game-specific knowledge
    score = play_game(strategy) #plays a game against a AI
    return score

# Function to play a single game against a AI
def play_game(strategy1):
    # Initialize empty board
    board = create_board()
    current_player = 1
    moves = 0
    total_score = 0
    score = 0
    while True:
        # Alternate between players
        if current_player == 1:
            column = select_move_genetic(strategy1, moves, board)
        else:
            column = select_move_ai(board)
            moves += 1

        # Drop piece into selected 
        row = get_next_open_row(board, column)

        drop_piece(board, row, column , current_player)

        if current_player == 1: 
            score = score_position(board, current_player) - score # old score difference goes +1 else it goes -1
            total_score += score

        # Check for win or draw
        if game_over_check(board, current_player):
            if current_player == 1:
                print("Genetic Algorithm wins!")
                print("Won: " , strategy1)
                exit()
            else:
                print("Score: ", total_score)
                return total_score
        elif check_draw(board):
            print("It's a draw!")
            print("Score: ", total_score)
            return total_score
        current_player = 3 - current_player  # Switch players

#selecting a move from a strategy 
def select_move_genetic(strategy, moves, board):
    if moves < len(strategy) and is_valid_location(board, strategy[moves]): # If strategy is valid, select move from strategy
        return strategy[moves] 
    else: # if strategy is invalid, select a random move
        locations = get_valid_locations(board) # Get valid locations
        move = random.choice(locations) # Randomly select a move
        if moves < len(strategy): # Update strategy
            strategy[moves] = move 
        return move

def select_move_ai(board):
    col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
    return col

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != 0 for col in range(COLS))

# Main genetic algorithm
population_size = 40
parents_size = 15
generations = 400
mutation_rate = 0.05  # Adjust mutation rate

# Improved mutation function
def mutate(strategy): # Mutates a strategy by changing a random move to a random column
    for i in range(len(strategy)): 
        if random.random() < mutation_rate: 
            strategy[i] = random.randint(0, COLS - 1)

# Improved crossover function - making parent 1 array and 50% chance to switch parent 1 values with parent 2
def crossover(parent1, parent2):
    child = parent1.copy()
    for i in range(len(child)):
        if random.random() < 0.5:
            child[i] = parent2[i]
    return child

# Initialize population starting from random popluation
population = [initialize_strategy() for _ in range(population_size)] 

for generation in range(generations):
    # Evaluate fitness of each strategy
    fitness_scores = [evaluate_strategy(strategy) for strategy in population] 
    #print("Generation", generation, "Average Fitness Score:", sum(fitness_scores) / len(fitness_scores))

    # Select parents for reproduction sorting an array of 50 population size and sorting it on best fitness value then sorting it from worst fitness to best fitness and picking the best 10 parents
    parents = [population[i] for i in sorted(range(len(population)), key=lambda x: fitness_scores[x], reverse=True)[:parents_size]]
    print("Parents = "+ parents)

    # Reproduction (crossover)
    offspring = []
    for _ in range(population_size - len(parents)): # Selecting 40 offspring
        parent1, parent2 = random.sample(parents, 2) # Select 2 random parents
        child = crossover(parent1, parent2)  # Use improved crossover
        offspring.append(child)

    # Mutation
    for child in offspring:
        mutate(child)  # Use improved mutation

    # Use elitism
    population = parents + offspring # Combine parents and offspring

# Evaluate final population
final_fitness_scores = [evaluate_strategy(strategy) for strategy in population]

# Print best strategy
best_strategy = population[final_fitness_scores.index(max(final_fitness_scores))]
print("Best strategy:", best_strategy)
print("Fitness score:", max(final_fitness_scores))
