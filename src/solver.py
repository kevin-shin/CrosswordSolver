import datamuse
from clue import Clue
from puzzle import Puzzle

class Solver():
    def __init__(self,puzzle:Puzzle):
        #TODO XML parser
        self.puzzle = puzzle.parsed()

if __name__ == "__main__":
    c1 = Clue(0,0,3,"A","_ wrestling",1)
    c4 = Clue(1,0,5,"A","Kids can makes money by losing them",4)
    c7 = Clue(2,0,5,"A","_ game",7)
    c8 = Clue(3,1,4,"A","video _",8)
    c9 = Clue(4,1,4,"A","Org on Brooklyn Nine-Nine",9)

    clue_1D = Clue(0,0,3,"D","Four-wheel off-roader", 1)
    clue_2D = Clue(0,1,5,"D","Period in power",2)
    clue_3D = Clue(2,0,5,"D","Time for some self-pampering",3)
    clue_5D = Clue(1,3,4,"D","Something measured in F or F, for short",5)
    clue_6D = Clue(1,4,4,"D","Worked the soil",6)

    l = [c1,c4,c7,c8,c9,clue_1D,clue_2D,clue_3D,clue_5D,clue_6D]
    example_puzzle = Puzzle(5,l,{})
    print("here")
    print(example_puzzle)