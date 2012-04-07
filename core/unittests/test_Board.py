
#! /usr/bin/env python3

import unittest
from ..tools import dicttolists
from ..Board import Board
from ..Line import Line
from ..constants import _EMP, _BLK, _UNK

class TestBoard(unittest.TestCase):
    """
    A test class for the Board module.
    """
    def setUp(self):
        self.maxDiff = None
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

    # TODO: test_memorysafe(self):

    def test_basicsolve(self):
        for line in self.Board.rows + self.Board.cols:
            line.gencombs()
        self.Board.basicsolve()
        
        result = dicttolists(self.Board.solved, 10)
        expected = ['**********',
                    '**********',
                    '**********',
                    '**********',
                    '*****.@.**',
                    '*@***.@.**',
                    '**********',
                    '**********',
                    '**********',
                    '**********']
        self.assertEqual(result, expected)

    def test_solve(self):
        self.Board.solve(hide_progress=True)

        result = dicttolists(self.Board.solved, 10)
        expected = ['.....@@@..',
                    '...@@...@.',
                    '...@....@.',
                    '..@...@@@@',
                    '..@.@.@..@',
                    '@@..@.@..@',
                    '@@....@..@',
                    '@......@@.',
                    '.@@..@@@..',
                    '..@@@.....']
        self.assertEqual(result, expected)

    # TODO: test_verdict(self):

    def test_singleguess(self):
        self.assertEqual(self.Board.singleguess((1, 1), _BLK), False)

    # TODO: test_keepguessing(self):

    def test_save(self):
        self.Board.save()

        backup = self.Board.backups.pop()
        self.assertEqual(backup[0], self.Board.solved)
        self.assertEqual(backup[1], self.Board.rows)
        self.assertEqual(backup[2], self.Board.cols)
        

    def test_restore(self):
        old_rows = [r.copy() for r in self.Board.rows]
        old_cols = [c.copy() for c in self.Board.cols]
        old_height = self.Board.height
        old_width  = self.Board.width
        old_solved = dict.copy(self.Board.solved)
        old_backups = []
        for backup in self.Board.backups:
            solved = dict.copy(backup[0])
            rows   = [r.copy() for r in backup[1]] 
            cols   = [c.copy() for c in backup[2]]
            old_backups.append((solved, rows, cols))

        self.Board.save()
        self.Board.solved = 'a'
        self.Board.rows = reversed(self.Board.rows)
        self.Board.cols = reversed(self.Board.cols)
        self.Board.restore()

        self.assertEqual(self.Board.rows, old_rows)
        self.assertEqual(self.Board.cols, old_cols)
        self.assertEqual(self.Board.height, old_height)
        self.assertEqual(self.Board.width, old_width)
        self.assertEqual(self.Board.solved, old_solved)
        self.assertEqual(self.Board.backups, old_backups)

    def test_valid(self):
        self.assertEqual(self.Board.valid(), False)

        for line in self.Board.rows + self.Board.cols:
            line.gencombs()
        self.assertEqual(self.Board.valid(), True)

        for line in self.Board.rows + self.Board.cols:
            line.combs = []
        self.assertEqual(self.Board.valid(), False)

    # TODO: def test_dump(self):

    def test_load(self):
        self.Board.solved = {}
        self.Board.load('core/unittests/load.txt')
        result = dicttolists(self.Board.solved, 10)
        expected = ['@...@@...@',
                    '@...@*...*',
                    '**..@*@@@*',
                    '**@@@*@..@',
                    '@...@**..*',
                    '@@@@@**@@@',
                    '@...@@...@',
                    '***@@****@',
                    '@.@@@@@@@@',
                    '@.********']
        self.assertEqual(result, expected)
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBoard))


if __name__ == '__main__':
    unittest.main()
