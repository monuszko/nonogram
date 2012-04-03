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
from   core.Line import Line

COMBINATION_LIMIT = 2000000

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
                    if self.solved[(x, y)] == cons._EMP:
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
        'color' should be cons._BLK or cons._EMP (Black or empty).

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
                    if not self.singleguess((x, y), cons._BLK): #Contradiction
                        return ((x, y), cons._EMP)
                    if not self.singleguess((x, y), cons._EMP): #Contradiction
                        return ((x, y), cons._BLK)
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
                    f.write(cons._UNK)
            f.write('\n')
        f.close()

    def load(self, path):
        '''
        Loads solved squares from a file. Use before attempting to solve.
        '''
        f = open(path, 'r')
        for y, line in enumerate(f):
            for x, char in enumerate(line):
                if char in (cons._EMP, cons._BLK):
                    self.solved[(x, y)] = char
                elif char == cons._UNK:
                    continue
        f.close()

