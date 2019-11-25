from solver import Solver
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder

if __name__ == "__main__":
    example_puzzle = Puzzle.from_file("./example_puzzle.json")
    solver = Solver(example_puzzle)
    print(solver)

