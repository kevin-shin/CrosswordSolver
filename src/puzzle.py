from clue import Clue

class Puzzle():
    def __init__(self, size:int, clues:list, clue_neighbors:dict):
        self.size = size
        self.clues = clues
        self.clues_map = {}
        self.build_adj_list()
        self.clue_neighbors = clue_neighbors

    def build_adj_list(self):
        for clue in self.clues:
            self.clues_map[clue.get_position()] = clue 

    def __str__(self):
        arr = []
        for clue in self.clues_map.keys():
            arr.append((clue, self.clues_map[clue].get_description()))
        return str(arr)

