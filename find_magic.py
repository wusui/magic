# Copyright (C) 2025 Warren Usui, MIT License
"""
Call find_solution for a range of numbers
"""
import os
from time import sleep, time
from math import sqrt
from functools import partial
import pyprimesieve
from find_solution import find_solution

def find_centers(range_low, range_hi):
    """
    Loop through a range of center values. Find center values that are square roots
    of odd numbers whose prime factors are all 1 mod(4).  Call find_solution for each
    possible center value.
    """
    timer = time() + 60
    primet = pyprimesieve.primes(int(sqrt(range_hi)))
    plus_3 = list(filter(lambda a: a % 4 == 3, primet))
    for indx in range(range_low // 4 * 4 + 1, range_hi, 4):
        def is_not_mod1(lindx, ivalue):
            return lindx % ivalue == 0
        if len(list(filter(partial(is_not_mod1, indx), plus_3))) > 0:
            continue
        find_solution(indx)
        if time() > timer:
            print(f'sleeping: {indx}')
            with open('Checkpoint.log', 'w', encoding='utf-8') as fd_chk:
                fd_chk.write(str(indx))
            sleep(60)
            timer = time() + 60

def find_magic():
    """
    Read Checkpoint.log to see how far previous checks have run.
    Look over the next million center values for possible solutions.
    Pas thre range of center square roots to find_centers
    """
    starttime = time()
    million = 1000000
    fstart = million
    if os.path.exists('Checkpoint.log') and os.access('Checkpoint.log', os.R_OK):
        with open('Checkpoint.log', 'r', encoding='utf-8') as fd_chk:
            fstart = int(fd_chk.read())
    find_centers(fstart, fstart + million)
    print(time() - starttime)

if __name__ == "__main__":
    find_magic()
