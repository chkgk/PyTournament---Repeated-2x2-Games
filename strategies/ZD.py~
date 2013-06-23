import sys, os
sys.path.append(os.path.abspath('../tournament.py'))
#sys.path.append('~/Dokumente/PyTournament---Repeated-2x2-Games/tournament.py')
import random
import tournament
#from tournament import determine_payoff

class ZD:
	def move(self, game, player, history):

		# play zero determinant strategy in prisoner's dilemma and otherwise all B
		if game == "prison":
			# set ZD strategy factors
			extortion_factor = 2
			phi = float(1)/8
			# range of phi: 0 < phi < (P-S)/((P-S) + extortion_factor*(T-P)) = 1/(1+2*extortion_factor)
		
			# set payoffs
			R = tournament.determine_payoff("prison", "a", "a")[0]
			S = tournament.determine_payoff("prison", "a", "b")[0]
			T = tournament.determine_payoff("prison", "b", "a")[0]
			P = tournament.determine_payoff("prison", "b", "b")[0]
		
			#print "R: " + str(R)
			#print "S: " + str(S)
			#print "T: " + str(T)
			#print "P: " + str(P)
		
			# set probabilities
			p1 = 1 - float(R-P)/float(P-S)*phi*(extortion_factor - 1)
			p2 = 1- phi*(float(T-P)/float(P-S)*extortion_factor + 1)
			p3 = phi*(extortion_factor + float(T-P)/float(P-S))
			p4 = 0
		
			#print "p1: " + str(p1)
			#print "p2: " + str(p2)
			#print "p3: " + str(p3)
			#print "p4: " + str(p4)
		
		
			# get random value to determine behaviour
			random.seed()
			rdm = random.random()
		
			# first round cooperate
			if not history:
				return "a"
		
			# print history
			#print "move: (" + str(history[-1][0]) + "," + str(history[-1][1]) + ")"
		
			# set behaviour for rounds
			if history[-1][0] == "a" and history[-1][1] == "a":
				if rdm < p1:
					return "a"
				else:
					return "b"
				
			if history[-1][0] == "a" and history[-1][1] == "b":
				if rdm < p2:
					return "a"
				else:
					return "b"
				
			if history[-1][0] == "b" and history[-1][1] == "a":
				if rdm < p3:
					return "a"
				else:
					return "b"
		
			if history[-1][0] == "b" and history[-1][1] == "b":
				if rdm < p4:
					return "a"
				else:
					return "b"
		

		else:
			return "b"
