#!/usr/bin/python
from __future__ import division
import itertools
import numbers
import copy


def removeDuplicates(listVariable):
	listVariable.sort()
	return list(k for k,_ in itertools.groupby(listVariable))	


def getPossibilitiesWithout(rule, nonterminal):
	possibilities = []

	for index in range(len(rule)):
		if rule[index] == nonterminal:
			listCopy = rule[:]
			del listCopy[index]
			if len(listCopy) >= 1:
				possibilities.append(listCopy)
				possibilities += getPossibilitiesWithout(listCopy, nonterminal)
	return removeDuplicates(possibilities)


def joinSamePossibilities(listOfRules):
	dictJoin = {}
	for rule in listOfRules:
		if tuple(rule[ : len(rule) - 1]) in dictJoin:
			dictJoin[tuple(rule[ : len(rule) - 1])] += \
				rule[len(rule) - 1]
		else:
			dictJoin[tuple(rule[ : len(rule) - 1])] = \
				rule[len(rule) - 1]

	returnRules = []
	for rule, probability in dictJoin.items():
		transition = list(rule)
		transition.append(probability)
		returnRules.append([transition])
	return returnRules


def getAllPossibilitiesRemoving(listOfRules, nonterminal):
	possibilities = []

	for rule in listOfRules:
		sumProbability = rule[len(rule) - 1]
		newPossibilities = []
		newPossibilities.append(rule[ : len(rule) - 1])
		possibilitiesWithout = \
			getPossibilitiesWithout(rule[ : len(rule) - 1], nonterminal)
		if possibilitiesWithout != []:
			newPossibilities += possibilitiesWithout
		newPossibilities = removeDuplicates(newPossibilities)

		# normalize the probability
		for possibility in newPossibilities:
			possibility.append(sumProbability / len(newPossibilities))
		possibilities += newPossibilities

	# join same possibilities
	return joinSamePossibilities(possibilities)


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
		for nonterminal, rules in dictionary.items():
			# if the nonterminal only generates an empty string
			if len(rules) == 0 or (len(rules) == 1 and emptyRule(rules[0])):
				# remove the nonterminal from every rule it appears
				for nonterminal1, rules1 in dictionary.items():
					print('\t' + nonterminal1)
					rules1 = removeFromRules(rules1, nonterminal)
					print('\t\t' + str(rules1))
					rules1 = removeEmptyRules(rules1)
					normalize(rules1)
					dictionary[nonterminal1] = rules1
				# remove the nonterminal from the dictionary
				del dictionary[nonterminal]
				break
			else:
				generates = False
				for rule in rules:
					if emptyRule(rule):
						generates = True
				# if the nonterminal generates an empty string in one of its rules
				if generates:
					# remove the empty generation rule
					rules = removeEmptyRules(rules)
					normalize(rules)
					# use getPossibilitiesRemoving in every rule it appears
					for nonterminal1, rules1 in dictionary.items():
						if nonterminal1 != nonterminal:
							rules1 = getAllPossibilitiesRemoving(rules1, nonterminal)
							rules1 = removeEmptyRules(rules1)
							normalize(rules1)
							dictionary[nonterminal1] = rules1
		# if the program has passed every nonterminal it has not found any
		# empty transition
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
			if len(rule) == 1:
				continue
			for stringGeneration in rule:
				if stringGeneration not in dictionary:
					if stringGeneration not in dictDummy:
						dictDummy[stringGeneration] = \
							"DUMMY%d" % (len(dictDummy))

	for _, rules in dictionary.items():
		for rule in rules:
			if len(rule) == 1:
				continue
			for index in range(len(rule)):
				if rule[index] not in dictionary:
					rule[index] = dictDummy[rule[index]]

	for dummy, nonterminal in dictDummy.items():
		dictionary[nonterminal] = dummy


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
dictRules['C'] = [['B', 1]]
print(dictRules)
removeEmptyTransitions(dictRules)
print(dictRules)
