import unittest
import sys
import os

sys.path.append(os.getcwd() + '/src')

from guess import Guess
from clue import Clue
from solver import collide, find_best_guess_set


class GuessTest(unittest.TestCase):

    # def test_collision(self):
    #     print("KIND, SPACE")
    #     print(collide(sample_guess, sample_guess_2))
    #     print("SPACE, IDEA")
    #     print(collide(sample_guess_3, sample_guess_2))
    #     print("KIND, IDEA")
    #     print(collide(sample_guess, sample_guess_3))

    def test_find_best_set(self):
        sample_clue = Clue(0,2,4,"D","",0,"KIND")
        sample_clue_2 = Clue(0,3,5,"D","",1,"SPACE")
        sample_clue_3 = Clue(2, 0, 4, "A", "", 2, "IDEA")

        sample_guess = Guess(sample_clue, "KIND", 4)
        sample_guess_2 = Guess(sample_clue_2, "SPACE", 6)
        sample_guess_3 = Guess(sample_clue_3, "IDEA", 5)

        guess_set = set()
        guess_set.add(sample_guess)
        guess_set.add(sample_guess_2)
        returned_set = find_best_guess_set(guess_set, sample_guess_3)

        for guess in returned_set:
            print(guess)

if __name__ == "__main__":
    unittest.main()