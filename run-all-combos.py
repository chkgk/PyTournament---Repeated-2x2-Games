#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
from math import *
import argparse
import tournament as tm
import leaderboard
import itertools

import matplotlib.pyplot as plt
# function load_strategies
# parameters: path(string), allowed(list)
# returns: dict(string, function), using the filename without .py as name and 
#               produces an instance of the corresponding class	
#			excludes all which are not in the allowed list.
#


#-------------
#Change strategy under test here!
#-------------
ANALYSE = "allA"



def load_strategies(path, allowed):
	strategies = {}
	available = get_strategy_list(path)
	for strategy in available:
		if strategy[0] in allowed.keys() and strategy[1] == ".py":
                        for i in range(allowed[strategy[0]]):
                                #loading the module
                                module = __import__(strategy[0])
                                #producing an instance of the strategy class
                                strategies.update({strategy[0]+str(i): getattr(module,strategy[0])()})

	return strategies 

def get_strategy_list(path):
	strategies = []
	split = []
	sys.path.append(os.path.join(path))
	for root, dirs, files in os.walk(path):                                             
		for filename in files:
			split = os.path.splitext(filename)
			if split[1] == ".py" and split[0][0] != ".":
				strategies.append(split)
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
	# parser.add_argument("-p", "--plot", \
	# 	help="plot a single iteration of two strategies", \
	# 	nargs=3, metavar=("iteration", "stratA", "stratB"))
	parser.add_argument("-s", "--strategies", \
		help="path to strategy files (default: ./strategies)", \
		default="./strategies")
	parser.add_argument("-f", "--focus", \
		help="focus on two strategies and play only those - requires -p", \
		action="store_true")
	# parser.add_argument("-a", "--analyse", \
	# 	help="define which strategy to analyse",\
	# 	type=str)
	# parser.add_argument("-pm", "--plotmulti", \
	# 	help="plot a single iteration of multiple stategies and save the graphs",\
	# 	nargs="*")
	# parser.add_argument("-pall", "--plotall", \
	# 	help="plot and save average payoffs over iterations per round/total for all strategy combinations to destination (default ./plots/)")
	parser.add_argument("-sl", "--strategylist", \
		help="supply a list of strategies to be included in the tournament", \
		nargs="*")

	parser.add_argument("-ps", "--poolsize", \
		help="specify how much strategies in total are used", \
		nargs=1, default=5)

def get_strategies(args, allowed):
	strategies = load_strategies(args.strategies, allowed)
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
	

	if args.strategylist: # if strategylist is given, only allow those strategies for the tournament
		allowed = args.strategylist
                allowed.remove(ANALYSE)
	else: # allow all strategies to enter the tournament
		allowed = []
		for name in get_strategy_list(args.strategies):
                        if name != ANALYSE:
                                allowed.append(name[0])
	
	if args.poolsize: #fixed number of strategies who are playing the tourny
		poolsize = int(args.poolsize[0])
        else:
                poolsize = 5

        all_strategy_lists = []

        np = int(poolsize)
        ns = len(allowed)
        
        #print str(s) + " " + str(p)
        #print str(p+s-1) + " over " + str(s-1)
        
        for i in range(int(pow(np+1,ns))):
                sl = {}
                sl.update({ANALYSE: 1})

                j = i
                c = 1
                summe = 0
                for s in allowed:
                        f = int((j/pow(np+1,ns-c))%(np+1))
                        #print "i: " + str(i) + "\t j: " + str(j) + "\t f: " + str(f) + "\t " + s

                        sl.update({s: f})
                        summe += f
                        c += 1

                if summe == np:
                        print sl
                        all_strategy_lists.append(sl)


	#for L in range(2, len(allowed)+1):
		#for subset in itertools.combinations(allowed, L):
			#allcombinations.append(subset)

        vs_rank = {}
        #relative payoff
        vs_rPayoff = {}
        #absolute payoff
        vs_aPayoff = {}
        vs_count = {}

        #produce empty dicts
        for s in allowed:
                vs_rank.update({s: []})
                vs_rPayoff.update({s: []})
                vs_aPayoff.update({s: []})
                vs_count.update({s: []})
                for i in range(poolsize+1):
                        vs_rank[s].append(0)
                        vs_rPayoff[s].append(0)
                        vs_aPayoff[s].append(0)
                        vs_count[s].append(0)

	# now we run a separate tournament for each possible combination of strategies generated above
	for strategycombo in all_strategy_lists:
		strategies = get_strategies(args, strategycombo)

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

                #get important data
                lb_data = leaderboard.get_lb_data(args.game, tournament_results)
                
                #produce counting list
                count_strat = {}
                for s in allowed:
                        count_strat.update({s: 0})

                for s in lb_data.keys():
                        for t in allowed:
                                if s[:-1] == t:
                                        count_strat[t] += 1


                #produce testing vs strategy dicts
                for s in allowed:
                        c = count_strat[s]
                        vs_aPayoff[s][c] += lb_data[ANALYSE+"0"][0]
                        vs_rPayoff[s][c] += lb_data[ANALYSE+"0"][1]
                        vs_rank[s][c] += lb_data[ANALYSE+"0"][2]
                        vs_count[s][c] += 1
                
        fig_number = 1

        #get average and print
        for s in allowed:
                for i in range(poolsize+1):
                        vs_aPayoff[s][i] = vs_aPayoff[s][i]/float(vs_count[s][i])
                        vs_rPayoff[s][i] = vs_rPayoff[s][i]/float(vs_count[s][i])*float(100)
                        vs_rank[s][i] = vs_rank[s][i]/float(vs_count[s][i])


                path = "./plots_combos/"
                path_rank = path + args.game + "/rank/"
                path_relP = path + args.game + "/relative_Payoff/"

                if not os.path.exists(path_rank):
                        os.makedirs(path_rank)

                if not os.path.exists(path_relP):
                        os.makedirs(path_relP)

                #plot average rank
                plt.figure(fig_number)
                plotname = path_rank+ANALYSE+"_vs_"+s+".pdf"
                title = "Average Rank of "+ANALYSE+" vs "+s
                plt.plot(range(poolsize+1),vs_rank[s],label=ANALYSE)
                #plt.legend(loc="upper left")
                plt.title(title)
                plt.axis([0,poolsize,poolsize+1,0])
                plt.xlabel("# of "+s+" in pool")
                plt.ylabel("rank")
                plt.savefig(plotname)
                fig_number += 1
                
                equal_share = []
                for i in range(poolsize+1):
                        equal_share.append(1.0/float(poolsize+1)*100)
                #plot average relative Payoff
                plt.figure(fig_number)
                plotname = path_relP+"rel_"+ANALYSE+"_vs_"+s+".pdf"
                title = "Average relative Payoff of "+ANALYSE+" vs "+s
                plt.plot(range(poolsize+1),vs_rPayoff[s],label=ANALYSE)
                plt.plot(range(poolsize+1),equal_share,label="equal share")
                #plt.legend(loc="upper left")
                plt.title(title)
                plt.axis([0,poolsize,0,30])
                plt.xlabel("# of "+s+" in pool")
                plt.ylabel("relative Payoff [%]")
                plt.savefig(plotname)
                fig_number += 1
