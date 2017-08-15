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
	print('nothing')



def earleyParse(sentence, grammar):
	chart = {}
	addRuleOnChart(chart, 0, ['start', '.', 'S', 0, 0])

	for index in range(len(sentence)):
		currentIndex = 0
		while currentIndex < len(chart[index]):
			print('nothing')
			currentIndex += 1


chart = {}
addRuleOnChart(chart, 0, ['test'])
addRuleOnChart(chart, 0, ['test1'])
addRuleOnChart(chart, 0, ['test'])
addRuleOnChart(chart, 1, ['test'])
print(chart)
print(complete(['A', 'B', '.', 'C']))
print(complete(['A', 'B', 'C', '.', 0, 0]))
grammar = [['A', 'B']]
grammar.append(['B', 'C'])
print(partOfSpeech(grammar, 'A'))
print(partOfSpeech(grammar, 'C'))