'''
    @author: Kevin Shin
    printer.py defines a set of functions which are helpful for debugging and visualization purposes.
    These functions are often imported into solver.py or main.py on a need-to-use basis. 

'''


def print_grid(matrix): 
    '''
    @input: matrix -> 2D array
        Provides printing method to preserve equal spacing between None, letters, and blanks.
    '''
    print("_________________________________")
    print()
    for row in matrix:
        for col in row: 
            if col == "[-]":
                print(" " + col + " ", end=" ")
            elif col == None:
                print(str(col) + " ", end=" ")
            else:
                print("  " + col + "  ", end= " ")
        print()
    print("_________________________________")


def print_puzzle(puzzle):
    '''
    @input: puzzle -> Puzzle object
        Provides printing method to print clues of a puzzle
    '''

    print("######################################")
    print("#               PUZZLE               #")
    print("######################################")
    
    for clue in puzzle.clues:
        print("   " + str(clue), end= " ")
        print()



def print_cluelist(clue_list):
    '''
    @input: clue_list -> list of Clue objects
        Provides printing method to print list of clues.
    '''
    for clue in clue_list:
        print("   " + str(clue))


def print_guess_set(guess_set):
    '''
    @input: guess_set -> Python set containing Guess objects
        Provides printing method for a set of guesses.
    '''
    for guess in guess_set:
         print("   " + str(guess))

