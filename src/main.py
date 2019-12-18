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

if __name__ == "__main__":
    example_puzzle = Puzzle.from_file("./data/test_puzzle_8.json")
    print_puzzle(example_puzzle)
    solver = Solver(example_puzzle)
    print(solver.complexity)
    print_grid(solver.grid)

    dfs_solution = solver.solve("DFS")
    print()
    print("#########################################")
    print("########## SOLUTIONS GENERATED ##########")
    print("#########################################")
    print_guess_set(dfs_solution)
    print_puzzle_stats(example_puzzle)

