from statistics import mean

def print_puzle_stats(puzzle):
    print("------------------")
    print("----STATISTICS----")
    print("------------------")
    print()
    print("Size =", puzzle.size)
    print("Num Clues =", len(puzzle.clues))
    print("Mean Solution Length=",mean(c.length for c in puzzle.clues))
    print("Mean Desc Length=",mean(len(c.description) for c in puzzle.clues))

def guess_set_score(guess_set):
    num_correct = 0
    num_total = 0
    for guess in guess_set:
        correct_solution = guess.get_clue().get_solution()
        guess_solution = guess.get_string()
        num_correct += compare_answers(guess_solution, correct_solution)
        num_total += len(guess_solution)
    
    return num_correct/num_total

def compare_answers(guess_answer, correct_answer):
    num_correct = 0
    for i in range(len(guess_answer)):
        if guess_answer[i] == correct_answer[i]:
            num_correct += 1
    
    return num_correct
