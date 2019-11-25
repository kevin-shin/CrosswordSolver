import json

class Clue:
    def __init__(self,row:int,column:int,length:int,direction:str,description:str,number:int):
        self.row = row
        self.column = column
        self.length = length
        self.direction = direction
        self.description = description
        self.number = number

    def get_position(self):
        return (self.row, self.column)

    def get_description(self):
        return self.description
    
    def get_direction(self):
        return self.direction
    
    def get_length(self):
        return self.length

    def __str__(self):
        return "Clue: {}".format(self.description)