#! /usr/bin/env python3

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
import argparse, sys, re, os.path
import core.puzzle

def parseargs():
    '''
    Parses commandline arguments.
    '''
    desc = {
            'filename': 'a file containing a nonogram',
            '-p': 'disables progress displays and messages',
            '-g': 'enables grouping rows and columns by five for progress',
            '-n': 'disables both row and column hint numbers',
            '-l': 'characters used for unkown, empty, and black squares, '
                                                              '(default: *.@)',
            '-s': 'characters used for vertical, horizontal, and cross-section'
                                                  ' separators (default: |-+)',
            '-d': 'disables caching of progress (for multiple solutions)',
            '-f': 'prevents use of existing cache files'
           }

    parser = argparse.ArgumentParser(description='Solve a nonogram.',
             epilog='''If there are multiple solutions, the program saves 
                    100% sure squares in a cache/*.sav file. You can edit it
                    manually and set an unknown square (*) to empty (.)
                    or (black). On the next run the program will use
                    your assumption.'''
                    )

    # I force defaults to None  
    # I want to actually use the defaults from .solve().
    parser.add_argument('filename', type=str, help=desc['filename'])
    parser.add_argument('-p', '--hide-progress', action='store_true', 
                                                 default=None, help=desc['-p'])
    parser.add_argument('-g', '--no-grouping', action='store_true', 
                                                 default=None, help=desc['-g'])
    parser.add_argument('-n', '--no-hints', action='store_true', 
                                                 default=None, help=desc['-n'])
    parser.add_argument('-l', '--legend', metavar='ueb', help=desc['-l'])      
    parser.add_argument('-s', '--separators', metavar='vhc', help=desc['-s'])
    parser.add_argument('-d', '--dont-save', action='store_true', 
                                                 default=None, help=desc['-d'])
    parser.add_argument('-f', '--from-scratch', action='store_true', 
                                                 default=None, help=desc['-f'])
    ardict = vars(parser.parse_args())
    ardict = {k : v for k, v in ardict.items() if v is not None}
    solveargs = ardict.copy()
    solveargs = {k : v for k, v in solveargs.items() 
             if k not in ('filename', 'from_scratch', 'dont_save')}

    for arg in ('legend', 'separators'):
        if arg in ardict and len(ardict[arg]) != 3:
            print('{0}: error: "{1}" must be 3 characters long.'.format(
                                                             sys.argv[0], arg))
            sys.exit(1)
    return (ardict, solveargs)

def formatcheck(lines):
    '''
    Checks if the input data is in the correct format.
    '''
    # Patterns for data format check.
    misc = '^([Rr]ows:|[Cc]ols:|[Cc]olumns:)$'
    # ...a single 0 or numbers separated by comma, commaspace, or space:
    numbers = '^(0|[1-9][0-9]*)((,|, | )[1-9][0-9]*)*$'
    for line in lines:
        unchanged = line
        line = line.partition('#')[0]
        if line.isspace() or line == '':
            continue
        if not re.match(misc, line) and not re.match(numbers, line):
            print('{0}: error: bad input line format: {1}'.format(
                                                       sys.argv[0], unchanged))
            sys.exit(1)

def parselines(lines):
    '''
    Parses data from the input file.
    '''
    rows = []
    cols = []
    for line in lines:
        line = line.partition('#')[0] # Handles comments
        if line.lower().startswith('rows:'): 
            mode = 'rows'
        elif line.lower().startswith(('cols:', 'columns:')): 
            mode = 'cols'
        elif line.isspace() or line == '':
            continue
        else:
            hint = line.replace(',', ' ').split()
            hint = [int(num) for num in hint]
            if mode == 'rows':
                rows.append(hint)
            elif mode == 'cols':
                cols.append(hint)
    return (rows, cols)

def consistencycheck(rows, cols):
    '''
    Verifies *logical* consistency of the input data.
    '''
    if not rows:
        print('{0}: error: no input *rows*.'.format(sys.argv[0]))
        sys.exit(1)
    if not cols:
        print('{0}: error: no input *columns*.'.format(sys.argv[0]))
        sys.exit(1)
    for line in rows:
        if sum(line) + len(line) - 1 > len(cols):
            print('{0}: error: row {1} too long.'.format(sys.argv[0], line))
            sys.exit(1)
    for line in cols:
        if sum(line) + len(line) - 1 > len(rows):
            print('{0}: error: column {1} too long.'.format(sys.argv[0], line))
            sys.exit(1)
    sumofcols = sum(sum(col) for col in cols) 
    sumofrows = sum(sum(row) for row in rows) 
    if sumofcols != sumofrows: # Would probably cover all of the above
        print("{0}: error: sum of cols doesn't equal sum of rows".format(
                                                                  sys.argv[0]))
        sys.exit(1)

if __name__ == '__main__':

    ardict, solveargs = parseargs()

    puzzlepath = ardict['filename']
    if not os.path.isfile(puzzlepath):
        print('{0}: error: file {1} not found'.format(sys.argv[0], puzzlepath))
        sys.exit(1)
    dumppath = puzzlepath.replace('puzzles', 'cache').replace('txt', 'sav')

    f = open(puzzlepath)
    lines = f.readlines()
    f.close()

    formatcheck(lines)
    rows, cols = parselines(lines)
    consistencycheck(rows, cols)

    # SOLVING !!!!
    board = core.puzzle.Board(rows, cols)
    if not 'from_scratch' in ardict.keys() and os.path.isfile(dumppath):
        board.load(dumppath)
    if not board.memorysafe():
        print('{0}: error: combination limit exceeded'.format(sys.argv[0]))
        sys.exit(1)
    board.solve(**solveargs)
    if not 'dont_save' in ardict.keys() and not board.issolved():
        board.dump(dumppath)
