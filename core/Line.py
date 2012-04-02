#! /usr/bin/env python3
#
#    Nonogram solver 
#    written for Python 3.2
#    Copyright (C) 2012 Marek Onuszko
#    marek.onuszko@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division, print_function
from itertools import combinations_with_replacement as comb_repl
import core.tools as tools
import core.constants as cons
import copy

COMBINATION_LIMIT = 2000000

class Line:
    '''
    Represents possible combinations for a row or column.
    '''
    def __init__(self, pos, orient, length, numbers):
        # Input data:
        self.numbers = numbers # a sequence of numbers or a single 0 
        self.pos = pos         # position relative to other rows/cols
        self.orient = orient   # 'row' or 'col'
        self.length = length   # Number of squares in the line
        
        # n-1 zones between @@@ @@, +2 for left and right which MAY have spaces
        self.zones = tuple([0] + [1] * (len(self.numbers) - 1) + [0])

        # Sequences of marked squares are fixed. There must be at least 1 space
        # between sequences. Number of floating spaces calculated below:
        self.fspaces = self.length - (len(self.numbers) - 1+sum(self.numbers))
        self.combs = [] # List of strings like @@@@...@@....

    def __str__(self):
        '''
        Debug printing method.
        '''
        s = []
        for c in self.combs:
            s.append(c)

        for field in 'numbers pos length zones'.split():
            s.append('{0}: {1}'.format(field, getattr(self, field)))
        s = '\n'.join(s)
        return s

    def strnums(self, sep=' '):
        '''
        Returns row/columns hint numbers as a list of strings
        '''
        return sep.join([str(nr) for nr in self.numbers])

    def gencombs(self):
        ''' 
        Transforms the input numbers into a list of possible combinations
            made of sequences of marked squares and spaces and places them in
            self.combs. Example below:

            ...########....########. (one of solutions for a 8, 8 row)
        '''

        if sum(self.numbers) == 0:
            self.combs = [cons._EMP * self.length]
            return

        # In practice, to generate a list of solutions for each list of numbers
        # I only need to care about the distribution of spaces between zones
        # (around sequences of marked squares). In math this is called
        # "combinations with repetitions".
        
        # For each floating space I generate a zone index. A list of such
        # indices will represent a way to distribute spaces around fixed 
        # sequences. So if I want to distribute 18 spaces, that will be a list
        # of 18 indices. Then I will use a list of indices to fill blanks 
        # between sequences.

        spacedistrib = comb_repl(range(len(self.zones)), self.fspaces)

        for distrib in spacedistrib:

            allocated = list(self.zones)
            for zoneindex in distrib:
                allocated[zoneindex] += 1

            comb = cons._EMP * allocated[0] # First space in combination
            for block, space in zip(self.numbers, allocated[1:]):
                comb += ((block * cons._BLK) + (space * cons._EMP))
            self.combs.append(comb)

    def valid(self):
        '''
        Return True if the row has possible combinations. Used for guessing.
        '''
        if self.combs:
            return True
        return False

    def combcount(self):
        '''
        Return the number of combinations possible with self.numbers
        '''
        k = self.fspaces    # k spaces...
        n = len(self.zones) # ...split between n zones 
        
        if sum(self.numbers) == 0:
            return 1
        if sum(self.numbers) + (len(self.numbers) - 1) == self.length:
            return 1

        ret = tools.binomial_coefficient(n + k - 1, k)
        return ret

    def fits(self, comb, solved):
        '''
        Checks if a combination string fits with the dict of solved squares.

        comb   - a combination string
        solved - the dictionary of solved squares
        '''
        if not solved:
            return True
        for i in range(self.length):
            if self.orient == 'row':
                x, y = i, self.pos
            else:
                x, y = self.pos, i

            if (x, y) in solved:
                if comb[i] != solved[(x, y)]:
                    return False
        return True

    def findfixed(self, solved):
        '''
        1. Loads the dictionary of solved squares
        2. Discards combinations not valid with already solved squares
        3. Checks for new squares that are always the same in all combinations
        and puts them back in dictionary of solved squares.

        solved - the dictionary of solved squares
        '''

        # First, remove combinations invalidated by already known squares:
        self.combs = [c for c in self.combs if self.fits(c, solved)]

        # Second, check if a square has the same 'color' in all combinations:
        changed = []
        for i in range(self.length):
            if self.orient == 'row':
                x, y = i, self.pos
            else:
                x, y = self.pos, i

            if (x, y) not in solved:
                char = set([comb[i] for comb in self.combs]) #i-th squares
                if len(char) == 1:
                    char = char.pop()
                    solved[(x, y)] = char 
                    changed.append((x, y))
        return changed

