from clue import Clue

'''
    The Guess class is a wrapper for the string that the external API returns. 
    The Guess object holds a reference to the Clue to which is responds, the string
    representing the actual answer, and a float representing its score.

'''

class Guess():
    def __init__(self, clue: Clue, string: str, score: float):
        self.clue = clue
        self.string = string
        self.score = score
    
    def get_direction(self):
        return self.clue.get_direction()
    
    def get_length(self):
        return len(self.string)
    
    def get_position(self):
        return self.clue.get_position()
    
    def get_string(self):
        return self.string
    
    def get_clue(self):
        return self.clue

    def get_score(self):
        return self.score

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.string == other.string

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return "GUESS" +  "  |  Guess: " + str(self.string) + "   for Clue: " + str(self. clue)