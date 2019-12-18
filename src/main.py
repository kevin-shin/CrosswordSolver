import sys
import os

sys.path.append(os.getcwd() + '/src/metrics')
sys.path.append(os.getcwd() + '/src/model')

from solver import Solver, matrix_score, make_grid_from_guesses, init_grid
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from printer import print_puzzle, print_grid
from metrics import print_puzzle_stats
from printer import print_guess_set
from statistics import mean

verbose = True

if __name__ == "__main__":
    print()
    print("Input the file name of the puzzle you would like to solve: ")
    print("      e.g. test_puzzle_8.json")
    print()

    user_input = input()
    puzzle_file = "./data/" + user_input

    input_puzzle = Puzzle.from_file(puzzle_file) 
    solver = Solver(input_puzzle)
    
    if verbose: 
        print_puzzle(input_puzzle)
        print_grid(solver.grid)

    dfs_solution = solver.solve()

    if verbose: 
        print()
        print("#########################################")
        print("########## SOLUTIONS GENERATED ##########")
        print("#########################################")
        print_guess_set(dfs_solution)
        final_result = make_grid_from_guesses(dfs_solution, input_puzzle.clues, input_puzzle.size)
        print_grid(final_result)
        print()

        print_puzzle_stats(input_puzzle)

