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
			if len(rule) == 2:
				continue
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
			while len(rule) > 3:
				key = "RLR%d" % (number)
				number += 1
				listAdd.append([key, rule[len(rule) - 3], rule[len(rule) - 2]])
				rule[len(rule) - 3] = key
				del rule[len(rule) - 2]

	for rule in listAdd:
		dictionary[rule[0]] = [[rule[1], rule[2], 1.0]]


def convertToChomsky(dictionary):
	removeEmptyTransitions(dictRules)
	createDummyNonTerminal(dictRules)
	removeLongRules(dictRules)


def getSymbolsFathers(rule, dictionary):
	fathers = []
	for nonterminal, rules in dictionary.items():
		for ruleList in rules:
			if rule == ruleList[0 : len(ruleList) - 1]:
				fathers.append([nonterminal] + [ruleList[len(ruleList) - 1]])
	return fathers


def ckyParse(string, dictionary):
	table = [[{} for x in range(len(string) + 1)] \
		for y in range(len(string))]
	back = [[{} for x in range(len(string) + 1)] \
		for y in range(len(string))]

	for j in range(1, len(string) + 1):
		# part of speech transitions
		fathers = getSymbolsFathers([string[j - 1]], dictionary)
		for father in fathers:
			table[j - 1][j][father[0]] = father[1]

		for i in range(j - 2, -1, -1):
			for k in range(i + 1, j):
				# after this part there is the possible two nonterminals
				# that make part of the right side of a rule
				listPosition = []
				for symbol1, _ in table[i][k].items():
					for symbol2, _ in table[k][j].items():
						listPosition.append([symbol1, symbol2])
				print(str(i) + str(j) + str(listPosition))
				for rule in listPosition:
					fathers = getSymbolsFathers(rule, dictionary)
					print(fathers)
					for father in fathers:
						if father in table[i][j]:
							if table[i][j][father] < father[1] * table[i][k][rule[0]] * table[k][j][rule[1]]:
								table[i][j][father] = father[1] * table[i][k][rule[0]] * table[k][j][rule[1]]
								back[i][j][father] = [k, rule[0], rule[1]]
						else:
							table[i][j][father] = father[1] * table[i][k][rule[0]] * table[k][j][rule[1]]
							back[i][j][father] = [k, rule[0], rule[1]]

	print(table)

	for i in range(len(table)):
		for j in range(len(table[i])):
			print(len(table[i][j]), end = "%5s" % ('\t'))
		print('')



dictRules = {}
dictRules['S'] = [['NP', 'VP', 0.5], ['Aux', 'NP', 'VP', 0.1], ['VP', 0.4]]
dictRules['NP'] = [['Pronoun', 0.7], ['Proper-noun', 0.1], ['Det', 'Nominal', 0.2]]
dictRules['Nominal'] = [['Noun', 0.2], ['Nominal', 'Noun', 0.4], ['Nominal', 'PP', 0.4]]
dictRules['VP'] = [['Verb', 0.2], ['Verb', 'NP', 0.2], ['Verb', 'NP', 'PP', 0.2], ['Verb', 'PP', 0.2], ['VP', 'PP', 0.2]]
dictRules['PP'] = [['Preposition', 'NP', 1.0]]
dictRules['Det'] = [['that', 0.25], ['this', 0.25], ['a', 0.5]]
dictRules['Noun'] = [['book', 0.3], ['flight', 0.3], ['meal', 0.2], ['money', 0.2]]
dictRules['Verb'] = [['book', 0.05], ['include', 0.35], ['prefer', 0.6]]
dictRules['Pronoun'] = [['I', 0.4], ['she', 0.2], ['me', 0.4]]
dictRules['Proper-noun'] = [['Houston', 0.5], ['TWA', 0.5]]
dictRules['Aux'] = [['does', 1.0]]
dictRules['Preposition'] = [['from', 0.3], ['to', 0.5], ['on', 0.1], ['near', 0.05], ['through', 0.05]]
convertToChomsky(dictRules)
ckyParse(['I', 'prefer', 'me'], dictRules)