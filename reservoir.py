#!/usr/bin/env python

import argparse
import random
import sys

def reservoir_sample_lines(input_stream, N, header_prefix=None, seed=None):
    # Set the random seed if provided
    if seed is not None:
        random.seed(seed)

    reservoir = []
    headers = []

    # Read from the input stream line by line
    for i, line in enumerate(input_stream):
        # If a header_prefix is provided and the line starts with it, treat it as a header
        if header_prefix is not None and line.startswith(header_prefix):
            headers.append(line)
        else:
            if len(reservoir) < N:
                reservoir.append(line)
            else:
                # Randomly decide if we should replace an element in the reservoir
                j = random.randint(0, i - len(headers))
                if j < N:
                    reservoir[j] = line

    # Output the header lines first (if any)
    sys.stdout.writelines(headers)
    # Output the selected lines from the reservoir
    sys.stdout.writelines(reservoir)

def main():
    parser = argparse.ArgumentParser(description="Select random N lines from a file or stdin using reservoir sampling, optionally keeping header lines.")
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin, 
                        help="Input file (or stdin if not provided).")
    parser.add_argument('-n', '--num', type=int, required=True, help="Number of lines to select.")
    parser.add_argument('-s', '--seed', type=int, help="Random seed for reproducibility.", required=False)
    parser.add_argument('-p', '--header_prefix', type=str, help="Prefix for header lines (optional, no header by default).", required=False)
    
    args = parser.parse_args()
    
    # Call the reservoir sampling function
    reservoir_sample_lines(args.input_file, args.num, header_prefix=args.header_prefix, seed=args.seed)

if __name__ == "__main__":
    main()
