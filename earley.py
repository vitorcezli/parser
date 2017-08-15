#!/usr/bin/python

def addRuleOnChart(chart, position, rule):
	if position not in chart:
		chart[position] = [rule]
	elif rule not in chart[position]:
		chart[position].append(rule)


def complete(rule):
	return rule.index('.') == len(rule) - 3


def terminal(grammar, symbol):
	for rule in grammar:
		if rule[0] == symbol:
			return False
	return True


def partOfSpeech(grammar, symbol):
	for rule in grammar:
		if rule[0] == symbol and len(rule) == 2 and \
			terminal(grammar, rule[1]):
			return True
	return False


def predict(currentRule, grammar, chart):
	nonTerminalSymbol = currentRule[currentRule.index('.') + 1]
	positionOnWord = currentRule[len(currentRule) - 1]

	for rule in grammar:
		if rule[0] == nonTerminalSymbol:
			addRuleOnChart(chart, positionOnWord, [rule[0]] + ['.'] +
				rule[1 : ] + [positionOnWord, positionOnWord])


def scanner(currentRule, grammar, chart):
	nonTerminalSymbol = currentRule[currentRule.index('.') + 1]
	positionOnWord = currentRule[len(currentRule) - 1]

	if partOfSpeech(grammar, nonTerminalSymbol):
		for rule in grammar:
			if rule[0] == nonTerminalSymbol:
				addRuleOnChart(chart, positionOnWord + 1, \
					[nonTerminalSymbol] + [rule[1]] + ['.'] + \
					[positionOnWord, positionOnWord + 1])


def complete(currentRule, grammar, chart):
	listAddToChart = []
	for state in chart:
		indexOfPoint = currentRule[currentRule.index('.') + 1]
		if state[indexOfPoint + 1] == currentRule[0]:
			newState = state[:]
			newState[indexOfPoint] = newState[indexOfPoint + 1]
			newState[indexOfPoint + 1] = '.'
			newState[len(newState - 1)] = currentRule[len(currentRule) - 1]
			listAddToChart.append(newState)

	for state in listAddToChart:
		addRuleOnChart(chart, currentRule[len(currentRule) - 1], state)


def earleyParse(sentence, grammar):
	chart = {}
	addRuleOnChart(chart, 0, ['start', '.', 'S', 0, 0])

	for index in range(len(sentence)):
		currentIndex = 0
		while currentIndex < len(chart[index]):
			print('nothing')
			currentIndex += 1


chart = {}
grammar = [['A', 'B']]
grammar.append(['B', 'C'])
grammar.append(['C', 'E'])
grammar.append(['C', 'F'])
grammar.append(['B', 'D', 'E'])
scanner(['B', '.', 'C', 0, 2], grammar, chart)
print(chart)
scanner(['G', '.', 'C', 'D', 'B', 3, 3], grammar, chart)
print(chart)