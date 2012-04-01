
#! /usr/bin/env python3

import unittest
from ..puzzle import *
from ..tools import gridtodict

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

    def test_combcount(self):
        l1 = Line(pos=9, orient='col', length=20, numbers=[0])
        self.assertEqual(l1.combcount(), 1)

        l2 = Line(pos=9, orient='col', length=20, numbers=[20])
        self.assertEqual(l2.combcount(), 1)

        l3 = Line(pos=9, orient='col', length=20, numbers=[5])
        self.assertEqual(l3.combcount(), 16) # Calculated with fingers

        l4 = Line(pos=9, orient='col', length=20, numbers=[1, 2, 3, 4])
        self.assertEqual(l4.combcount(), 330) # Calculated by hand

    def test_fits(self):


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
        self.assertEqual(c1.fits('...@@@@@@@', solved), True)
        self.assertEqual(c1.fits('...@@..@@@', solved), False)

        c2 = Line(pos=4, orient='col', length=10, numbers=[0])
        self.assertEqual(c2.fits('..........', solved), True)
        self.assertEqual(c2.fits('..@...@...', solved), False)

        r1 = Line(pos=4, orient='row', length=10, numbers=[0])
        self.assertEqual(r1.fits('.....@...@', solved), True)
        self.assertEqual(r1.fits('@.@.@.@.@.', solved), False)

        r2 = Line(pos=0, orient='row', length=10, numbers=[0])
        self.assertEqual(r2.fits('......@@@.', solved), True)
        self.assertEqual(r2.fits('.@....@@@.', solved), False)

        solved2 = ['.*.*****@.',
                   '@.@@******',
                   '***...@.**',
                   '@.*****@@@',
                   '***.****.@',
                   '**...@****',
                   '.******@**',
                   '.....@@@**',
                   '.....@...@',
                   '.....@@@@@' ]
        solved2 = gridtodict(solved2)

        c1 = Line(pos=2, orient='col', length=10, numbers=[0])
        self.assertEqual(c1.fits('.@@@@.@...', solved2), True)
        self.assertEqual(c1.fits('.@.@......', solved2), True)
        self.assertEqual(c1.fits('...@......', solved2), False)
        self.assertEqual(c1.fits('.........@', solved2), False)
        self.assertEqual(c1.fits('..........', solved2), False)
        self.assertEqual(c1.fits('@@@@@@@@@@', solved2), False)

        c2 = Line(pos=9, orient='col', length=10, numbers=[0])
        self.assertEqual(c2.fits('...@@...@@', solved2), True)
        self.assertEqual(c2.fits('.@@@@..@@@', solved2), True)
        self.assertEqual(c2.fits('@..@@...@@', solved2), False)

        r1 = Line(pos=0, orient='row', length=10, numbers=[0])
        self.assertEqual(r1.fits('.@.@...@@.', solved2), True)
        self.assertEqual(r1.fits('........@.', solved2), True)
        #self.assertEqual(r1.fits('........@..', solved2), True) TODO: fix !
        self.assertEqual(r1.fits('..........', solved2), False)
        self.assertEqual(r1.fits('.@.@...@..', solved2), False)
        self.assertEqual(r1.fits('@@@@@@@@@@', solved2), False)

        r2 = Line(pos=1, orient='row', length=10, numbers=[0])
        self.assertEqual(r2.fits('@.@@......', solved2), True)
        self.assertEqual(r2.fits('@.@@@@@@@@', solved2), True)
        self.assertEqual(r2.fits('@..@......', solved2), False)
        self.assertEqual(r2.fits('@@@@......', solved2), False)

    def test_findfixed(self):
        initialcombs = ['@@..@@@.@@',
                        '@@@..@@.@.',
                        '@...@@@@@@',
                        '@@....@@@@',
                        '@@@.@..@@@']
        
        # Test the 'find new squares' functionality:
        solved = dict()
        c1 = Line(pos=2, orient='col', length=10, numbers=[0])
        c1.combs = initialcombs
        self.assertEqual(c1.findfixed(solved), [(2, 0), (2, 3), (2, 8)])
        self.assertEqual((solved), {(2, 0): '@', (2, 3): '.', (2, 8): '@'})

        solved2 = dict()
        r1 = Line(pos=2, orient='row', length=10, numbers=[0])
        r1.combs = initialcombs 
        self.assertEqual(r1.findfixed(solved2), [(0, 2), (3, 2), (8, 2)])
        self.assertEqual((solved2), {(0, 2): '@', (3, 2): '.', (8, 2): '@'})

        # Test the 'discard unfitting combinations' functionality:
        solved3 = {(5, 1): '@'}
        c2 = Line(pos=5, orient='col', length=10, numbers=[8])
        c2.combs = initialcombs
        self.assertEqual(c2.findfixed(solved3), [(5, 0), (5, 3), (5, 8)])

        self.assertEqual(c2.combs, ['@@..@@@.@@',
                                    '@@@..@@.@.',
                                   #'@...@@@@@@', automatically removed
                                    '@@....@@@@',
                                    '@@@.@..@@@'])
        
        solved4 = {(4, 6): '.'}
        r2 = Line(pos=6, orient='row', length=10, numbers=[8])
        r2.combs = initialcombs
        self.assertEqual(r2.findfixed(solved4), [(0, 6), (1, 6), (3, 6), (6, 6), (8, 6)])
        self.assertEqual(r2.combs,  [#'@@..@@@.@@', automatically removed
                                      '@@@..@@.@.',
                                     #'@...@@@@@@', automatically removed
                                      '@@....@@@@',
                                     #'@@@.@..@@@'  automatically removed
                                     ])

        # Two squares at the same time
        solved5 = {(1, 7): '@', (7, 7): '@'}
        r3 = Line(pos=7, orient='row', length=10, numbers=[2,3])
        r3.combs = initialcombs
        self.assertEqual(r3.findfixed(solved5), [(0, 7), (3, 7), (5, 7), (8, 7), (9, 7)])
        self.assertEqual(r3.combs, [#'@@..@@@.@@',
                                    #'@@@..@@.@.',
                                    #'@...@@@@@@',
                                    '@@....@@@@',
                                    '@@@.@..@@@'])
        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Testpuzzle))


if __name__ == '__main__':
    unittest.main()
