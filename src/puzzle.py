import json
import os 
from statistics import mean
from clue import Clue

class Puzzle():
    def __init__(self, size, clues):
        self.size = size
        self.clues = clues

    def __str__(self):
        return str(self.clues)

    def print_stats(self):
        print("------------------")
        print("----STATISTICS----")
        print("------------------")
        print()
        print("Size =", self.size)
        print("Num Clues =", len(self.clues))
        print("Mean Solution Length=",mean(c.length for c in self.clues))
        print("Mean Desc Length=",mean(len(c.description) for c in self.clues))

    @staticmethod
    def from_file(filename):
        pd = PuzzleDecoder()
        with open(filename,"r") as f:
            lines = f.read()
            return pd.decode(lines)


class PuzzleEncoder(json.JSONEncoder):
     def default(self, object):
        if isinstance(object, Puzzle):
            return {"puzzle":{"size":object.size,"clues":object.clues}}
        elif isinstance(object,Clue):
            return {"clue":object.__dict__}
        else:
            return json.JSONEncoder.default(self, object) 

class PuzzleDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    def object_hook(self, dct):
        if 'clue' in dct:
            return Clue(dct['clue']['row'],dct['clue']['column'],
            dct['clue']['length'],dct['clue']['direction'],dct['clue']['description'],
            dct['clue']['number'], dct['clue']['solution'])
        elif "puzzle" in dct:
            return Puzzle(dct["puzzle"]["size"],dct["puzzle"]["clues"])
        return dct