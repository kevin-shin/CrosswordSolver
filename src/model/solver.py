
'''
@author: Kevin Shin

    solver.py is the heart of the algorithm. It contains the IDFS algorithm, which is essentially
    depth-first search but allowing for backtracking by implementing its own collision algorithm. At each recursive
    call, we assess whether the new grid we've returned fills in more of the grid. 

    Specifically, a Solver object contains IDFS as its method. The file is organized as:
        - class Solver()
        - IDFS algorithm
        - Helper methods to IDFS
        - Computational methods for evaluating heuristic

'''

import sys
import os

sys.path.append(os.getcwd() + '/src/model')
sys.path.append(os.getcwd() + '/src/helper')
sys.path.append(os.getcwd() + '/src/searcher')

from clue import Clue
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from datamuse import get_answers
from printer import print_grid, print_cluelist, print_guess_set
import random
import datamuse
import google_searcher 

# Toggle booleans to see prewritten print functions. 
printInit = False
printDFSIteration = False
printGuessAndGrid = False

class Solver():
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.size = puzzle.size * puzzle.size
        self.grid = init_grid(self.puzzle.clues, self.puzzle.size)
        self.complexity = get_complexity(puzzle, self.grid)

        if printInit:
            print("----------> Starting Grid: INIT GRID")
            print_grid(self.grid)

    def solve(self):
        return IDFS(self.grid, self.puzzle.clues, set(), set(), set(), self.grid)

    def get_size(self):
        return self.size

    def __str__(self):
        return str(self.puzzle) + "\n" + str(self.grid)


########################################################################################################## 
#                                       SEARCH ALGORITHM                                                 #
##########################################################################################################       

def IDFS(state_grid, clues, guess_set, visited_states, visited_clues, best_solution):
    '''
        @input:
            state_grid      -> 2d array
            clues           -> list of Clue objects
            guess_set       -> Python set of Guess objects
            visited_states  -> Python set of tuples representing state_grids
            visited_clues   -> Python set of visited clues 
            best_solution   -> 2d array

        @return: Python set of Guess objects

        See notes below on specific implementation details. 
    '''
    size = len(state_grid)
    limit = 5

    #IDFS terminates if we've visisted every clue or the grid is full.
    if len(visited_clues) == len(clues) or is_full(state_grid):
        return guess_set

    #In order to compute the clues we haven't tried yet, we pass in both the full clues list
    #and visited_clues list, and always compute the set difference. generate_guesses iterates through 
    #this difference set, and consolidates the guesses into one big array.
    possible_guesses = generate_guesses(clues, visited_clues, limit)

    for guess in possible_guesses:
        if check_fit(state_grid, guess) == "fit":
            guess_set.add(guess)
            visited_clues.add(guess.get_clue())
        elif check_fit(state_grid, guess) == "collision":
            guess_set = find_best_guess_set(guess_set, guess)
        elif check_fit(state_grid, guess) == "bounds_error":
            continue

        #new state_grid, made from the guess_set returned by the conditions above.
        state_grid = make_grid_from_guesses(guess_set, clues, size)

        #if this new state_grid fills in more of the grid, we consider this the 
        if matrix_score(state_grid) > matrix_score(best_solution):
            best_solution = state_grid

        if printDFSIteration:
            print()
            print("CURRENT GRID: ")
            print_grid(state_grid)
            print_cluelist(clues)

        if printGuessAndGrid:
            print("NEW GUESS SET")
            print_guess_set(guess_set)
            print("NEW GRID")
            print_grid(state_grid)

        # For reasons of storing states, we cast the grid to a tuple for hashability.
        tuple_v = grid_to_tuple(state_grid)
        
        if (tuple_v not in visited_states):
            visited_states.add(tuple_v)
            IDFS(state_grid, clues, guess_set, visited_states, visited_clues, best_solution)

    return guess_set


################################################################################################################ 
#                                         Helper Methods                                                       #
################################################################################################################ 


def generate_guesses(clues, visited_clues, limit):
    '''
        Returns a list of guess objects based on clues which have not been visited.
            @input: clues ->          Python set of Clue objects
                    visited_clues ->  Python set of Clue objects
                    limit ->          int representing 
            @return: list of Guess objects (sorted on score)
    '''

    clue_set = set(clues)
    not_used_clues = clue_set.difference(visited_clues)
    not_used_list = list(not_used_clues)
    guesses = []

    for clue in not_used_list:
        answer_func = partition_clue(clue)
        clue_guesses = answer_func(clue, limit)
        guesses.extend(clue_guesses)

    return sorted(guesses, reverse=True)


def partition_clue(clue:Clue):
    '''
        Clues are passed into Google or Datamuse depending on certain characteristics of the clue description.
        Returns appropriate function.
            @input:  clue -> Clue object
            @return: function
    '''
    if "*" in clue.description:
        return google_searcher.get_blank_answers
    elif '"' in clue.description:
        return google_searcher.get_quote_answers
    else:
        return datamuse.get_answers


def find_best_guess_set(guess_set, current_guess):
    '''
        In the event of a collision, this method is called to find the guess_set with the better score.
            @input: guess_set     -> Python set of Guess objects
                    current_guess -> Guess object
            @return: Python set of Guess objects. This set is always a legal configuration of the board.
    '''

    collide_guess = []
    for guess in guess_set:
        if collide(guess, current_guess) != None:
            collide_guess.append(collide(guess, current_guess))
    
    if len(collide_guess) > 1 or len(collide_guess) == 0:
        return guess_set
    else:
        guess, current_guess = collide_guess[0][0], collide_guess[0][1]
        if guess.get_score() > current_guess.get_score():
            return guess_set
        elif guess.get_score() <= current_guess.get_score():
            guess_set.remove(guess)
            guess_set.add(current_guess)
            return guess_set
    
    if guess_set == None: 
        raise ValueError("Guess set should not be None.")


def check_fit(grid, guess):
    ''' 
        Fits a guess into the grid, returning new grid
            @input: grid ->  2d array
                    guess -> Guess object
            @return: String representing code ("fit", "collision", or "bounds_error")
    
    '''
    guess_direction = guess.get_direction()
    guess_position = guess.get_position()
    guess_length = guess.get_length()
    guess_string = guess.get_string()

    if guess_direction == 'A': #across
        if guess_position[1] + guess_length > len(grid[0]):
            return "bounds_error"
        else:
            for index in range(guess_length):
                if not (grid[guess_position[0]][guess_position[1]+index] == None or grid[guess_position[0]][guess_position[1]+index] == guess_string[index]):
                    return "collision" 
    elif guess_direction == 'D': #down
        if guess_position[0] + guess_length > len(grid):
                return "bounds_error"
        else: 
            for index in range(guess_length):
                if not (grid[guess_position[0]+index][guess_position[1]] == None or grid[guess_position[0]+index][guess_position[1]] == guess_string[index]):
                    return "collision"
    return "fit"

def collide(guess, other_guess):
    ''' 
        Returns (guess, other_guess) if there is a collision between two guesses. If not, returns None
        @input: guess ->       Guess object
                other_guess -> Guess object
    '''

    guess_direction = guess.get_direction()
    guess_position = guess.get_position()
    guess_length = guess.get_length()
    guess_string = guess.get_string()

    other_guess_direction = other_guess.get_direction()
    other_guess_position = other_guess.get_position()
    other_guess_length = other_guess.get_length()
    other_guess_string = other_guess.get_string()

    collision_map = {}

    if guess_direction == "A":
        for i in range(guess_length):
            new_position = (guess_position[0], guess_position[1]+i)
            if new_position not in collision_map:
                collision_map[new_position] = guess_string[i]
            else: 
                if collision_map[new_position] != guess_string[i]:
                    return (guess, other_guess)

    elif guess_direction == "D":
        for i in range(guess_length):
            new_position = (guess_position[0]+i, guess_position[1])
            if new_position not in collision_map:
                collision_map[new_position] = guess_string[i]
            else: 
                if collision_map[new_position] != guess_string[i]:
                    return (guess, other_guess)
    
    if other_guess_direction == "A":
        for i in range(other_guess_length):
            new_position = (other_guess_position[0], other_guess_position[1]+i)
            if new_position not in collision_map:
                collision_map[new_position] = other_guess_string[i]
            else: 
                if collision_map[new_position] != other_guess_string[i]:
                    return (guess, other_guess)

    elif other_guess_direction == "D":
        for i in range(other_guess_length):
            new_position = (other_guess_position[0]+i, other_guess_position[1])
            if new_position not in collision_map:
                collision_map[new_position] = other_guess_string[i]
            else: 
                if collision_map[new_position] != other_guess_string[i]:
                    return (guess, other_guess)
    
    return None


def make_grid_from_guesses(guess_set, clues, size):
    '''
        Makes a 2d array given a guess_set.
            @input: guess_set -> Python set of Guess objects
                    clues     -> list of Clue objects
                    size      -> int, representing what the board size should be
            @return: 2d array
    '''
    state_grid = init_grid(clues, size)

    for guess in guess_set:
        guess_direction = guess.get_direction()
        guess_position = guess.get_position()
        guess_length = guess.get_length()
        guess_string = guess.get_string()

        if guess_direction == 'A':
            for index in range(guess_length):
                state_grid[guess_position[0]][guess_position[1]+index] = guess_string[index]
        elif guess_direction == 'D':
            for index in range(guess_length):
                state_grid[guess_position[0]+index][guess_position[1]] = guess_string[index]
    return state_grid


def init_grid(clues, size):
    '''
        Initializes an empty grid.
        @input: clues -> list of Clue objects
                size  -> int representing size of board
        @return: 2d array
    '''

    blank = [["[-]" for i in range(size)] for i in range(size)]

    for clue in clues:
        clue_direction = clue.get_direction()
        clue_position = clue.get_position()
        clue_length = clue.get_length()

        if clue_direction == 'A':
            for index in range(clue_length):
                blank[clue_position[0]][clue_position[1]+index] = None

        elif clue_direction == 'D':
            for index in range(clue_length):
                blank[clue_position[0]+index][clue_position[1]] = None
                
    return blank


def is_full(grid):
    '''
        Returns True/False whether all the spaces which can be filled are filled.
        @input: grid -> 2d array
        @return: True/False
    '''
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == None:
                return False
    return True 


def grid_to_tuple(grid):
    '''
        For hashing reasons, we can't store states as lists in the visited_states set. 
        We need a way to make grids tuples.
        @input: grid -> 2d array
        @return: tuple
    '''
    list_to_tuple = []
    for row in grid: 
        list_to_tuple.append(tuple(row))
    
    return tuple(list_to_tuple)


################################################################################################################ 
#                                     Computational Methods                                                    #
################################################################################################################ 

def matrix_score(grid):
    '''
        The grid score is defined as the ratio of filled in letters to the total size of the board.
        @input: grid -> 2d array
        @return: float
    '''
    num_rows = len(grid)
    num_cols = len(grid[0])
    
    total = num_rows * num_cols
    solved = 0

    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] != "[-]" and grid[row][col] != None:
                 solved += 1
    
    return solved/total

def get_complexity(puzzle, grid):
    '''
        Complexity is defined as the product of the grid score and collision score. See below for more details.
        @input: puzzle -> Puzzle object
                grid -> 2d array
        @return: float
    '''
    grid_score = get_grid_score(grid)
    collision_score = get_collision_score(grid)
    return grid_score * collision_score


def get_grid_score(grid):
    '''
        Grid score is defined as the ratio of blank fillable squares to the total size of the grid.
        @input: grid -> 2d array
        @return: float
    '''
    empty_squares = 0
    blocked_squares = 0

    num_rows = len(grid)
    num_cols = len(grid[0])

    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] == None:
                empty_squares += 1
            elif grid[row][col] == "[-]":
                blocked_squares += 1
    
    return empty_squares/(num_cols*num_rows)


def get_collision_score(grid):
    '''
        Collision score is defined as the ratio of the number of fillable boxes which are used
        for more than one clue to the total number of fillable boxes.
        @input: grid -> 2d array
        @return: float
    '''
    num_collision = 0
    num_None = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            
            if grid[row][col] == None:
                num_None += 1
                left_neighbor = "[-]"
                right_neighbor = "[-]"
                bottom_neighbor = "[-]"
                top_neighbor = "[-]"

                if row-1 >= 0:
                    left_neighbor = grid[row-1][col]
                if row+1 <= len(grid)-1:
                    right_neighbor = grid[row+1][col]
                if col-1 >= 0:
                    top_neighbor = grid[row][col-1]
                if col+1 <= len(grid)-1:
                    bottom_neighbor = grid[row][col+1]
            
                horizontal_hit = left_neighbor == None or right_neighbor == None
                vertical_hit = top_neighbor == None or bottom_neighbor == None

                if horizontal_hit and vertical_hit:
                    num_collision += 1

    return num_collision/num_None