
#! /usr/bin/env python3

import unittest
from ..puzzle import Line, Board, _BLK, _EMP, _UNK
from ..tools import gridtodict, dicttolists

class TestLine(unittest.TestCase):
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
        self.assertEqual(l1.gaps, (0, 1, 1, 0))
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

    def test_combcount(self):
        l1 = Line(pos=9, orient='col', length=20, numbers=[0])
        self.assertEqual(l1.combcount(), 1)

        l2 = Line(pos=9, orient='col', length=20, numbers=[20])
        self.assertEqual(l2.combcount(), 1)

        l3 = Line(pos=9, orient='col', length=20, numbers=[5])
        self.assertEqual(l3.combcount(), 16) # Calculated with fingers

        l4 = Line(pos=9, orient='col', length=20, numbers=[1, 2, 3, 4])
        self.assertEqual(l4.combcount(), 330) # Calculated by hand

    def test_updated_combs(self):


        solved = ['......@@@.',
                  '@.@@.@@.@.',
                  '.@....@.@.',
                  '@....@@@@@',
                  '.....@...@',
                  '.....@@@.@',
                  '.....@@@.@',
                  '.....@@@.@',
                  '.....@...@',
                  '.....@@@@@' ]
        solved = gridtodict(solved)
    
        # Actually only pos and orient matter
        c1 = Line(pos=9, orient='col', length=10, numbers=[0])
        combs1 = ['...@@@@@@@',
                  '...@@..@@@',]
        c1.combs = combs1[:]
        solved_line = [solved.get(xy, _UNK) for xy in c1.coords()]
        filtered = c1.updated_combs(solved_line)
        self.assertItemsEqual(filtered, combs1[:1])

    def test_findfixed(self):
        initialcombs = ['@@..@@@.@@',
                        '@@@..@@.@.',
                        '@...@@@@@@',
                        '@@....@@@@',
                        '@@@.@..@@@']
        
        c1 = Line(pos=2, orient='col', length=10, numbers=[0])
        c1.combs = initialcombs
        solved_line = [_UNK for coords in c1.coords()]
        changed = c1.findfixed(solved_line)
        self.assertEqual(changed, [
                                   ((2, 0), _BLK),
                                   ((2, 3), _EMP),
                                   ((2, 8), _BLK),
                                  ]
                        )

        r1 = Line(pos=2, orient='row', length=10, numbers=[0])
        r1.combs = initialcombs
        solved_line = [_UNK for coords in r1.coords()]
        changed = r1.findfixed(solved_line)
        self.assertEqual(changed, [
                                   ((0, 2), _BLK),
                                   ((3, 2), _EMP),
                                   ((8, 2), _BLK),
                                  ]
                        )


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
    suite.addTest(unittest.makeSuite(TestLine))
    suite.addTest(unittest.makeSuite(TestBoard))

if __name__ == '__main__':
    unittest.main()
