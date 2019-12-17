from solver import Solver, matrix_score, make_grid_from_guesses, init_grid
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from clue_solutions import guess_set_score
from printer import print_puzzle, print_grid
from clue_solutions import guess_set_score
from printer import print_guess_set
from statistics import mean

test_puzzles = ["test_puzzle_1.json", "test_puzzle_2.json", "test_puzzle_3.json", "test_puzzle_4.json", "test_puzzle_5.json", "test_puzzle_6.json", "test_puzzle_7.json", "test_puzzle_8.json", "test_puzzle_9.json"]

if __name__ == "__main__":
    for puzzle in test_puzzles:
        example_puzzle = Puzzle.from_file("data/" + puzzle)
        solver = Solver(example_puzzle)
        dfs_solution = solver.solve("DFS")
        score = guess_set_score(dfs_solution)
        print("PUZZLE " + puzzle + ":")
        print("     Complexity: " + str(solver.complexity))
        print("     Score: " + str(score))
        

