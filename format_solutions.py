# Copyright (C) 2025 Warren Usui, MIT License
"""
Format solutions for all local Magic files
"""
import os
import json
from uuid import uuid4
import pandas as pd

def mformat(sq_ints):
    """
    Save html file version of the magic square in a new Display file
    """
    def mk_sqs(sq_val):
        sqroot = int(sq_val ** .5)
        if sqroot * sqroot ==  sq_val:
            return f'{sqroot} ^ 2'
        return str(sq_val)
    rfmt = list(map(mk_sqs, sq_ints))
    dframe = pd.DataFrame({'x': rfmt[0:3], 'y': rfmt[3:6], 'z': rfmt[6:9]})
    html_table = dframe.to_html(index=False, header=False, escape=False)
    with open('template.html', 'r', encoding='utf-8') as fread:
        html_template = fread.read()
    html_out = html_template.replace('<!-- INSERT_TABLE_HERE -->', html_table)
    with open(f'Display.{str(uuid4())}.html', 'a', encoding='utf-8') as fd_sol:
        fd_sol.write(html_out)

def format_it():
    """
    Call mformats for all magic squares found in local Magic* files
    """
    for msquare in list(filter(lambda a: a.startswith('Magic'), os.listdir('.'))):
        with open(msquare, 'r', encoding='utf-8') as fd_sq:
            sq_ints = json.load(fd_sq)
            mformat(sq_ints)

if __name__ == "__main__":
    format_it()
