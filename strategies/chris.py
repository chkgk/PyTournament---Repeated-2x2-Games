# Strategy: demo
# parameters: game (string), player (int), history (list of tupels)
# returns: "a" or "b" (string)

import random
import tournament

def move(game, player, history):
	# if history is empty, we are in the very first round. Let's cooperate!
	if game == "prison": # in Prisoners' Dilemma I play imitation.
		if not history: # first round - randomize
			if random.randint(0,1) == 0: # play "a" or "b" with prob. 1/2
				return "a"
			else:
				return "b"
		else: # determine payoffs of last round
			last_payoffs = tournament.determine_payoff(game, history[-1][0], history[-1][1])

			if game == "prison": # for prisoners dilemma, lower values are better!
				best_result = min(last_payoffs)
			else:
				best_result = max(last_payoffs)

			for i in range(len(last_payoffs)): # look up which player got the best payoff this round
				if last_payoffs[i] == best_result:
					best_key = i

			return history[-1][best_key] # play the best strategy of last round
	
	elif game == "staghunt": # in staghunt I play grimtrigger
		if not history: # first round cooperate
			return "a"

		else: 

			sumB = 0
			for run in history: # let's count how often opponent defected so far
				if run[1] == "b":
					sumB =+ 1

			if sumB == 0: # if no defect, play a
				return "a"
			else: # if opponent ever defected, play b
				return "b"
	elif game == "chicken": # in chicken i play cournot adjustment

		best_response = {"chicken":{"a":"b","b":"a"}}

		if not history: # first round
			if random.randint(0,1) == 0: # play "a" or "b" with prob. 1/2
				return "a"
			else:
				return "b"
		else: # subsequent rounds
			return best_response[game][history[-1][1]]

	elif game == "pennies":
		if not history:
			return "a";
		else:
			if player == 1: # when playing matching pennies, player number (1 = row, 2 = column) matters:
				if history[-1][1] == "a": # if I am player one, I want matching choices
					return "a" # let's mirror what the other has done in his last round
				else:
					return "b"
			else: # if I am not player 1, I must be player 2, so i don't want matching choices:
				if history[-1][1] == "a":
					return "b" # let's do the opposite of what the other did last round.
				else:
					return "a"


