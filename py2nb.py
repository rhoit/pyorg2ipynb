#!/usr/bin/env python3

import sys
import tokenize
import nbformat.v4 as nbf4

import re

FILE = sys.argv[1]

nb_cells = []
flag_nl, buffer, pline = 0, list(), -1
buffer_token = set()

for token in tokenize.tokenize(open(FILE, 'rb').readline):
    
    # print(token)

    if token.end == (0, 0): continue # auto encoding
    if token.start[0] == 1 and token.line.startswith('#!'): continue # auto encoding
    if token.type == 4: continue # line break

    if token.start[0] > pline: buffer.append(token.line)
    buffer_token.add(token.type)
    pline = token.start[0]

    # if token.type == 57: # comment
    #     if re.search('^# \*+ ', token.line):
    #         buffer.pop()
    #         block = "".join(buffer).strip()
    #         if block: nb_cells.append(nbf4.new_code_cell(source=block))
    #         heading = token.line.replace('*', '#')
    #         nb_cells.append(nbf4.new_markdown_cell(source=heading.strip()))
    #         buffer.clear()
    #

    if token.type == 58: # new line
        if flag_nl < 1: flag_nl += True; continue
        comment_block = buffer_token.issubset({57,58})
        block = "".join(buffer).strip()
        buffer.clear()
        buffer_token.clear()
        if block:
            if comment_block:
                nb_cells.append(nbf4.new_markdown_cell(source=block.replace("#", "").replace("*", "#")))
            else:
                nb_cells.append(nbf4.new_code_cell(source=block))
        continue

    flag_nl = False
else:
    nb_cells.append(nbf4.new_code_cell(source="".join(buffer).strip()))


with open("out.ipynb", 'w') as fp:
    nbook = nbf4.new_notebook(cells=nb_cells)
    fp.write(nbf4.writes(nbook))
