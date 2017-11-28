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

COMBINATION_LIMIT = 2000000
_UNK = '*' # Unknown square
_EMP = '.' # Empty square
_BLK = '@' # Black square

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
        
        # Each element equals to the MINIMUM possible width:
        self.gaps = tuple([0] + [1] * (len(self.numbers) - 1) + [0])

        # Sequences of marked squares are fixed. There must be at least 1 space
        # between sequences. Number of floating spaces calculated below:
        self.fspaces = self.length - (len(self.numbers) - 1+sum(self.numbers))
        self.combs = [] # List of strings like @@@@...@@....


    def copy(self):
        '''
        Returns a copy of the the line.
        '''
        new = Line(self.pos, self.orient, self.length, self.numbers)
        new.combs = self.combs[:]
        return new

    def __eq__(self, other):
        for attr in 'numbers pos orient length gaps fspaces combs'.split():
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __str__(self):
        '''
        Debug printing method.
        '''
        s = []
        for c in self.combs:
            s.append(c)

        for field in 'numbers pos length gaps'.split():
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
            self.combs = [_EMP * self.length]
            return

        # In practice, to generate a list of solutions for each list of numbers
        # I only need to care about the distribution of spaces between gaps
        # (around sequences of marked squares). In math this is called
        # "combinations with repetitions".
        
        # For each floating space I generate a gap index. A list of such
        # indices will represent a way to distribute spaces around fixed 
        # sequences. So if I want to distribute 18 spaces, that will be a list
        # of 18 indices. Then I will use a list of indices to fill blanks 
        # between sequences.

        spacedistrib = comb_repl(range(len(self.gaps)), self.fspaces)

        for distrib in spacedistrib:

            allocated = list(self.gaps)
            for gapindex in distrib:
                allocated[gapindex] += 1

            comb = _EMP * allocated[0] # First space in combination
            for block, space in zip(self.numbers, allocated[1:]):
                comb += ((block * _BLK) + (space * _EMP))
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
        n = len(self.gaps) # ...split between n gaps
        
        if sum(self.numbers) == 0:
            return 1
        if sum(self.numbers) + (len(self.numbers) - 1) == self.length:
            return 1

        ret = tools.binomial_coefficient(n + k - 1, k)
        return ret


    def i_to_xy(self, i):
        if self.orient == 'row':
            return (i, self.pos)
        return (self.pos, i)


    def updated_combs(self, solved_line):

        solved_indices = [i for i, ch in enumerate(solved_line) if ch != _UNK]

        newcombs = []
        for comb in self.combs:
            for ind in solved_indices:
                if comb[ind] != solved_line[ind]:
                    break
            else:
                newcombs.append(comb)

        return newcombs


    def findfixed(self, solved):
        '''
        1. Loads the dictionary of solved squares
        2. Discards combinations not valid with already solved squares
        3. Checks for new squares that are always the same in all combinations
        and puts them back in dictionary of solved squares.

        solved - the dictionary of solved squares
        '''
        solved_line = []
        for i in range(self.length):
            coords = self.i_to_xy(i)
            solved_line.append(solved.get(coords, _UNK))

        # First, remove combinations invalidated by already known squares:
        self.combs = self.updated_combs(solved_line)

        # Second, check if a square has the same 'color' in all combinations:
        changed = []
        if not self.combs:
            return changed

        for i in range(self.length):
            if solved_line[i] != _UNK:
                continue

            for comb in self.combs:
                if comb[i] != self.combs[0][i]:
                    break
            else:
                coords = self.i_to_xy(i)
                solved[(coords)] = comb[i]
                changed.append((coords))

        return changed

class Board:
    '''
    Represents a board consisting of rows and columns. Provides high-level
    methods.
    '''
    def __init__(self, rows, cols):
        # Load rows, cols and produce some metadata:
        self.rows = []
        self.cols = []
        self.solved = dict()
        self.height = len(rows)
        self.width  = len(cols)
        for nr, row in enumerate(rows):
            self.rows.append(Line(nr, 'row', self.width, row))
        for nr, col in enumerate(cols):
            self.cols.append(Line(nr, 'col', self.height, col))
        self.backups = [] # For guessing (contradictions)

    def isfull(self):
        '''
        Returns true if all squares have been determined
        '''
        return len(self.solved) == self.height * self.width


    def display(self, no_grouping=False, no_hints=False, 
                                               legend='*.@', separators='|-+'):
        '''
        A hopelessly complex line-based display method

        no_grouping - don't display as 5x5 squares 
        no_hints    - don't print line hints
        legend      - a length 3 string, (unkown, empty, black)
        separators  - a length 3 string (horizontal, vertical, crossing)
        '''
        VSEP, HSEP, CSEP = separators[0], separators[1], separators[2]

        lines = []
        for y in range(self.height):
            # The core part of the line
            # .....@@@@@..@.@...@@.....
            line = []
            for x in range(self.width):
                if (x, y) in self.solved:
                    if self.solved[(x, y)] == _EMP:
                        line.append(legend[1])
                    else:
                        line.append(legend[2]) # Black square
                else:
                    line.append(legend[0]) # Unknown square
            lines.append(line)

        if not no_grouping:
            # .....|@@@@@|..@.@|...@@|.....
            lines = [tools.inserteveryfifth(line, VSEP) for line in lines]

            horsep =  [HSEP] * self.width
            horsep = tools.inserteveryfifth(horsep, CSEP)
            lines  = tools.inserteveryfifth(lines, horsep)
        lines = [''.join(line) for line in lines]

        if not no_hints:
            # 5, 1, 1, 2 .....|@@@@@|..@.@|...@@|.....
            # ROW hints:
            row_hints = [r.strnums() for r in self.rows]
            longest = max(len(h) for h in row_hints)
            row_hints = [hint.rjust(longest) + ' ' for hint in row_hints]
            if not no_grouping:
                row_hints = tools.inserteveryfifth(row_hints, 
                                                            ' ' * (longest +1))
            lines = [h + l for h, l in zip(row_hints, lines)]

            # COLUMN hints:
            linewidth = len(lines[0])
            col_extras = [c.strnums() for c in self.cols]
            longest_hint = max(len(c) for c in col_extras)
            col_extras = [c.rjust(longest_hint) for c in col_extras]
            if not no_grouping:
                col_extras = tools.inserteveryfifth(col_extras, 
                                                          [' '] * longest_hint)
            col_extras = tools.rotated_lists(col_extras)
            col_extras = [''.join(c).rjust(linewidth) for c in col_extras]
            col_extras.append(' ' * linewidth)
            lines = col_extras + lines

        for line in lines: 
            print(line)

    def basicsolve(self):
        '''
        The straightforward solving method.
        Check each row and column at least once. If a square is solved,
        add the corresponding perpendicular line (row if column, column if row)
        to the queue of lines to check. Repeat for as long as progress is made.
        '''
        initially_solved = len(self.solved)
        tocheck = self.rows + self.cols # A list
        while len(tocheck) > 0:
            line = tocheck.pop()
            changed = line.findfixed(self.solved)
            for square in changed:
                x, y = square[0], square[1]
                if line.orient == 'row':
                    if self.cols[x] not in tocheck:
                        tocheck.insert(0, self.cols[x])
                if line.orient == 'col':
                    if self.rows[y] not in tocheck:
                        tocheck.insert(0, self.rows[y])
        return len(self.solved) > initially_solved

    def memorysafe(self):
        '''
        Return false if sum of row and column combinations exceeds the static
        limit.
        '''
        sum_of_combs = sum(c.combcount() for c in self.rows + self.cols)
        if sum_of_combs > COMBINATION_LIMIT:
            return False
        return True

    def solve(self, no_hints=False, legend='*.@', 
            separators='|-+', no_grouping=False, hide_progress=False):
        '''
        The master solve method calling lesser methods.
        '''

        for line in self.rows + self.cols:
            line.gencombs()

        progress = True # don't assume everything is solvable with this program
        while progress:
            if not hide_progress:
                print('Straightforward attempt...')
            progress = self.basicsolve()
            if not self.valid():
                break
            if progress and not hide_progress:
                self.display(no_grouping, no_hints, legend, separators)
            if self.isfull(): # To avoid the single unneeded guess
                break
            if not hide_progress:
                print('Attempting contradiction...')
            guess = self.keepguessing()
            if guess is not None:
                progress = True
                x, y, color = guess[0][0] + 1, guess[0][1] + 1, guess[1]
                if not hide_progress:
                    print('From contradiction: ({0}, {1}) is "{2}"'.format(
                                                                 x, y, color))
                self.solved[guess[0]] = guess[1]

    def verdict(self):
        '''
        Print the status of the board at the end of solving.
        '''
        
        if self.valid():
            self.display(no_grouping=True, legend='* #', no_hints=True)
            if self.isfull():
                print("{0} out of {1} squares solved.".format(
                           len(self.solved), self.width * self.height))
            else:
                unsolved = self.width * self.height - len(self.solved)
                print("{0} out of {1} squares left.".format(unsolved,
                                                   self.width * self.height))
        else:
            self.display(no_grouping=True, legend='* #', no_hints=True)
            print('The puzzle has no solutions !')

    def singleguess(self, xy, color):
        '''
        A single attempt at guessing: assume the given square is black/empty.
        Then keep solving normally and see where it leads. If there's
        a contradiction, GOOD, restore the board from last save and the square
        is the opposite of guess. If there's no contradiction, simply restore.

        'xy' - a tuple of coordinates
        'color' should be _BLK or _EMP (Black or empty).

        Returns True if the board remains valid after the guess.
        Returns False if the guess produces a condradiction.
        '''

        self.save()
        self.solved[xy] = color
        self.basicsolve()
        ret = self.valid()
        self.restore()
        return ret

    def keepguessing(self):
        '''
        A sequence of guesses to uncover a contradiction and determine a single
        square this way.

        Returns:
        ((x, y), color) if found a contradiction
        None - if not found 
        '''
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.solved:
                    if not self.singleguess((x, y), _BLK): #Contradiction
                        return ((x, y), _EMP)
                    if not self.singleguess((x, y), _EMP): #Contradiction
                        return ((x, y), _BLK)
        return None


    def save(self):
        '''
        Saves the current state of 'solved', 'rows', and 'cols' in 'backups'.
        Performed before attempting to guess.
        '''
        solved = dict.copy(self.solved)
        #rows = copy.deepcopy(self.rows)  # deepcopy is supposedly WRONG
        rows = [r.copy() for r in self.rows]
        #cols = copy.deepcopy(self.cols)  # and EVIL
        cols = [c.copy() for c in self.cols]
        self.backups.append((solved, rows, cols))

    def restore(self):
        '''
        Restores self.solved, self.rows, self.cols after a guess.
        '''
        backup = self.backups.pop()
        self.solved, self.rows, self.cols = backup[0], backup[1], backup[2]

    def valid(self):
        '''
        A board is valid if all of its rows and columns are valid.
        Used for guessing.
        '''
        if all(l.valid() for l in self.rows + self.cols): # Assumes lists !
            return True
        return False

    def dump(self, path):
        '''
        Dumps the solved squares to a file. 
        '''
        f = open(path, 'w')

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.solved:
                    f.write(self.solved[(x, y)])
                else:
                    f.write(_UNK)
            f.write('\n')
        f.close()

    def load(self, path):
        '''
        Loads solved squares from a file. Use before attempting to solve.
        '''
        f = open(path, 'r')
        for y, line in enumerate(f):
            for x, char in enumerate(line):
                if char in (_EMP, _BLK):
                    self.solved[(x, y)] = char
                elif char == _UNK:
                    continue
        f.close()

