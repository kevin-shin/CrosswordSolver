from clue import Clue
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from datamuse import get_answers
from printer import print_grid, print_cluelist, print_guess_set
import random
import datamuse
import google_searcher 

verbose = True

class Solver():
    def __init__(self, puzzle: Puzzle):
        #TODO XML parser
        self.puzzle = puzzle
        self.size = puzzle.size * puzzle.size
        self.grid = init_grid(self.puzzle.clues, self.puzzle.size)
        print("INIT GRID")
        print_grid(self.grid)

    def solve(self, solve_method):
        if solve_method == "DFS":
            return DFS(self.grid, self.puzzle.clues, set(), set(), set(), [])
        # elif solve_method == "BFS":
        #     return BFS(self.grid, {}, {}, [])

    def get_size(self):
        return self.size

    def __str__(self):
        return str(self.puzzle) + "\n" + str(self.grid)


################################################################################################################ 
#                         SEARCH ALGORITHMS: DFS, BFS                                                          #
################################################################################################################       


def DFS(state_grid, clues, guess_set, visited_states, visited_clues, solution_list):

    print("NEW DFS")
    print("------->     STARTING DFS  ")
    print("Current Guesses: ")
    print_guess_set(guess_set)
    print("Current Clues: ")
    print_cluelist(clues)
    print("Current Visited Clues: " )
    print_cluelist(list(visited_clues))
    print("Clues I haven't visisted: ")
    print_cluelist(set(clues).difference(visited_clues))
    print("CURRENT GRID: ")
    print_grid(state_grid)

    size = len(state_grid)

    if len(visited_clues) == len(clues) or is_full(state_grid):
        solution_list.append(state_grid)

    possible_guesses = generate_guesses(state_grid, clues, visited_clues)
    print("$$$$$$$$$$$$$$$$$$$$")
    for guess in possible_guesses:
        print("        " + str(guess))

    for guess in possible_guesses:
        if check_fit(state_grid, guess) == "fit":
            print("HIT FIT")
            guess_set.add(guess)
            print("NEW GUESS SET")
            print_guess_set(guess_set)
            state_grid = make_grid_from_guesses(guess_set, clues, size)
            print_grid(state_grid)
            tuple_v = grid_to_tuple(state_grid)
            if (tuple_v not in visited_states):
                visited_clues.add(guess.get_clue())
                visited_states.add(tuple_v)
                DFS(state_grid, clues, guess_set, visited_states, visited_clues, solution_list)
        elif check_fit(state_grid, guess) == "collision":
            print("HIT COLLISION")
            best_guess_set = find_best_guess_set(guess_set, guess)
            print_guess_set(best_guess_set)
            state_grid = make_grid_from_guesses(guess_set, clues, size)
            tuple_v = grid_to_tuple(state_grid)
            if (tuple_v not in visited_states):
                visited_states.add(tuple_v)
                DFS(state_grid, clues, best_guess_set, visited_states, visited_clues, solution_list)
        else:
            continue

    return solution_list

#what if instead of a "do this" approach based on clue fitting, we did it based off of ranking which clues are the easiest to solve?

################################################################################################################ 
#                                         Helper Methods                                                       #
################################################################################################################ 

def generate_guesses(state_grid, clues, visited_clues):
    #major code smell. I think clues might need to be a set 

    clue_set = set(clues)
    not_used_clues = clue_set.difference(visited_clues)
    not_used_list = list(not_used_clues)

    guesses = []

    for clue in not_used_list:
        #eventually need to be a little smarter about this, which is why state_grid is there but not used. 
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
        print("---------------")
        print("---------------")
        print("HERE ARE MY TWO GUESSES ")
        print(str(guess))
        print(str(current_guess))
        if guess.get_score() > current_guess.get_score():
            return guess_set
        elif guess.get_score() < current_guess.get_score():
            guess_set.remove(guess)
            guess_set.add(current_guess)
            return guess_set


def init_grid(clues, size):
    blank = [["[-]" for i in range(size)] for i in range(size)]

    print_grid(blank)

    for clue in clues:
        clue_direction = clue.get_direction()
        clue_position = clue.get_position()
        clue_length = clue.get_length()
        print(str(clue))
        print(clue_direction)
        print(clue_position)
        print(clue_length)

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

# def BFS(state_grid, clues):
#     state_queue = []
#     solution_list = []
#     visited_clues = {}
#     visited_states = {}

#     if verbose:
#         print()
#         print("------->     STARTING BFS  ")
#         print("Current Clues: ")
#         print_cluelist(clues)
#         print("Current Visited Clues: " )
#         print_cluelist(list(visited_clues))
#     # Revisit this. BFS needs a start trigger but maybe shouldn't be random?
#     first_clue = random.choice(clues)
#     state_queue.append(first_clue)
#     visited_clues.add(first_clue)

#     while state_queue:
#         clue = state_queue.pop()
#         possible_guesses = generate_guesses(state_grid, clues, visited_clues)
#         for guess in possible_guesses:
#             if check_fit(state_grid, guess) == "fit":
#                 new_child = fit(state_grid, guess)
#                 print_grid(new_child)
#                 tuple_v = grid_to_tuple(new_child)
#                 if (tuple_v not in visited_states):
#                     visited_clues.add(guess.get_clue())
#                     visited_states.add(tuple_v)
#                     state_queue.append()
#             elif check_fit(state_grid, guess) == "collision":
#                 new_child = change_rank(state_grid, guess, )
#     return solution_list