#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import argparse
import tournament as tm
import leaderboard

# function load_strategies
# parameters: path(string)
# returns: dict(string, function), using the filename without .py as name and 
#	maps that to the move function in that file
#
def load_strategies(path):
	strategies = {}
	sys.path.append(os.path.join(path))
	for root, dirs, files in os.walk(path):                                             
		for filename in files:
			split = os.path.splitext(filename)
			name = split[0]
			if name[0] == "." or split[1] != ".py":
				pass
			else:
				module = __import__(name)
                                strategies.update({name: getattr(module,name)()})
	return strategies 

def prepare_parser(parser):
	game_names = ["prison", "staghunt", "chicken", "pennies"]
	# get neccessary information from arguments
	parser.add_argument("game", help="game", type=str, choices=game_names)
	parser.add_argument("-n", "--rounds", \
		help="number of rounds (default: 1000 + X)", type=int, \
		default=-1)
	parser.add_argument("-i", "--iterations", \
		help="number of iterations (default: 100)", \
		type=int, default=100)
	parser.add_argument("-p", "--plot", \
		help="plot a single iteration of two strategies", \
		nargs=3, metavar=("iteration", "stratA", "stratB"))
	parser.add_argument("-s", "--strategies", \
		help="path to strategy files (default: ./strategies)", \
		default="./strategies")
	parser.add_argument("-f", "--focus", \
		help="focus on two strategies and play only those - requires -p", \
		action="store_true")
	parser.add_argument("-a", "--analyse", \
		help="define which strategy to analyse",\
		type=str)
	parser.add_argument("-pm", "--plotmulti", \
		help="plot a single iteration of multiple stategies and save the graphs",\
		nargs="*")

def get_strategies(args):
	strategies = load_strategies(args.strategies)
	if args.focus:
		new_strategies = {}
		for i in range(1, 3):
			new_strategies[args.plot[i]] = strategies[args.plot[i]]
		strategies = new_strategies
	
	return strategies

def get_rounds(i):
	if i == -1:
		return "1000 + X"
	else:
		return str(i)
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	prepare_parser(parser)
	args = parser.parse_args()
	
	strategies = get_strategies(args)
	os.system('clear')

	print "Running " + str(args.iterations)+ \
		" iterations with " + get_rounds(args.rounds) + \
		" rounds of a Round-Robin Tournament of " + args.game + "..."
	tournament_start = time.time()
	tournament_results = tm.play_tournament(args.game, strategies, \
		args.iterations, args.rounds)
	print "Finished. Tournament took "+str(round(time.time()-tournament_start, 1)) + \
		" seconds to run."
	print "Calculating results..."

	print "\nLeaderboard:"

	print leaderboard.get_leaderboard(args.game, tournament_results)

	if args.analyse:
		try:
			game_analyser = __import__("game_analyser")
		except ImportError:
			print "NumPy and MatPlotLib are required for these functions."
			sys.exit(1)
		print "Presenting Analysis for "+args.analyse+":\n"
		preppedRes = game_analyser.prep_for_analysis(args.game, args.analyse, tournament_results)
		print game_analyser.analyse_strategy(args.game, args.analyse, preppedRes)

	if args.plotmulti:
		try:
			plotter = __import__("plotter")
		except ImportError:
			print "NumPy and MatPlotLib are required for these functions."
			sys.exit(1)

		strats = ""
		for strategy in args.plotmulti[2:]:
			strats += strategy + ", "

		print "Saving plots for " + args.plotmulti[1] + " vs. " + strats[:-2]
		plotter.prepare_figure(args.game)
		plotter.plot_multi(args.game,args.plotmulti[1],args.plotmulti[2:], \
				int(args.plotmulti[0])-1, tournament_results)
		print "done."
		print ""

	if args.plot:
		try:
			plotter = __import__("plotter")
		except ImportError:
			print "NumPy and MatPlotLib are required for these functions."
			sys.exit(1)

		print "Plotting graphs of iteration " + args.plot[0] + " of "+ \
			args.plot[1] +" vs. "+args.plot[2]
		plotter.prepare_figure(args.game)
		if plotter.plot_game(args.game,args.plot[1],args.plot[2], \
			int(args.plot[0])-1, tournament_results): 
			# iterations go from 0-99 but users will input 1-100
			#game_analyser.save_figure("test.png")
			plotter.show_figure()
