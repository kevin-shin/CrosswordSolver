import json

'''
    Clue objects represent one clue of the puzzle. They store their position on the grid, length, description, 
    id_number, and solution. The solution is included as an instance variable only to allow for efficient 
    scoring calculations, and is not actually used in the IDFS algorithm.
'''

class Clue:
    def __init__(self, row:int, column:int, length:int, direction:str, description:str, number:int, solution: str):
        self.row = row
        self.column = column
        self.length = length
        self.direction = direction
        self.description = description
        self.number = number
        self.solution = solution

    def get_position(self):
        return (self.row, self.column)

    def get_description(self):
        return self.description
    
    def get_direction(self):
        return self.direction
    
    def get_length(self):
        return self.length
    
    def get_solution(self):
        return self.solution

    def __str__(self):
        return "Clue ({}) at position {}: {}".format(self.direction, (self.row, self.column), self.description)

    def __eq__(self,other):
        return type(other) == type(self) and self.description == other.description
    
    def __hash__(self):
        return hash(self.description)