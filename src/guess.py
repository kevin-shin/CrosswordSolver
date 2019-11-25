class Guess():
    def __init__(self, clue: Clue, string: String):
        self.clue = clue #may not be needed
        self.string = string
        self.length = clue.get_length()
        self.direction = clue.get_direction()
        self.position = clue.get_position()
    
    def get_direction(self):
        return self.direction
    
    def get_length(self):
        return self.length
    
    def get_position(self):
        return self.position
    
    def get_string(self):
        return self.string
    
    def get_clue(self):
        return self.clue