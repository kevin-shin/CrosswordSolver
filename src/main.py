from solver import Solver
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder

verbose = True


if __name__ == "__main__":
    example_puzzle = Puzzle.from_file("data/example_puzzle.json")
    if verbose:
        print("EXAMPLE PUZZLE")
        print(example_puzzle)
    solver = Solver(example_puzzle)
    dfs_solution = solver.solve("DFS")
    print(dfs_solution)

