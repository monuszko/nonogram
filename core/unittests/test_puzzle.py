
#! /usr/bin/env python3

import unittest
from ..puzzle import *

class Testpuzzle(unittest.TestCase):
    """
    A test class for the puzzle module.
    """

    def test_strnums(self):
        l1 = Line(pos=4, orient='row', length=25, numbers=[3, 4, 5])
        self.assertEqual(l1.strnums(), '3 4 5')

        l2 = Line(pos=5, orient='row', length=20, numbers=[0])
        self.assertEqual(l2.strnums(), '0')

        l3 = Line(pos=6, orient='row', length=21, numbers=[4])
        self.assertEqual(l3.strnums(), '4')

    
    def testfields(self):
        '''
        Checks if intermediate fields are properly initiated
        '''

        # Pointless ?
        l1 = Line(pos=4, orient='row', length=25, numbers=[3, 4, 5])
        self.assertEqual(l1.zones, (0, 1, 1, 0))
        self.assertEqual(l1.fspaces, 11)

    def test_gencombs(self):
        l1 = Line(pos=9, orient='col', length=20, numbers=[0])
        l1.gencombs()
        l1combs = ['.' * 20]
        self.assertEqual(l1.combs, l1combs)

        l2 = Line(pos=9, orient='col', length=20, numbers=[20])
        l2.gencombs()
        l2combs = ['@' * 20]
        self.assertEqual(l2.combs, l2combs)

        l3 = Line(pos=9, orient='col', length=20, numbers=[8])
        l3.gencombs()
        l3combs = ['............@@@@@@@@',
                   '...........@@@@@@@@.',
                   '..........@@@@@@@@..',
                   '.........@@@@@@@@...',
                   '........@@@@@@@@....',
                   '.......@@@@@@@@.....',
                   '......@@@@@@@@......',
                   '.....@@@@@@@@.......',
                   '....@@@@@@@@........',
                   '...@@@@@@@@.........',
                   '..@@@@@@@@..........',
                   '.@@@@@@@@...........',
                   '@@@@@@@@............',
                  ]
        self.assertEqual(l3.combs, l3combs)

        l4 = Line(pos=9, orient='col', length=20, numbers=[7, 9])
        l4.gencombs()
        l4combs = ['...@@@@@@@.@@@@@@@@@',
                   '..@@@@@@@..@@@@@@@@@',
                   '..@@@@@@@.@@@@@@@@@.',
                   '.@@@@@@@...@@@@@@@@@',
                   '.@@@@@@@..@@@@@@@@@.',
                   '.@@@@@@@.@@@@@@@@@..',
                   '@@@@@@@....@@@@@@@@@',
                   '@@@@@@@...@@@@@@@@@.',
                   '@@@@@@@..@@@@@@@@@..',
                   '@@@@@@@.@@@@@@@@@...']
        self.assertEqual(l4.combs, l4combs)

    def test_valid(self):
        l1 = Line(pos=9, orient='col', length=20, numbers=[7, 9])
        self.assertEqual(l1.valid(), False)

        l1.gencombs()
        self.assertEqual(l1.valid(), True)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Testpuzzle))


if __name__ == '__main__':
    unittest.main()
