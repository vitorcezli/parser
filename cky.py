#!/usr/bin/python
import itertools
import copy


def hasEmptyTransition(rulesDictionary, nonterminal):
	return [] in rulesDictionary[nonterminal]


def hasOnlyEmptyTransition(rulesDictionary, nonterminal):
	return len(rulesDictionary[nonterminal]) == 1 and \
		[] in rulesDictionary[nonterminal]


def deleteEmptyRules(rulesDictionary):
	for nonterminal, rule in rulesDictionary.items():
		if [] in rule:
			del rule[rule.index([])]


def deleteEmptyNonTerminals(rulesDictionary):
	deleteList = []
	for nonterminal, rule in rulesDictionary.items():
		if len(rule) == 0:
			deleteList.append(nonterminal)
	for nonterminal in deleteList:
		del rulesDictionary[nonterminal]


def removeNonterminalFromRules(listOfRules, nonterminal):
	listValueRemoved = []

	for rule in listOfRules:
		rule = list(filter(lambda a: a != nonterminal, rule))
		if rule != []:
			listValueRemoved.append(rule)
	return listValueRemoved


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


def getAllPossibilitiesRemoving(listOfRules, nonterminal):
	possibilities = []

	for rule in listOfRules:
		possibilities.append(rule)
		possibilitiesWithout = getPossibilitiesWithout(rule, nonterminal)
		if possibilitiesWithout != []:
			possibilities += possibilitiesWithout
	return removeDuplicates(possibilities)


def removeEmptyTransitions(dictionary):
	for nonterminal, _ in dictionary.items():
		if hasOnlyEmptyTransition(dictionary, nonterminal):
			for nonterminal1, rules in dictionary.items():
				dictionary[nonterminal1] = \
					removeNonterminalFromRules(rules, nonterminal)
		if hasEmptyTransition(dictionary, nonterminal):
			for nonterminal1, rules in dictionary.items():
				dictionary[nonterminal1] = \
					getAllPossibilitiesRemoving(rules, nonterminal)
	deleteEmptyRules(dictionary)
	deleteEmptyNonTerminals(dictionary)


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



dictRules = {}
dictRules['S'] = [['NP', 'VP'], ['Aux', 'NP', 'VP'], ['VP']]
dictRules['NP'] = [['Pronoun'], ['Proper-noun'], ['Det', 'Nominal']]
dictRules['Nominal'] = [['Noun'], ['Nominal', 'Noun'], ['Nominal', 'PP']]
dictRules['VP'] = [['Verb'], ['Verb', 'NP'], ['Verb', 'NP', 'PP'], ['Verb', 'PP'], ['VP', 'PP']]
dictRules['PP'] = [['Preposition', 'NP']]
dictRules['Det'] = [['that'], ['this'], ['a']]
dictRules['Noun'] = [['book'], ['flight'], ['meal'], ['money']]
dictRules['Verb'] = [['book'], ['include'], ['prefer']]
dictRules['Pronoun'] = [['I'], ['she'], ['me']]
dictRules['Proper-noun'] = [['Houston'], ['TWA']]
dictRules['Aux'] = [['does']]
dictRules['Preposition'] = [['from'], ['to'], ['on'], ['near'], ['through']]
convertToChomsky(dictRules)
ckyParse(['does', 'I', 'include', 'TWA', 'to', 'Houston'], dictRules)