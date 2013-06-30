import sys, os
sys.path.append(os.path.abspath('../tournament.py'))
import random
import tournament

class reinforced_learning:

	# set initial reinforcement level
	reflvl_a = 10
	reflvl_b = 10

	def move(self, game, player, history):

		if game == "prison":
			
			# first round action
			if not history:
				# calculate probabilities
				p_a = float(self.reflvl_a) / (self.reflvl_a + self.reflvl_b)
				p_b = 1 - p_a	# p_b = float(self.reflvl_b) / (self.reflvl_a + self.reflvl_b)
				
				random.seed()
				rdm = random.random()
				#print "rdm: " + str(rdm)
				
				if rdm < p_a:
					#print "a"
					return "a"
				else:
					#print "b"
					return "b"
		
		
			# adjust reinforcfement levels
			if history[-1][0] == "a":
				self.reflvl_a = self.reflvl_a + tournament.determine_payoff("prison", "a", history[-1][1])[0]
		
			if history[-1][0] == "b":
				self.reflvl_b = self.reflvl_b + tournament.determine_payoff("prison", "b", history[-1][1])[0]
		
			#print "reflvl_(a,b): (" + str(self.reflvl_a) + ", " + str(self.reflvl_b) + ")"
			
			# calculate probabilities
			p_a = float(self.reflvl_a) / (self.reflvl_a + self.reflvl_b)
			p_b = 1 - p_a	# p_b = float(self.reflvl_b) / (self.reflvl_a + self.reflvl_b)
			
			#print "probabilities (a,b): (" + str(p_a) + ", " + str(p_b) + ")"
		
		
			# choose action
			random.seed()
			rdm = random.random()
			#print "rdm: " + str(rdm)
		
			if rdm < p_a:
				#print "a"
				return "a"
			else:
				#print "b"
				return "b"
		
	
		else:
			return "b"
