#!/usr/bin/python

def addRuleOnChart(chart, position, rule):
	if position not in chart:
		chart[position] = [rule]
	elif rule not in chart[position]:
		chart[position].append(rule)


def isComplete(rule):
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


def complete(currentRule, chart):
	listAddToChart = []

	for state in chart[currentRule[len(currentRule) - 2]]:
		indexOfPoint = state.index('.')
		if state[indexOfPoint + 1] == currentRule[0]:
			newState = state[:]
			newState[indexOfPoint] = newState[indexOfPoint + 1]
			newState[indexOfPoint + 1] = '.'
			newState[len(newState) - 1] = currentRule[len(currentRule) - 1]
			listAddToChart.append(newState)

	for state in listAddToChart:
		addRuleOnChart(chart, currentRule[len(currentRule) - 1], state)


def earleyParse(sentence, grammar):
	chart = {}
	addRuleOnChart(chart, 0, ['start', '.', 'S', 0, 0])

	for index in range(len(sentence) + 1):
		currentIndex = 0
		while currentIndex < len(chart[index]):
			state = chart[index][currentIndex]
			if isComplete(state):
				complete(state, chart)
			elif partOfSpeech(grammar, state[state.index('.') + 1]):
				scanner(state, grammar, chart)
			else:
				predict(state, grammar, chart)
			currentIndex += 1

	return chart


grammar = []
grammar += [['S', 'NP', 'VP'], ['S', 'Aux', 'NP', 'VP'], ['S', 'VP']]
grammar += [['NP', 'Pronoun'], ['NP', 'Proper-noun'], ['NP', 'Det', 'Nominal']]
grammar += [['Nominal', 'Noun'], ['Nominal', 'Nominal', 'Noun'], ['Nominal', 'Nominal', 'PP']]
grammar += [['VP', 'Verb'], ['VP', 'Verb', 'NP'], ['VP', 'Verb', 'NP', 'PP'], ['VP', 'Verb', 'PP'], ['VP', 'VP', 'PP']]
grammar += [['PP', 'Preposition', 'NP']]
grammar += [['Det', 'that'], ['Det', 'this'], ['Det', 'a']]
grammar += [['Noun', 'book'], ['Noun', 'flight'], ['Noun', 'meal'], ['Noun', 'money']]
grammar += [['Verb', 'book'], ['Verb', 'include'], ['Verb', 'prefer']]
grammar += [['Pronoun', 'I'], ['Pronoun', 'she'], ['Pronoun', 'me']]
grammar += [['Proper-noun', 'Houston'], ['Proper-noun', 'TWA']]
grammar += [['Aux', 'does']]
grammar += [['Preposition', 'from'], ['Preposition', 'to'], ['Preposition', 'on'], ['Preposition', 'near'], ['Preposition', 'through']]
print(earleyParse(['I', 'include'], grammar))