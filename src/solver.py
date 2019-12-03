from clue import Clue
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from datamuse import get_answers


verbose = True

class Solver():
    def __init__(self, puzzle: Puzzle):
        #TODO XML parser
        self.puzzle = puzzle
        self.size = puzzle.size * puzzle.size
        self.grid = [[None for i in range(self.puzzle.size)] for i in range(self.puzzle.size)]

    def solve(self, solve_method):
        if solve_method == "DFS":
            return DFS(self.grid, self.puzzle.clues, {}, {}, [])
        # elif solve_method == "BFS":
        #     return BFS(self.grid, {}, {}, [])

    def get_size(self):
        return self.size

    def __str__(self):
        return str(self.puzzle) + "\n" + str(self.grid)


################################################################################################################ 
#                                         SEARCH ALGORITHMS                                                    #
#                                                                                                              #
################################################################################################################       


def DFS(state_grid, clues, visited_states, visited_clues, solution_list):
    if verbose:
        print("######  STARTING DFS  ########")

    if len(visited_clues) == len(clues):
        solution_list.append(state_grid)
        return 

    possible_guesses = generate_guesses(state_grid, clues, visited_clues)

    for guess in possible_guesses:
        new_child = fit(state_grid, guess)

        if (new_child not in visited_states):
            visited_clues.add(guess.get_clue())
            visited_states.add(new_child)
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
        clue_guesses = get_answers(clue)
        guesses.extend(clue_guesses)
    
    return guesses

def fit(grid, guess):
    ''' Fits a guess into the grid, returning new grid'''
    new_grid = grid
    guess_direction = guess.get_direction()
    guess_position = guess.get_position()
    guess_length = guess.get_length()
    guess_string = guess.get_string()

    if guess_direction == 'A': #across
        for index in range(guess_length):
           if not (new_grid[guess_position[0]][guess_position[1]+index] == None or new_grid[guess_position[0]][guess_position[1]+index] == guess[index]):
               return new_grid
    elif guess_direction == 'D': #down
        for index in range(guess_length):
            if not (new_grid[guess_position[0]+index][guess_position[1]] == None or new_grid[guess_position[0]+index][guess_position[1]] == guess[index]):
                return new_grid

    if guess_direction == 'A': #across
        for index in range(guess_length):
            new_grid[guess_position[0]][guess_position[1]+index] = guess[index]
    elif guess_direction == 'D': #down
        for index in range(guess_length):
            new_grid[guess_position[0]+index][guess_position[1]] = guess[index]

    return new_grid