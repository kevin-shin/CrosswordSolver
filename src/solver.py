from clue import Clue
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from datamuse import get_answers
from printer import print_grid, print_cluelist, print_guess_set
import random
import datamuse
import google_searcher 

printInit = False
printDFSIteration = True
printGuessAndGrid = True

class Solver():
    def __init__(self, puzzle: Puzzle):
        #TODO XML parser
        self.puzzle = puzzle
        self.size = puzzle.size * puzzle.size
        self.grid = init_grid(self.puzzle.clues, self.puzzle.size)
        if printInit:
            print("----------> Starting Grid: INIT GRID")
            print_grid(self.grid)

    def solve(self, solve_method):
        return DFS(self.grid, self.puzzle.clues, set(), set(), set(), self.grid)

    def get_size(self):
        return self.size

    def __str__(self):
        return str(self.puzzle) + "\n" + str(self.grid)


########################################################################################################## 
#                                 SEARCH ALGORITHM                                                       #
##########################################################################################################       


def DFS(state_grid, clues, guess_set, visited_states, visited_clues, best_solution):

    size = len(state_grid)
    
    if len(visited_clues) == len(clues) or is_full(state_grid):
        return guess_set

    possible_guesses = generate_guesses(clues, visited_clues)

    for guess in possible_guesses:
        if check_fit(state_grid, guess) == "fit":
            guess_set.add(guess)
            visited_clues.add(guess.get_clue())
        elif check_fit(state_grid, guess) == "collision":
            guess_set = find_best_guess_set(guess_set, guess)
        elif check_fit(state_grid, guess) == "bounds_error":
            continue

        state_grid = make_grid_from_guesses(guess_set, clues, size)

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

        tuple_v = grid_to_tuple(state_grid)
        if (tuple_v not in visited_states):
            visited_states.add(tuple_v)
            DFS(state_grid, clues, guess_set, visited_states, visited_clues, best_solution)

    return guess_set


################################################################################################################ 
#                                         Helper Methods                                                       #
################################################################################################################ 


def generate_guesses(clues, visited_clues):

    clue_set = set(clues)
    not_used_clues = clue_set.difference(visited_clues)
    not_used_list = list(not_used_clues)
    guesses = []

    for clue in not_used_list:
        #TODO: Use information about the clues to not check for bounds_error but only call permissible clues? 
        #might be difficult with google. 
        answer_func = partition_clue(clue)
        clue_guesses = answer_func(clue, 3)
        guesses.extend(clue_guesses)
    return guesses


def check_fit(grid, guess):
    ''' Fits a guess into the grid, returning new grid'''
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


def find_best_guess_set(guess_set, current_guess):
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
        print("FIND BEST GUESS SET IS GOING WRONG")



def init_grid(clues, size):
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


def make_grid_from_guesses(guesses, clues, size):

    state_grid = init_grid(clues, size)

    for guess in guesses:
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


def grid_to_tuple(grid):
    '''For hashing reasons, we can't use lists. We need a way to make grids tuples.'''
    list_to_tuple = []
    for row in grid: 
        list_to_tuple.append(tuple(row))
    
    return tuple(list_to_tuple)


def is_full(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == None:
                return False
    return True 


def collide(guess, other_guess):
    ''' returns (guess, other_guess) if there is a collision between two guesses. If not, returns none"'''

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
    
def partition_clue(clue:Clue):
    if "*" in clue.description:
        return google_searcher.get_blank_answers
    elif '"' in clue.description:
        return google_searcher.get_quote_answers
    else:
        return datamuse.get_answers

def matrix_score(grid):
    num_rows = len(grid)
    num_cols = len(grid[0])
    
    total = num_rows * num_cols

    solved = 0

    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] != "[-]" and grid[row][col] != None:
                 solved += 1
    
    return solved/total