#!/usr/bin/env python

import argparse
import random
import sys

def reservoir_sample_lines(input_stream, N):
    reservoir = []
    
    # Read from the input stream line by line
    for i, line in enumerate(input_stream):
        if i < N:
            reservoir.append(line)
        else:
            # Randomly decide if we should replace an element in the reservoir
            j = random.randint(0, i)
            if j < N:
                reservoir[j] = line
    
    # Output the selected lines
    sys.stdout.writelines(reservoir)

def main():
    parser = argparse.ArgumentParser(description="Select random N lines from a file or stdin using reservoir sampling.")
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin, 
                        help="Input file (or stdin if not provided).")
    parser.add_argument('-n', '--num', type=int, required=True, help="Number of lines to select.")
    
    args = parser.parse_args()
    
    reservoir_sample_lines(args.input_file, args.num)

if __name__ == "__main__":
    main()
