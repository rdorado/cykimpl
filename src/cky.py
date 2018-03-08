'''
Author: Ruben Dorado

A Python implementation of the CKY algorithm given a CFG and a sentence.
'''
import re

class Grammar:

	def __init__(self):
		self.rules = {}
		self.terminals = {}
		self.backrule = {}

	def addRule(self, left_side, right_side):
		try:
			self.rules[left_side].append(right_side)
		except KeyError:
			self.rules[left_side] = [right_side]
		try:
			self.backrule[tuple(right_side)].append(left_side)
		except KeyError:
			self.backrule[tuple(right_side)] = [left_side]
		
	def addTerminal(self, left_side, right_side):
		try:
			self.terminals[right_side].append(left_side)
		except KeyError:
			self.terminals[right_side] = [left_side]		

	def print(self):
		print(self.rules)
		print(self.terminals)
		print(self.backrule)
		
	def getTerminalRules(self, terminal):
		resp = ["OOV"]
		try:
			resp = self.terminals[terminal]
		except KeyError: pass 		
		return resp

	def getSymbolFromRule(self, rule):
		resp = []
		try:
			resp = self.backrule[tuple(rule)]
                        
		except KeyError: pass
			
		return resp


def table_print(table):
	for row in table:
		line = ""
		for col in row:
			line+=str(col)+"\t"
		print(line)


def cky(grammar, sentence, debug=False):
	n = len(sentence)
	table = [[[] for i in range(n-j)] for j in range(n)]
	unaries = [[{} for i in range(n-j)] for j in range(n)]
	nodes_back = [[[] for i in range(n + 1)] for j in range(n + 1)]

	#Initialize table
	for w in range(1, n + 1):
		symbols = grammar.getTerminalRules(sentence[w-1])
		table[0][w-1].extend( symbols )
                # Add unaries 
		for S in symbols:
			rules = grammar.getSymbolFromRule([S])
			for U in rules:
				if S not in unaries[0][w-1] and U not in table[0][w-1]:
					table[0][w-1].append(U)
					unaries[0][w-1][U] = True

	if debug: table_print(table)
	for l in range(0, n-1):
		for s in range(n-l-1):
			for p in range(l+1):
				for X in table[p][s]:
					for Y in table[l-p][s+p+1]:
						symbols = grammar.getSymbolFromRule([X, Y])
						table[l+1][s].extend(symbols)

                				# Add unaries 
						for S in symbols:
							rules = grammar.getSymbolFromRule([S])
							for U in rules:			
								if U not in unaries[l+1][s] and U not in table[l+1][s]:
									table[l+1][s].append(U)
									unaries[l+1][s][U] = True
		if debug:
			print()				
			table_print(table)

	return table[n-1][0]


def load_grammar(grammar_filename):
	grammar = Grammar()
	pattern = re.compile(".+->.+( .+)?")
	
	nline = 0
	with open(grammar_filename, 'r') as f:
		lines = f.readlines()
		for line in lines:
			nline+=1
			line = line.strip()
			if len(line) == 0 or line[0] == '#' : continue
			if not pattern.match(line):
				raise ValueError("Error reading grammar in file '"+grammar_filename+"' line "+nline)
				
			rule = [x.strip() for x in line.split('->')]
			right_side = rule[1].split()

			if len(right_side) == 1 and right_side[0] == right_side[0].lower():
				grammar.addTerminal(rule[0],right_side[0])	
			else:                        
				grammar.addRule(rule[0], right_side)

	return grammar


def parse(grammar_filename, sentence, debug=False):
	grammar = load_grammar(grammar_filename)
	if debug: grammar.print()
	result = cky(grammar, sentence.split(),debug=debug)
	return "S" in result

