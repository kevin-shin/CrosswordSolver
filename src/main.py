from solver import Solver
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder
from printer import print_puzzle, print_grid

if __name__ == "__main__":
    example_puzzle = Puzzle.from_file("data/example_puzzle_avik_2.json")
    print_puzzle(example_puzzle)
    solver = Solver(example_puzzle)
    dfs_solution = solver.solve("DFS")
    print()
    print("#########################################")
    print("########## SOLUTIONS GENERATED ##########")
    print("#########################################")
    for solution in dfs_solution:
        print()
        print_grid(solution)
        print()

