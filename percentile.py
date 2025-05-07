#!/usr/bin/env python3

import argparse
import pandas as pd
import sys

def main():
    parser = argparse.ArgumentParser(description="Add a percentile column to a tab-delimited file.")
    parser.add_argument("input", nargs="?", type=argparse.FileType('r'), default=sys.stdin,
                        help="Input file (default: stdin)")
    parser.add_argument("-c", "--column", type=int, required=False, default=1,
                        help="1-based index of the column to compute percentiles (default: 1)")
    parser.add_argument("-o", "--output", type=argparse.FileType('w'), default=sys.stdout,
                        help="Output file (default: stdout)")

    args = parser.parse_args()

    # Load the input file
    df = pd.read_csv(args.input, sep="\t", header=None)

    # Adjust to 0-based index for the selected column
    col_idx = args.column - 1

    if col_idx >= len(df.columns):
        raise ValueError(f"Column index {args.column} is out of range for the input file.")

    # Compute percentiles
    df['percentile'] = df.iloc[:, col_idx].rank(pct=True)

    # Write the output
    df.to_csv(args.output, sep="\t", index=False, header=False)

if __name__ == "__main__":
    main()
