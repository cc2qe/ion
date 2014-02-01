#!/usr/bin/env python

import argparse, sys
from argparse import RawTextHelpFormatter
import numpy as np

__author__ = "Colby Chiang (cc2qe@virginia.edu)"
__version__ = "$Revision: 0.0.1 $"
__date__ = "$Date: 2014-01-31 19:31 $"

# --------------------------------------
# define functions

def get_args():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description="\
rollingstats.py\n\
author: " + __author__ + "\n\
version: " + __version__ + "\n\
description: Calculate statistics on a numeric data column within a rolling window")
    #parser.add_argument('-a', '--argA', metavar='argA', type=str, required=True, help='description of argument')
    #parser.add_argument('-b', '--argB', metavar='argB', required=False, help='description of argument B')
    #parser.add_argument('-e', '--endrule', required=False, default='keep', choices=['keep', 'omit', 'constant', 'mean', 'median', 'min', 'max'], help='behavior at begining and end of the set.\n\'keep\' retains original values,\n\'omit\' drops them from the output\n\'constant\' copies the first and last informative values\n(default: keep)')
    parser.add_argument('-a', '--align', required=False, default='center', choices=['left', 'center', 'right'], help='alignment of the index with respect to the rolling window (default: center)')
    parser.add_argument('-e', '--endrule', required=False, default='constant', choices=['keep', 'omit', 'constant'], help='behavior at begining and end of the set.\n\'keep\' retains original values,\n\'omit\' drops them from the output\n\'constant\' copies the first and last informative values\n(default: constant)')
    parser.add_argument('-t', '--type', required=False, default='mean', choices=['mean', 'median', 'min', 'max'], help='type of rolling summary (default: mean)')
    parser.add_argument('-w', '--window', required=False, type=int, default=11, help='window size. must be odd. (default: 11)')
    parser.add_argument('-c', '--col', required=False, type=int, default=1, help='column to assess (default: 1)')
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'), default=None, help='file to read. If \'-\' or absent then defaults to stdin.')

    # parse the arguments
    args = parser.parse_args()

    # if no input, check if part of pipe and if so, read stdin.
    if args.input == None:
        if sys.stdin.isatty():
            parser.print_help()
            exit(1)
        else:
            args.input = sys.stdin
    
    if not args.window % 2:
        print '\n# Error: window size must be odd integer #\n'
        parser.print_help()
        exit(1)

    # send back the user input
    return args

# primary function
def rollingStats(f, col, window, stype, endrule, align):
    c = col - 1
    col_buffer = []
    counter = 0

    if align == 'right':
        offset = 0
    elif align == 'left':
        offset = window - 1
    elif align == 'center':
        pass

    # if endrule constant, then make a buffer
    # to hold the full lines until we can write them
    if endrule == 'constant':
        line_buffer = []
        
    for line in f:
        v = line.rstrip().split('\t')
        col_buffer.append(float(v[c]))
        counter += 1

        # get col_summary at the end of each window
        if counter == window - offset:
            if stype == 'mean':
                col_summary = np.mean(col_buffer)
            elif stype == 'median':
                col_summary = np.median(col_buffer)
            elif stype == 'max':
                col_summary = max(col_buffer)
            elif stype == 'min':
                col_summary = min(col_buffer)
            # write the end buffer if it exists
            if endrule == 'constant' and len(line_buffer):
                for l in line_buffer:
                    print '\t'.join(map(str, l[:c] + [col_summary] + l[c+1:] ) )
                line_buffer = []
            # write the line with the modified column
            print '\t'.join(map(str, v[:c] + [col_summary] + v[c+1:] ) )
            col_buffer.pop(0)
            counter -= 1
        # if counter is less than window size,
        # then we must be at either beginning or end of the data.
        # behavior based on endrule
        elif counter < window - offset:
            if endrule == 'keep':
                print line.rstrip()
            elif endrule == 'omit':
                continue
            elif endrule == 'constant':
                line_buffer.append(v)
        # if counter is larger than window then something is horribly wrong
        elif counter > window - offset:
            print 'Error: buffer should never be greater than window'
            exit(1)
    # once done with the for loop, write the end buffer if endrule constant
    if endrule == 'constant':
        pass

    return

# --------------------------------------
# main function

def main():
    # parse the command line args
    args = get_args()

    # call primary function
    rollingStats(args.input, args.col, args.window, args.type, args.endrule, args.align)

    # close the input file
    args.input.close()

# initialize the script
if __name__ == '__main__':
    sys.exit(main())
