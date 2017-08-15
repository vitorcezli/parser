#!/usr/bin/python

def addRuleOnChart(chart, position, rule):
	if position not in chart:
		chart[position] = [rule]
	elif rule not in chart[position]:
		chart[position].append(rule)


def complete(rule):
	return rule.index('.') == len(rule) - 3


def partOfSpeech(grammar, symbol):
	for rule in grammar:
		if rule[0] == symbol:
			return False
	return True


def predict(currentRule, grammar, chart):
	nonTerminalSymbol = currentRule[currentRule.index('.') + 1]
	positionOnWord = currentRule[len(currentRule) - 1]

	for rule in grammar:
		if rule[0] == nonTerminalSymbol:
			addRuleOnChart(chart, positionOnWord, [rule[0]] + ['.'] +
				rule[1 : ] + [positionOnWord, positionOnWord])



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
grammar.append(['B', 'D', 'E'])
predict(['A', 'V', 'Y', '.', 'B', 3, 8], grammar, chart)
print(chart)