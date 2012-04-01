#! /usr/bin/env python3

import unittest
from ..tools import *

class Testtools(unittest.TestCase):
    """
    A test class for the tools module.
    """
    
    def test_insert(self):
        seq1 = range(6)
        seq2 = range(5)
        seq3 = range(0)
        seq4 = range(1)

        item = '*'

        self.assertEqual(inserteveryfifth(range(6), item), [0, 1, 2, 3, 4, '*', 5])
        self.assertEqual(inserteveryfifth(range(5), item), [0, 1, 2, 3, 4])
        self.assertEqual(inserteveryfifth(range(0), item), [])
        self.assertEqual(inserteveryfifth(range(1), item), [0])
        self.assertEqual(inserteveryfifth(range(16), item), [0, 1, 2, 3, 4, '*', 5, 6, 7, 8, 9, '*', 10, 11, 12, 13, 14, '*', 15])

    def test_rotated(self):
        lis1 = []
        lis2 = [[1, 2, 3, 4]]
        lis3 = [['a', 'b'], [[], '']]
        lis4 = [[1, 2, 3], ['a', 'b', 'c'], [None, False, True]]

        self.assertEqual(rotated_lists(lis1), [])
        self.assertEqual(rotated_lists(lis2), [[1], [2], [3], [4]])
        self.assertEqual(rotated_lists(lis3), [['a', []], ['b', '']])
        self.assertEqual(rotated_lists(lis3, reverse=True), [[[], 'a'], ['', 'b']])
        self.assertEqual(rotated_lists(lis4), [[1, 'a', None], [2, 'b', False], [3, 'c', True]])

    def test_binomial(self):
        self.assertEqual(binomial_coefficient(6, 1), 6)
        self.assertEqual(binomial_coefficient(9, 2), 36)
        self.assertEqual(binomial_coefficient(11, 5), 462)
        self.assertEqual(binomial_coefficient(1, 1), 1)

    def test_gridtodict(self):
        lines1 = ['r@2',
                  'fah',
                  'wjv']
        expected1 = {(0, 0): 'r', (1, 0): '@', (2, 0): '2',
                     (0, 1): 'f', (1, 1): 'a', (2, 1): 'h',
                     (0, 2): 'w', (1, 2): 'j', (2, 2): 'v'}
        self.assertEqual(gridtodict(lines1), expected1)

        lines2 = ['_.-=',
                  '*/\|', # Asterisk (*) should be skipped
                  '>:-)']
        expected2 = {(0, 0): '_', (1, 0): '.', (2, 0): '-',  (3, 0): '=',
                                  (1, 1): '/', (2, 1): '\\', (3, 1): '|',
                     (0, 2): '>', (1, 2): ':', (2, 2): '-',  (3, 2): ')'}
        self.assertEqual(gridtodict(lines2), expected2)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Testtools))


if __name__ == '__main__':
    unittest.main()
