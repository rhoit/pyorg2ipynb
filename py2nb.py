#!/usr/bin/env python3

import sys
import tokenize
import nbformat.v4 as nbf4

import re

FILE = sys.argv[1]

nb_cells = []
buffer = list()
buffer_token = set()
pline = -1
flag_cl = False  # line comment flag
flag_pcl = False # previous line comment flag
flag_il = False  # line indent flag

for token in tokenize.tokenize(open(FILE, 'rb').readline):
    

    if token.end == (0, 0): continue # auto encoding
    if token.start[0] == 1 and token.line.startswith('#!'): continue # auto encoding
    if token.start[1] != 0 : continue 
    if token.type in [4, 58]: continue # line break

    
    flag_pcl = flag_cl
    flag_cl = token.type == 57
    flag_il = token.type in [5, 6]

    print(token)

    if flag_pcl:
        if not flag_cl:
            block = "".join(buffer).strip()
            buffer.clear()
            nb_cells.append(nbf4.new_markdown_cell(source=block.replace("#", "").replace("*", "#")))
    else:
        if not flag_il:
            block = "".join(buffer).strip()
            buffer.clear()
            nb_cells.append(nbf4.new_code_cell(source=block))

    buffer.append(token.line)
 
else:
    nb_cells.append(nbf4.new_code_cell(source="".join(buffer).strip()))


with open(FILE.split(".")[0]+".ipynb", 'w') as fp:
    nbook = nbf4.new_notebook(cells=nb_cells)
    fp.write(nbf4.writes(nbook))
