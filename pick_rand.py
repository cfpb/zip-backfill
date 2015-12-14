'''
Pick a number of random rows from a file and place them in an output file
'''

import random
from collections import deque

def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

def choose_rows(length, number):
	picks = random.sample(range(length), number)
	return sorted(picks)

def write_rows(inputF, outputF, number):
	picks = deque(choose_rows(file_len(inputF), number))
	output = open(outputF, 'w')
	current = picks.popleft()
	with open(inputF, 'r') as f:
		for inx, row in enumerate(f):
			if inx == current: 
				output.write(row)
				if len(picks) > 0: current = picks.popleft()
				else: break

if __name__ == '__main__':
	
	import argparse

	#command line parser
	parser = argparse.ArgumentParser(description = 'picks random rows from a file')
	parser.add_argument('input', help = 'the input file')
	parser.add_argument('output', help = 'the output file')
	parser.add_argument('number', type = int, help = 'the number of rows to return')
	args = parser.parse_args()

	pick_rows(args.input, args.output, args.number)