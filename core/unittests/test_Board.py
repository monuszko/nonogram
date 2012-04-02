
#! /usr/bin/env python3

import unittest
from ..Board import Board
from ..Line import Line
from ..constants import _EMP, _BLK, _UNK

class TestBoard(unittest.TestCase):
    """
    A test class for the Board module.
    """
    def setUp(self):
        rows = ([3],
                [2, 1],
                [1, 1],
                [1, 4],
                [1, 1, 1, 1],
                [2, 1, 1, 1],
                [2, 1, 1],
                [1, 2],
                [2, 3],
                [3]
               )
        cols = ([3],
                [2, 1],
                [2, 2],
                [2, 1],
                [1, 2, 1],
                [1, 1],
                [1, 4, 1],
                [1, 1, 2],
                [3, 1],
                [4]
               )
        self.Board = Board(rows, cols)

    def test_isfull(self):

        for y in range(10):
            for x in range(10):
                self.Board.solved[(x, y)] = _BLK if x % 3 == 0 else _EMP

        self.assertEqual(self.Board.isfull(), True)
        
        del self.Board.solved[(4, 5)]
        self.assertEqual(self.Board.isfull(), False)

    # TODO: test_display(self):

        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBoard))


if __name__ == '__main__':
    unittest.main()
