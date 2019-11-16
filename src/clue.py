across = "across"

class Clue:
    def __init__(self,row,column,length,direction,description,number):
        self.row = row
        self.column = column
        self.length = length
        self.direction = direction
        self.description = description
        self.number = number
        self.num_filled = 0

    def get_position(self):
        return (self.row, self.column)

    def get_description(self):
        return self.description

    def __str__(self):
        return "Clue: {}".format(self.description)
    
        