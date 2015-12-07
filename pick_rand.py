import argparse
import random
from collections import deque

parser = argparse.ArgumentParser(description = 'picks random rows from a file')
parser.add_argument('input', help = 'the input file')
parser.add_argument('output', help = 'the output file')
parser.add_argument('number', type = int, help = 'the number of rows to return')
args = parser.parse_args()

def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

def pick_rows(length, number):
	picks = random.sample([i for i in range(length)], number)
	return sorted(picks)

picks = deque(pick_rows(file_len(args.input), args.number))
output = open(args.output, 'w')
current = picks.popleft()
with open(args.input, 'r') as f:
	for inx, row in enumerate(f):
		if inx == current: 
			output.write(row)
			if len(picks) > 0: current = picks.popleft()
			else: break