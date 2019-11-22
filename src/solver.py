import datamuse
from clue import Clue
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder

class Solver():
    def __init__(self,puzzle:Puzzle):
        #TODO XML parser
        self.puzzle = puzzle.parsed()

if __name__ == "__main__":
    p = Puzzle.from_file("example_puzzle.json")
    print(p)