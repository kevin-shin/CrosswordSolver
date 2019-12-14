from solver import Solver, matrix_score, make_grid_from_guesses
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from printer import print_puzzle, print_grid
from clue_solutions import guess_set_score
from printer import print_guess_set

if __name__ == "__main__":
    example_puzzle = Puzzle.from_file("data/test_puzzle_1.json")
    print_puzzle(example_puzzle)
    solver = Solver(example_puzzle)
    dfs_solution = solver.solve("DFS")
    print()
    print("#########################################")
    print("########## SOLUTIONS GENERATED ##########")
    print("#########################################")
    print_guess_set(dfs_solution)
    print_grid(make_grid_from_guesses(dfs_solution,example_puzzle.clues,example_puzzle.size))
    print("HERE IS THE SCORE")
    print(guess_set_score(dfs_solution))


