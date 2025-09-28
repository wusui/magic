# Copyright (C) 2025 Warren Usui, MIT License
"""
Given a center value, find possible magic square solutions with 6+ square numbers in
them.  Log any with 7+ square numbers.
"""
from math import sqrt
from itertools import combinations
from uuid import uuid4
import json

def get_threesomes(center_root):
    """
    return offsets from center of square values that would be found in a magic
    square solution

    center_root -- square root of center square
    """
    mid_point = center_root * center_root
    offset = center_root
    bottom = mid_point
    ret_parm = []
    while bottom > 0:
        offset += 1
        topp = offset * offset
        diffv = topp - mid_point
        bottom = mid_point - diffv
        if bottom > 0:
            rval = int(sqrt(bottom))
            if rval * rval == bottom:
                ret_parm.append([mid_point, topp - mid_point])
    return ret_parm

def is_not_magic(magic):
    """
    Return True if list of values sent do not for a magic square

    magic -- magic square solution with squares listed in row/column order.
    """
    tvalues = [sum(magic[0:3]), sum(magic[3:6]), sum(magic[6:9]),
               sum([magic[0], magic[4], magic[8]]),
               sum([magic[2], magic[4], magic[6]]),
               sum([magic[0], magic[3], magic[6]]),
               sum([magic[1], magic[4], magic[7]]),
               sum([magic[2], magic[5], magic[8]])]
    if len(set(tvalues)) != 1:
        print('Not Magic')
        return True
    return False

def checkout(magic):
    """
    Check for magic squares with at least six squares in it.  If a new
    non-Bremner magic square is found, write that square to Magic_log.json

    magic -- magic square as list in row/column order
    """
    if len(list(filter(lambda a: a > 0, magic))) != 9:
        return
    if len(list(set(magic))) != 9:
        return
    squares = list(filter(lambda a: int(sqrt(a)) * int(sqrt(a)) == a, magic))
    if len(squares) >= 6:
        print(magic)
    if len(squares) > 6:
        if magic[-2] % 529 == 0 and magic[-3] % 222121 == 0:
            return
        with open(f'Magic_log.{str(uuid4())}.json', 'a',
                    encoding='utf-8') as fd_sol:
            json.dump(magic, fd_sol, indent=4)
            if is_not_magic(magic):
                fd_sol.write('Not Magic')

def fill_sq(abc_vals):
    """
    Given Lucas square values passed in, create associated magic square and
    check if the square qualifies for a new solution.
    """
    apb = abc_vals[0] + abc_vals[1]
    bma = abc_vals[1] - abc_vals[0]
    aval = abc_vals[0]
    bval = abc_vals[1]
    cval = abc_vals[2]
    magic = [cval - bval, cval + apb, cval - aval, cval + bma, cval, cval - bma,
             cval + aval, cval - apb, cval + bval]
    checkout(magic)

def solv_it(combo, pattern):
    """
    For pair of combos listed, find a, b, and c Lucas square values based on
    the pattern passed
    """
    if pattern[0] == 'a':
        if pattern[1] == 'b':
            fill_sq([combo[0][1], combo[1][1], combo[0][0]])
        if pattern[1] == '+':
            if combo[1][1] <= 2 * combo[0][1]:
                return
            fill_sq([combo[0][1], combo[1][1] - combo[0][1], combo[0][0]])
        if pattern[1] == '-':
            fill_sq([combo[1][1], combo[0][1] + combo[1][1], combo[0][0]])
    if pattern[0] == '-':
        if pattern[1] == 'a':
            fill_sq([combo[1][1], combo[0][1] + combo[1][1], combo[0][0]])
        if pattern[1] == 'b':
            fill_sq([combo[1][1] - combo[0][1], combo[1][1], combo[0][0]])
        if pattern[1] == '+':
            aval = (combo[0][1] + combo[1][1]) // 2
            fill_sq([aval, combo[1][1] - aval, combo[0][0]])
    if pattern[0] == 'b':
        if pattern[1] == '+':
            fill_sq([combo[1][1] - combo[0][1], combo[0][1], combo[0][0]])

def find_solution(center_root):
    """
    Find magic square solutions where the center value is center_root^2

    center_root -- square root of center square
    """
    trips = get_threesomes(center_root)
    if len(trips) < 2:
        return
    for combo in list(combinations(trips, 2)):
        lcomb = combo
        if lcomb[0][-1] > lcomb[1][-1]:
            lcomb = lcomb[::-1]
        for solv_pat in [['a', 'b'], ['a', '+'], ['a', '-'], ['-', 'a'],
                         ['-', 'b'], ['-', '+'], ['b', '+']]:
            solv_it(lcomb, solv_pat)
