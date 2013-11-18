#!/usr/bin/env python

import argparse, sys
from argparse import RawTextHelpFormatter

__author__ = "Colby Chiang (cc2qe@virginia.edu)"
__version__ = "$Revision: 0.0.1 $"
__date__ = "$Date: 2013-11-18 11:19 $"

# --------------------------------------
# define functions

def get_args():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description="\
headerGrep.py\n\
author: " + __author__ + "\n\
version: " + __version__ + "\n\
description: Grep for a string within the column headers and only print those columns")
    parser.add_argument('-d', '--delim', required=False, type=str, default='\t', help='delimiter (default: <tab>)')
    parser.add_argument('-r', '--rowLabels', required=False, action='store_true', help='print the first column')
    parser.add_argument('-c', '--colLabels', required=False, action='store_true', default=True, help='print the first row (default)')
    parser.add_argument('s', metavar='string', type=str, help='search string')
    parser.add_argument('infile', metavar='file', nargs='?', type=argparse.FileType('r'), default=None, help='file to read. If \'-\' or absent then defaults to stdin.')

    # parse the arguments
    args = parser.parse_args()

    # if no input, check if part of pipe and if so, read stdin.
    if args.infile == None:
        if sys.stdin.isatty():
            parser.print_help()
            exit(1)
        else:
            args.infile = sys.stdin

    # send back the user input
    return args

# primary function
def colGrep(s, delim, rowLabs, colLabs, infile):
    # search for the match string columns
    matchCols = list()
    header_v = infile.readline().split(delim)
    for i in range(len(header_v)):
        if s in header_v[i]:
            matchCols.append(i)

    # add the first column (rowLabels) if requested
    if rowLabs and 0 not in matchCols:
        matchCols = [0] + matchCols

    # print matching header rows if requested
    if colLabs:
        outV = list()
        for m in matchCols:
            outV.append(header_v[m])
        if outV:
            print delim.join(outV)
            
    # print the matching body rows
    for line in infile:
        outV = list()
        v = line.rstrip().split(delim)
        for m in matchCols:
            outV.append(v[m])
        if outV:
            print delim.join(outV)
    
    return

# --------------------------------------
# main function

def main():
    # parse the command line args
    args = get_args()

    # store into global values
    s = args.s
    delim = args.delim
    rowLabs = args.rowLabels
    colLabs = args.colLabels
    infile = args.infile
    
    # call primary function
    colGrep(s, delim, rowLabs, colLabs, infile)

    # close the input file
    infile.close()

# initialize the script
if __name__ == '__main__':
    sys.exit(main())
