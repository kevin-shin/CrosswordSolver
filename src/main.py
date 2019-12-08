from solver import Solver
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from printer import print_puzzle

verbose = True


if __name__ == "__main__":
    example_puzzle = Puzzle.from_file("../data/example_puzzle_avik_1.json")
    print_puzzle(example_puzzle)
    solver = Solver(example_puzzle)
    dfs_solution = solver.solve("DFS")
    print(dfs_solution)

