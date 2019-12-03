from clue import Clue
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from datamuse import get_answers
from printer import print_grid, print_cluelist


verbose = True

class Solver():
    def __init__(self, puzzle: Puzzle):
        #TODO XML parser
        self.puzzle = puzzle
        self.size = puzzle.size * puzzle.size
        self.grid = make_grid(self.puzzle)
        # self.grid = [[None for i in range(self.puzzle.size)] for i in range(self.puzzle.size)]


    def solve(self, solve_method):
        if solve_method == "DFS":
            return DFS(self.grid, self.puzzle.clues, set(), set(), [])
        # elif solve_method == "BFS":
        #     return BFS(self.grid, {}, {}, [])

    def get_size(self):
        return self.size

    def __str__(self):
        return str(self.puzzle) + "\n" + str(self.grid)


################################################################################################################ 
#                         SEARCH ALGORITHMS: DFS, BFS                                                          #
################################################################################################################       


def DFS(state_grid, clues, visited_states, visited_clues, solution_list):
    if verbose:
        print()
        print("------->     STARTING DFS  ")
        print("Current Clues: ")
        print_cluelist(clues)
        print("Current Visited Clues: " )
        print_cluelist(list(visited_clues))
        # print("Current Visited States: " + str(visited_states))
    if len(visited_clues) == len(clues):
        solution_list.append(state_grid)
        print("Hit here")

    possible_guesses = generate_guesses(state_grid, clues, visited_clues)

    for guess in possible_guesses:
        if check_fit(state_grid, guess):
            new_child = fit(state_grid, guess)
            print_grid(new_child)
            tuple_v = grid_to_tuple(new_child)
            if (tuple_v not in visited_states):
                visited_clues.add(guess.get_clue())
                visited_states.add(tuple_v)
                DFS(new_child, clues, visited_states, visited_clues, solution_list)

    return solution_list

def BFS(state_grid, clues):
    state_queue = []
    solution_list = []
    visited_clues = {}
    visited_states = {}

    if len(visited_clues) == len(clues):
        solution_list.append(state_grid)

    possible_guesses = generate_guesses(state_grid, clues, visited_clues)

    for guess in possible_guesses:
        new_child = fit(state_grid, guess)

        if (new_child not in visited_states):
            visited_clues.add(guess.get_clue())
            visited_states.add(new_child)
            DFS(new_child, visited_states, visited_clues, solution_list)

    return solution_list



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
        clue_guesses = get_answers(clue, 1)
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
            return False
        else:
            for index in range(guess_length):
                if not (grid[guess_position[0]][guess_position[1]+index] == None or grid[guess_position[0]][guess_position[1]+index] == guess_string[index]):
                    return False 
    elif guess_direction == 'D': #down
        if guess_position[0] + guess_length > len(grid):
                return False
        else: 
            for index in range(guess_length):
                if not (grid[guess_position[0]+index][guess_position[1]] == None or grid[guess_position[0]+index][guess_position[1]] == guess_string[index]):
                    return False
    return True 

def fit(grid, guess):
    new_grid = grid
    guess_direction = guess.get_direction()
    guess_position = guess.get_position()
    guess_length = guess.get_length()
    guess_string = guess.get_string()

    if guess_direction == 'A': #across
        for index in range(guess_length):
            new_grid[guess_position[0]][guess_position[1]+index] = guess_string[index]
    elif guess_direction == 'D': #down
        for index in range(guess_length):
            new_grid[guess_position[0]+index][guess_position[1]] = guess_string[index]

    return new_grid

def make_grid(puzzle):
    blank = [["[-]" for i in range(puzzle.size)] for i in range(puzzle.size)]
    for clue in puzzle.clues:
        clue_direction = clue.get_direction()
        clue_position = clue.get_position()
        clue_length = clue.get_length()
        if clue_direction == 'A':
            for index in range(clue_length):
                blank[clue_position[0]][clue_position[1]+index] = None
        elif clue_direction == 'A':
            for index in range(clue_length):
                blank[clue_position[0]+index][clue_position[1]] = None
    
    return blank


def grid_to_tuple(grid):
    '''For hashing reasons, we can't use lists. We need a way to make grids tuples.'''
    
    list_to_tuple = []
    for row in grid: 
        list_to_tuple.append(tuple(row))
    
    return tuple(list_to_tuple)