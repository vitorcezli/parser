#!/usr/bin/python
from __future__ import division
import itertools
import numbers
import copy


def normalize(rules):
	sumProbability = 0
	for rule in rules:
		sumProbability += rule[len(rule) - 1]
	for rule in rules:
		rule[len(rule) - 1] /= sumProbability


def emptyRule(rule):
	return len(rule) == 1 and isinstance(rule[0], numbers.Number)


def removeFromRules(rules, nonterminal):
	newRules = []
	for rule in rules:
		newRules.append(list(filter(lambda a: a != nonterminal, rule)))
	return newRules


def removeEmptyRules(rules):
	return list(filter(lambda a: len(a) != 1, rules))


def removeEmptyTransitions(dictionary):
	while(True):
		doneDeleting = True
		for nonterminal, rules in dictionary.items():
			print(nonterminal)
			# if the nonterminal only generates an empty string
			if len(rules) == 0 or (len(rules) == 1 and emptyRule(rules[0])):
				# remove the nonterminal from every rule it appears
				for nonterminal1, rules1 in dictionary.items():
					rules1 = removeFromRules(rules1, nonterminal)
					rules1 = removeEmptyRules(rules1)
					normalize(rules1)
					dictionary[nonterminal1] = rules1
				# remove the nonterminal from the dictionary
				del dictionary[nonterminal]
				doneDeleting = False
				break
		# if the program has passed every nonterminal it has not found any
		# empty transition
		if doneDeleting:
			break


def getUnitarySons(dictionary, nonterminal):
	if nonterminal not in dictionary:
		return [[nonterminal]]

	listDelete = []
	listAdd = []
	rules = copy.deepcopy(dictionary[nonterminal])

	for index in range(len(rules)):
		if len(rules[index]) == 1:
			listDelete.append(index)
			listAdd += getUnitarySons(dictionary, rules[index][0])

	deleted = 0
	for index in range(len(listDelete)):
		del rules[listDelete[index] - deleted]
		deleted += 1

	rules += listAdd
	rules.sort()
	return list(k for k,_ in itertools.groupby(rules))


def removeUnitaryTransitions(dictionary):
	for nonterminal, _ in dictionary.items():
		dictionary[nonterminal] = getUnitarySons(dictionary, \
			nonterminal)


def createDummyNonTerminal(dictionary):
	dictDummy = {}

	for _, rules in dictionary.items():
		for rule in rules:
			if len(rule) == 2:
				continue
			for index in range(len(rule) - 1):
				if rule[index] not in dictionary:
					if rule[index] not in dictDummy:
						dictDummy[rule[index]] = \
							"DUMMY%d" % (len(dictDummy))

	for _, rules in dictionary.items():
		for rule in rules:
			for index in range(len(rule) - 1):
				if rule[index] not in dictionary:
					rule[index] = dictDummy[rule[index]]

	for nonterminal, dummy in dictDummy.items():
		dictionary[dummy] = [[nonterminal, 1.0]]


def removeLongRules(dictionary):
	listAdd = []
	number = len(dictionary)
	for nonterminal, rules in dictionary.items():
		for rule in rules:
			while len(rule) > 2:
				key = "RLR%d" % (number)
				number += 1
				listAdd.append([key, rule[len(rule) - 2], rule[len(rule) - 1]])
				rule[len(rule) - 2] = key
				del rule[len(rule) - 1]

	for rule in listAdd:
		dictionary[rule[0]] = [[rule[1], rule[2]]]


def convertToChomsky(dictionary):
	removeEmptyTransitions(dictRules)
	createDummyNonTerminal(dictRules)
	removeUnitaryTransitions(dictRules)
	removeLongRules(dictRules)


def getFatherNonterminal(rule, dictionary):
	fathers = []
	for nonterminal, rules in dictionary.items():
		for ruleList in rules:
			if rule == ruleList:
				fathers.append(nonterminal)
	return fathers


def ckyParse(string, dictionary):
	table = [[[] for x in range(len(string) + 1)] \
		for y in range(len(string))]

	for j in range(1, len(string) + 1):
		table[j - 1][j] = getFatherNonterminal([string[j - 1]], dictionary)
		for i in range(j - 2, -1, -1):
			for k in range(i + 1, j):
				listPosition = []
				for position1 in table[i][k]:
					for position2 in table[k][j]:
						listPosition.append([position1, position2])
				for rule in listPosition:
					table[i][j] += \
						getFatherNonterminal(rule, dictionary)
			table[i][j] = list(set(table[i][j]))

	for i in range(len(table)):
		for j in range(len(table[i])):
			print(table[i][j], end = "%5s" % ('\t'))
		print('')



# dictRules = {}
# dictRules['S'] = [['NP', 'VP'], ['Aux', 'NP', 'VP'], ['VP']]
# dictRules['NP'] = [['Pronoun'], ['Proper-noun'], ['Det', 'Nominal']]
# dictRules['Nominal'] = [['Noun'], ['Nominal', 'Noun'], ['Nominal', 'PP']]
# dictRules['VP'] = [['Verb'], ['Verb', 'NP'], ['Verb', 'NP', 'PP'], ['Verb', 'PP'], ['VP', 'PP']]
# dictRules['PP'] = [['Preposition', 'NP']]
# dictRules['Det'] = [['that'], ['this'], ['a']]
# dictRules['Noun'] = [['book'], ['flight'], ['meal'], ['money']]
# dictRules['Verb'] = [['book'], ['include'], ['prefer']]
# dictRules['Pronoun'] = [['I'], ['she'], ['me']]
# dictRules['Proper-noun'] = [['Houston'], ['TWA']]
# dictRules['Aux'] = [['does']]
# dictRules['Preposition'] = [['from'], ['to'], ['on'], ['near'], ['through']]
# convertToChomsky(dictRules)
# ckyParse(['does', 'I', 'include', 'TWA', 'to', 'Houston'], dictRules)
dictRules = {}
dictRules['B'] = [[1]]
dictRules['A'] = [['B', 0.5], ['C', 0.5]]
dictRules['C'] = [['B', 0.3], ['E', 0.7]]
dictRules['D'] = [['B', 'A', 'E', 0.3], ['E', 0.7]]
dictRules['H'] = [['D', 0.7]]
dictRules['I'] = [['D', 'H', 'E', 'H', 'F', 1]]
print(dictRules)
removeEmptyTransitions(dictRules)
print(dictRules)
createDummyNonTerminal(dictRules)
print(dictRules)