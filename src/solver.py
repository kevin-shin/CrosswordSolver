from clue import Clue
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
import datamuse

class Solver():
    def __init__(self, puzzle: Puzzle):
        #TODO XML parser
        self.puzzle = puzzle
        self.size = puzzle.size*puzzle.size
        self.filled = 0
        self.grid = [[None for i in range(self.puzzle.size)] for i in range(self.puzzle.size)]

    def solve(self, solve_method):
        if solve_method == "DFS":
            return DFS(self.grid, {}, {}, [])
        # elif solve_method == "BFS":
        #     return BFS(self.grid, {}, {}, [])

    def get_size(self):
        return self.size
    
    def is_filled(self):
        return self.size == self.filled

    def update_size(self):
    # KEVIN MAKE THIS MORE EFFICIENT LATER
        size = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] != None:
                    size += 1
    def __str__(self):
        return str(self.puzzle) + "\n" + str(self.grid)


################################################################################################################ 
#                                         SEARCH ALGORITHMS                                                    #
#                                                                                                              #
#                                                                                                              #
################################################################################################################       


def DFS(state_grid, visited_states, visited_clues, solution_list):
    if state_grid.is_filled():
        solution_list.append(state_grid)
        return 

    possible_guesses = generate_guesses(state_grid, visited_clues)

    #    TODO: generate_guesses is a function that outputs an array of all the possible moves here.
    #          functionality here might replace the legal move, since in theory this function should 
    #          return all legal moves (see below)

    #          In order to increase efficiency, we should probably do something like "only generate guesses for clues
    #          not explored in that state. But in order to fit a "guess" in the next for-loop, this should be an object?

    for guess in possible_guesses:
        new_child = fit(state_grid, guess)

        if (new_child not in visited_states):
            visited_clues.add(guess.get_clue())
            visited_states.add(new_child)
            DFS(new_child, visited_states, visited_clues, solution_list)

    return solution_list


def BFS(state_grid):
    state_queue = []

    if state_grid.is_filled():
        solution_list.append(state_grid)
        return 

    possible_guesses = generate_guesses(state_grid, visited_clues)

    #    TODO: generate_guesses is a function that outputs an array of all the possible moves here.
    #          functionality here might replace the legal move, since in theory this function should 
    #          return all legal moves (see below)

    #          In order to increase efficiency, we should probably do something like "only generate guesses for clues
    #          not explored in that state. But in order to fit a "guess" in the next for-loop, this should be an object?

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

def fit(grid, guess):
    ''' Fits a guess into the grid, returning new grid'''
    new_grid = grid
    guess_direction = guess.get_direction()
    guess_position = guess.get_position()
    guess_length = guess.get_length()
    guess_string = guess.get_string()

    if guess_direction == 'A': #across
        for index in range(guess_length):
            new_grid[guess_position[0]][guess_position[1]+index] = guess[index]

    elif guess_direction == 'D': #down
        for index in range(guess_length):
            new_grid[guess_position[0]+index][guess_position[1]] = guess[index]

    return new_grid