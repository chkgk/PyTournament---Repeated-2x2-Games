#!/usr/bin/python
# -*- coding: utf-8 -*-

import tournament
import numpy as np

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


# function analyse_strategy
#
#
#
def analyse_strategy(game, strategy, preppedResults):
	result = ""
	reset = '\033[0m' # resets all formating

	result += "Average of Sums Performance:\n"
	for opponent in preppedResults["avg-of-sums"].keys():
		valueA = preppedResults["avg-of-sums"][opponent][0]
		valueB = preppedResults["avg-of-sums"][opponent][1]

		color = get_color(valueA, valueB, game)

		line = str(strategy) + "  " + color + ('%.3f' % valueA).rjust(8) + reset + " | " + ('%.3f' % valueB).rjust(8) + "  "+ str(opponent) +"\n"
		result += line


	result += "\nAverage of Averages Performance:\n"
	for opponent in preppedResults["avg-of-avgs"].keys():
		valueA = preppedResults["avg-of-avgs"][opponent][0]
		valueB = preppedResults["avg-of-avgs"][opponent][1]

		color = get_color(valueA, valueB, game)

		line = str(strategy) + "  " + color+ ('%.3f' % valueA).rjust(8) + reset +" | " + ('%.3f' % valueB).rjust(8) + "  "+ str(opponent) +"\n"
		result += line

	result += "\nRepresantative Iteration and Standard Deviation between Least Squares of that Iteration:\n"
	for opponent in preppedResults["avg-of-sums"].keys():
		tmp = correct_rounds(preppedResults["payoff-history"][opponent])
		(valueA, least_squares) = get_representative_iteration(tmp)
		valueB = get_standard_deviation(tmp, valueA)
		line = "rep. Iteration: " + str(valueA) + (" least square %8.2f" % least_squares) + (" with std: %8.2f " % valueB) + str(opponent) + "\n"
		result += line

	return result

# function get_color
#
# compares valA and valB and returns the color valA should be printed in depending on the game which is played
# in prisoners dilemma, low values are good -> color code smaller values in green
# in all other games, the higher value is colored green.
def get_color(valA, valB, game):
	if game != "prison":
		if valA > valB:
			color = '\033[32m' #green
		elif valA < valB:
			color = '\033[31m' #red
		else:
			color = '\033[33m' #yellow
	else:
		if valA < valB:
			color = '\033[32m' #green
		elif valA > valB:
			color = '\033[31m' #red
		else:
			color = '\033[33m' #yellow
	return color

# function prep_for_plot
#
# takes the game, the two strategies, the iteration to plot and a histories object as created by the tournament
# and turn it into a 4-element tupel that is accepted by the plot_game function in game_analyser
#
# First, the history is turned into a payoff history, then the payoffs are summed up to each step in the history
# finally the step_sum history is split into two separate lists. These are then returned together with the
# corresponding strategy names.
#
def prep_for_plot(game, stratA, stratB, iteration, histories):
	splitted_stepsum = split_stepwise(sum_stepwise(make_payoff_history(game,histories[stratA][stratB][iteration])))
	return (stratA, stratB, splitted_stepsum[0], splitted_stepsum[1])

# function prep_for_analysis
#
# take a game, a strategy name and a histories object (from the tournament)
# and prepare summary statistics from the point of view of the given strategy
# 
# returns a dictionary{"payoff-history", "payoff-stepsums", "payoff-iteration-sums", "payoff-iteration-avgs",
# "avg-of-sums", "avg-of-avgs" }
#
# "payoff-history" contains a dictionary {"opponent1":[[(1,1),(0,3)],[(4,4),(2,2)]], "oppontent2": [], ...}
# i.e. for each opponent we have a list of all iterations, which each contains a payoff-history
#
# "payoff-stepsums" contains a dictionary of opponents (see above) which again contains a list of all iterations
# each iteration then again includes a step-sum history as produced by the corresponding function
#
# "payoff-iteration-sums" contains a dictionary of opponents which contains a list of iterations
# each iteration contains a tupel (sumA, sumB) as produced by the function sum_payoffs
# i.e. it includes for each player the sum of all payoffs over all rounds within that iteration
#
# "payoff-iteration-avgs" contains a dict of opponents which contains a list of iterations
# each iteration contains a tuple (avgA, avgB) as produced by the function avg_payoffs
#
# "avg-of-sums" contains a dict of opponents which contains a tuple (avg-sum-A, avg-sum-B). 
# i.e. the payoff sums of all iterations are summed up for each player and then devided by the number of iterations
#
# "avg-of-avgs" contains a dict of opponents which contains a tuple (avg-avg-A, avg-avg-B)
# i.e. the average of the average payoffs of each player over all iterations
#

def prep_for_analysis(game, strategy, histories):
	payoff_his = {}
	payoff_sums = {}
	payoff_stepwise = {}
	payoff_avgs = {}

	avg_sums = {}
	avg_avgs = {}

	# make payoff histories for iterations and rounds vs. all opponent strategies
	# then calculate averages and sums (incl. stepwise) 
	for opponent in histories[strategy].keys():
		payoff_his[opponent] = []
		payoff_sums[opponent] = []
		payoff_stepwise[opponent] = []
		payoff_avgs[opponent] = []
		for iteration in range(len(histories[strategy][opponent])):
			payoff_his[opponent].append(make_payoff_history(game, histories[strategy][opponent][iteration]))
			payoff_sums[opponent].append(sum_payoffs(payoff_his[opponent][iteration]))
			payoff_avgs[opponent].append(avg_payoffs(payoff_his[opponent][iteration]))
			payoff_stepwise[opponent].append(sum_stepwise(payoff_his[opponent][iteration]))

	# calculate average of the sum of payoffs vs. each opponent for each iteartion played
	# and also the average of the average payoffs vs. each opponent
	for opponent in payoff_sums.keys():
		sumA = 0
		sumB = 0
		avgSumA = 0
		avgSumB = 0
		for i in range(len(payoff_sums[opponent])):
			sumA += payoff_sums[opponent][i][0]
			sumB += payoff_sums[opponent][i][1]
			avgSumA += payoff_avgs[opponent][i][0]
			avgSumB += payoff_avgs[opponent][i][1]
		avg_sums[opponent] = (sumA/float(len(payoff_sums[opponent])), sumB/float(len(payoff_sums[opponent])))
		avg_avgs[opponent] = (avgSumA/float(len(payoff_avgs[opponent])), avgSumB/float(len(payoff_avgs[opponent])))

	result = {"payoff-history":payoff_his, "payoff-stepsums":payoff_stepwise, "payoff-iteration-sums":payoff_sums, \
				 "payoff-iteration-avgs":payoff_avgs, "avg-of-sums":avg_sums, "avg-of-avgs":avg_avgs}

	return result

# functino least_squares
#
# Takes to iterations and compares them by least square difference.
#
def least_squares(i, n):
	i = np.array(i)
	n = np.array(n)
	diff = i - n
	diff = diff * diff
	res = diff.sum()
	return res

# function correct_rounds
#
# Creates an iteration_array with equal amount of rounds in each iteration.
#
def correct_rounds(iteration_array):
	lengths = []
	for i in iteration_array:
		lengths.append(len(i))
	min_len = min(lengths)
	new_iteration_array = np.zeros([len(iteration_array), min_len, 2])
	for i in range(len(iteration_array)):
		for n in range(min_len):
			new_iteration_array[i, n, 0] = iteration_array[i][n][0]
			new_iteration_array[i, n, 1] = iteration_array[i][n][1]
	return new_iteration_array

# functino get_representative_iteration 
#
# Searches for lowest least square difference among all iterations.
#
def get_representative_iteration(iteration_array):
	length = len(iteration_array)
	best = None
	tmp = 0
	for i in range(length):
		tmp = 0
		for n in range(length):
			if i == n:
				continue
			tmp += least_squares(iteration_array[n], iteration_array[i])
		if not best:
			best = {"value": tmp, "index": i}
		if best["value"] > tmp:
			best["value"] = tmp
			best["index"] = i
	return (best["index"], best["value"])

# functino get_standard_deviation 
#
# Calculates Standard Deviation for all least square differences from given iteration.
#
def get_standard_deviation(iteration_array, iteration):
	dis = []
	for n in range(len(iteration_array)):
		if iteration == n:
			continue
		dis.append(least_squares(iteration_array[iteration], iteration_array[n]))
	return np.std(dis)	
