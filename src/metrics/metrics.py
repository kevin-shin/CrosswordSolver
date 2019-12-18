'''
@author: Kevin Shin, Avik Bosshardt
    metrics.py consolidates methods which compute statistics and scores 
    when evaluating the correctness of the puzzle and guesses.
'''

import sys
import os

sys.path.append(os.getcwd() + '/model')

from guess import Guess
from clue import Clue
from solver import collide, find_best_guess_set
from statistics import mean


def print_puzzle_stats(puzzle):
    '''
    @input: puzzle -> Puzzle object
        Prints the size, number of clues, average solution length, and average description length
        associated with the puzzle. 
    '''
    print("--------------------------")
    print("-       STATISTICS       -")
    print("--------------------------")
    print("     Size = ", puzzle.size)
    print("     Num Clues = ", len(puzzle.clues))
    print("     Mean Solution Length = ",mean(c.length for c in puzzle.clues))
    print("     Mean Desc Length = ", mean(len(c.description) for c in puzzle.clues))


def guess_set_score(guess_set):
    '''
    @input: guess_set -> Python set of Guess objects
        The "Guess set score" is defined as the ratio of the total number of correctly guessed letters
        PER GUESS, to the total number of letters PER GUESS. In other words, for each guess, we compute
        how many letters it shares with the actual solution, and divide by the total number of letters.
        Note that this means that in instance where clues intersect on the board, these are double-counted.
    '''
    num_correct = 0
    num_total = 0
    for guess in guess_set:
        correct_solution = guess.get_clue().get_solution()
        guess_solution = guess.get_string()
        num_correct += compare_answers(guess_solution, correct_solution)
        num_total += len(guess_solution)
    
    return num_correct/num_total


def compare_answers(guess_answer, correct_answer):
    '''
    @input: guess_answer -> String, correct_answer -> String
        Returns the number of corresponding letters between the guess and actual answer.
    '''
    num_correct = 0
    for i in range(len(guess_answer)):
        if guess_answer[i] == correct_answer[i]:
            num_correct += 1
    
    return num_correct
