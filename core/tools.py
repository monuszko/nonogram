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

def inserteveryfifth(lst, item):
    '''
    Inserts the second argument after every fifth element of the list.

    lst  - the list to be modified 
    item - item to insert
    '''

    newlst = lst[:]
    insertion_points = [x for x in range(len(newlst)) if x % 5 == 0 and x != 0]
    for i in reversed(insertion_points):
        newlst.insert(i, item)
    return newlst

def rotated_lists(list_of_lists, reverse=False):
    '''
    Rotates the lists right, or left if reverse is True

    Example:
    [
    [1, 2, 3]
    [4, 5, 6]
    ]

    becomes:
    [
    [1, 4]
    [2, 5]
    [3, 6]
    ]
    '''
    if reverse:
        list_of_lists.reverse()
    return [list(ls) for ls in zip(*list_of_lists)]

def binomial_coefficient(n, k):
    '''
    Calculate a binomial coefficient.
    '''
    result = 1
    for i in range(1, k + 1):
        result = result * (n - i + 1) // i
    return result 

def gridtodict(lst, ignored='*'):
    '''
    ignored - this character will be skipped

    Converts a grid in the form of a list of strings:
    [row1,
     row2,
     row3]

    ... to a dictionary: {(0, 0): char, (0, 1): char, ...}

    '''
    ret = dict()
    for y, line in enumerate(lst):
        for x, char in enumerate(line):
            if char in ignored:
                continue
            ret[(x, y)] = char
    return ret

