'''
Author: Ruben Dorado

A Test to run the CKY algorithm implementation cyk.py.
'''
import os
import sys
from cky import parse


def main():
	if len(sys.argv) != 3:
		print("   Usage: python3 test.py <grammar_file> <sentence>")
		print("   Example: python3 test.py grammar.cfg \"I prefer the morning flight through Denver\"")
		sys.exit()

	filename = sys.argv[1]
	if not os.path.isfile(filename):
		print("ERROR. File '"+str(filename)+"' not found")
		sys.exit()

	sentence = sys.argv[2]
	if sentence[0] == "\"" and sentence[-1] == "\"": sentence = sentence[1:-1]
	sentence = sentence.lower()
	
	resp = parse(filename, sentence)
	if resp: print("This is a valid sentence according to the grammar")
	else: print("This is not a valid sentence according to the grammar")

if __name__ == '__main__':
	main()


