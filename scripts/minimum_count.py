import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-input', '-i', type=str, required=True, help="input path")
parser.add_argument('-output', '-o', type=str, required=True, help="output path")
parser.add_argument('-minimum_count', '-m', type=int, default=2, help="minimum count")
args = parser.parse_args()

with open(args.input, "r+") as f:
    with open(args.output, "w") as g:
        for line in f:
            if int(line.split()[2]) >= args.minimum_count:
                g.write(line)