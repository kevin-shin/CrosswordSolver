import unittest
import sys
import os

sys.path.append(os.getcwd() + '/src/model')
sys.path.append(os.getcwd() + '/src/metrics')

from guess import Guess
from clue import Clue
from solver import collide, find_best_guess_set, init_grid, check_fit, matrix_score, make_grid_from_guesses
from metrics import compare_answers, guess_set_score

class GuessTest(unittest.TestCase):

    ################################## Solver Tests ##############################################

    def test_collision(self):

        sample_clue = Clue(0,2,4,"D","",0,"KIND")
        sample_clue_2 = Clue(0,3,5,"D","",1,"SPACE")
        sample_clue_3 = Clue(2, 0, 4, "A", "", 2, "IDEA")

        sample_guess = Guess(sample_clue, "KIND", 4)
        sample_guess_2 = Guess(sample_clue_2, "SPACE", 6)
        sample_guess_3 = Guess(sample_clue_3, "IDEA", 5)

        self.assertEquals(None,collide(sample_guess, sample_guess_2))
        self.assertEquals(None,collide(sample_guess_3, sample_guess_2))
        self.assertEquals((sample_guess,sample_guess_3),collide(sample_guess, sample_guess_3))

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

    def test_check_fit(self):
        sample_clue = Clue(0,2,4,"D","",0,"KIND")
        sample_clue_2 = Clue(0,3,5,"D","",1,"SPACE")
        sample_clue_3 = Clue(2, 0, 4, "A", "", 2, "IDEA")

        grid = init_grid([sample_clue,sample_clue_2,sample_clue_3],5)

        sample_guess = Guess(sample_clue, "KIND", 4)
        sample_guess_2 = Guess(sample_clue_2, "SPACE", 6)
        sample_guess_3 = Guess(sample_clue_3, "IDEASS", 5)

        self.assertEqual("fit",check_fit(grid,sample_guess))
        self.assertEqual("fit",check_fit(grid,sample_guess_2))
        self.assertEqual("bounds_error",check_fit(grid,sample_guess_3))

    def test_matrix_score(self):
        sample_clue = Clue(0,2,4,"D","",0,"KIND")
        sample_clue_2 = Clue(0,3,5,"D","",1,"SPACE")
        sample_clue_3 = Clue(2, 0, 4, "A", "", 2, "IDEA")

        sample_guess = Guess(sample_clue, "KIND", 4)
        sample_guess_2 = Guess(sample_clue_2, "SPACE", 6)
        sample_guess_3 = Guess(sample_clue_3, "IDEA", 5)

        grid_empty = init_grid([sample_clue,sample_clue_2,sample_clue_3],5)
        grid_from_guesses = make_grid_from_guesses([sample_guess,sample_guess_2,sample_guess_3],
        [sample_clue,sample_clue_2,sample_clue_3],5)

        self.assertEqual(0,matrix_score(grid_empty))
        self.assertEqual(11/25,matrix_score(grid_from_guesses))

    ################################## Metrics Tests ##############################################

    def test_compare_answers(self):

        self.assertEqual(4,compare_answers("IDEA","IDEA"))
        self.assertEqual(3,compare_answers("IDES","IDEA"))
        self.assertEqual(0,compare_answers("TEST","IDEA"))




if __name__ == "__main__":
    unittest.main()