
'''
@author: Kevin Shin
    complexity_statistics.py is the Python file used to generate the datapoints used for the plots in the paper.
    Each puzzle is read in, and a Puzzle and Solver object are initialized. The main method uses guess_set_score
    to report the accuracy of the puzzle and prints it out with the complexity. See src/model/solver.py for information
    about complexity, and ./metrics.py for guess_set_score.
'''


import sys
import os

#Python requires specific paths to import correctly. 
sys.path.append(os.getcwd() + '/src/model')
sys.path.append(os.getcwd() + '/src/helper')

from solver import Solver, matrix_score, make_grid_from_guesses, init_grid
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from metrics import guess_set_score


test_puzzles = ["test_puzzle_1.json", 
                "test_puzzle_2.json", 
                "test_puzzle_3.json", 
                "test_puzzle_4.json", 
                "test_puzzle_5.json", 
                "test_puzzle_6.json", 
                "test_puzzle_7.json", 
                "test_puzzle_8.json", 
                "test_puzzle_9.json"]


if __name__ == "__main__":

    for puzzle in test_puzzles:
        example_puzzle = Puzzle.from_file("data/" + puzzle)
        solver = Solver(example_puzzle)
        dfs_solution = solver.solve()
        score = guess_set_score(dfs_solution)
        print("PUZZLE " + puzzle + ":")
        print("     Complexity: " + str(solver.complexity))
        print("     Score: " + str(score))
        
