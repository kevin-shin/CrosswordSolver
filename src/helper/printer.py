def print_grid(matrix):
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
    print("######################################")
    print("#               PUZZLE               #")
    print("######################################")
    
    for clue in puzzle.clues:
        print("   " + str(clue), end= " ")
        print()

def print_cluelist(clue_list):
    for clue in clue_list:
        print("   " + str(clue))

def print_guess_set(guess_set):
    for guess in guess_set:
         print("   " + str(guess))

