from solver import Solver, matrix_score
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from printer import print_puzzle, print_grid

if __name__ == "__main__":
    example_puzzle = Puzzle.from_file("data/test_puzzle_1.json")
    print_puzzle(example_puzzle)
    solver = Solver(example_puzzle)
    dfs_solution = solver.solve("DFS")
    print()
    print("#########################################")
    print("########## SOLUTIONS GENERATED ##########")
    print("#########################################")
    print_grid(dfs_solution)
    print("HERE IS THE SCORE")
    print(matrix_score(dfs_solution))


