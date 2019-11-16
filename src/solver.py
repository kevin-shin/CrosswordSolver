import datamuse
from clue import Clue
from puzzle import Puzzle, PuzzleEncoder, PuzzleDecoder

class Solver():
    def __init__(self,puzzle:Puzzle):
        #TODO XML parser
        self.puzzle = puzzle.parsed()

if __name__ == "__main__":
    
    with open("example_puzzle.json","r") as f:
        lines = f.read()
    d = PuzzleDecoder()
    example_puzzle = d.decode(lines)
    print(type(example_puzzle),example_puzzle, example_puzzle.clues[0])