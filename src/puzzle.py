import json
import os 

from clue import Clue


class Puzzle():
    def __init__(self, size, clues):
        self.size = size
        self.clues = clues
        self.clues_map = {}
        self.build_adj_list()

    def build_adj_list(self):
        #TODO: Fix this
        for clue in self.clues:
            self.clues_map[clue.get_position()] = clue 

    def __str__(self):
        arr = []
        for clue in self.clues_map.keys():
            arr.append((clue, self.clues_map[clue].get_description()))
        # return str(arr)
        return str(self.clues)

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
            dct['clue']['number'])
        elif "puzzle" in dct:
            return Puzzle(dct["puzzle"]["size"],dct["puzzle"]["clues"])
        return dct