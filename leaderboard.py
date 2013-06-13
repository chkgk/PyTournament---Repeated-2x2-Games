#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module provides the leaderboard function without requireing any other modules.
# It is used to allow a basic tournament to work without any non-std modules.
# Other game analysis should be done in game_analyser.py

import tournament

# function calc_sums
#
# Returns dictonary with total reward for each strategy
#
def calc_sums(game, history):
	total= {}
	for stratA in history.keys():
		total[stratA] = 0
	for stratA in sorted(history.keys()):
		for stratB in sorted(history.keys()):
			if stratA == stratB:
				break
			for i in range(len(history[stratA][stratB])):
				payoffs = make_payoff_history(game, history[stratA][stratB][i])
				for n in range(len(payoffs)):
					total[stratA] += payoffs[n][0]
					total[stratB] += payoffs[n][1]
	return total

# function get_round_number
# 
# Counts total number of rounds played by each strategy.
#
def get_round_number(histories):
	rounds = 0
	keys = sorted(histories.keys())
	for i in histories[keys[0]][keys[1]]:
		rounds += len(i)
	rounds = rounds * (len(histories.keys()) - 1)
	return rounds

# function get_leaderboard
#
# Returns sorted leaderbard from game and histories object.
#
def get_leaderboard(game, histories):
	res = ""
	sums = calc_sums(game, histories)
	if game == "prison":
		rev = False 
	else:
		rev = True
	rounds = get_round_number(histories)
	length = len(max(sums.keys(), key=lambda i:len(i))) + 1
	for a in sorted(sums.keys(), key=lambda i:sums[i], reverse=rev):
		b = a + ":"
		while len(b) < length:
			b += " "
		res += b + " " + str(sums[a]) + " | " + str(round(sums[a]/float(rounds), 1)) + "\n"
	return res 

# function make_payoff_history
#
# transforms a history of choices into a history of payoffs
# i.e. [("a","a"),("a","b")] will turn into [(1,-1),(-1,1)] for the game pennies
#
def make_payoff_history(game, history):
	pay_history = []
	for i in range(len(history)):
		pay_history.append(tournament.determine_payoff(game,history[i][0],history[i][1]))
	return pay_history

# function sum_payoffs
#
# takes a payoff history (as created my make_payoff_history) and sums up payoffs for each player
# 
def sum_payoffs(payoff_history):
	sumA = 0
	sumB = 0
	for run in payoff_history:
		sumA += run[0]
		sumB += run[1]
	return (sumA,sumB)

# function avg_payoffs
#
# takes a payoff history (as created my make_payoff_history) and averages payoffs for each player
# 
def avg_payoffs(payoff_history):
	sumA = 0
	sumB = 0
	for run in payoff_history:
		sumA += run[0]
		sumB += run[1]
	avgA = sumA / float(len(payoff_history))
	avgB = sumB / float(len(payoff_history))

	return (avgA,avgB)

# function sum_stepwise
#
# takes a payoff history and returns a history with stepwise summed up payoffs.
# i.e. [(1,1),(0,3)] turns into [(1,1),(1,4)]
# 
def sum_stepwise(payoff_history):
	sumA = 0
	sumB = 0
	stepsum_history = []

	for run in payoff_history:
		sumA += run[0]
		sumB += run[1]
		stepsum_history.append((sumA, sumB))

	return stepsum_history

# function split_stepwise
#
# takes a stepsum history (as created by sum_stepwise) and separates the payoff histories of both players
# i.e.  [(1,1),(1,4),(1,7)] turns into [[1,1,1], [1,4,7]]
# 
def split_stepwise(stepsum_history):
	payoffsA = []
	payoffsB = []
	for run in stepsum_history:
		payoffsA.append(run[0])
		payoffsB.append(run[1])
	return (payoffsA, payoffsB)
