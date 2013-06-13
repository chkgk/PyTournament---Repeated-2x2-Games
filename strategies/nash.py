import random

# Strategy: nash
# parameters: game (string), player (int), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements a strategy which always plays a nash equilibrium
# if multiple equilibrium strategies exist, one is chosen randomly.
#

def move(game, player, history):
	if game == "prison":
		# Nash EQ is to always defect.
		return "b"

	elif game == "staghunt": 
		# pure Nash EQ are aa, bb. mixed eq is to play A with p=3/5 
		eq_to_play = random.randint(1,3)
		if eq_to_play == 1:
			return "a"
		elif eq_to_play == 2:
			return "b"
		else:
			if random.randint(1,5) <= 3: 
				return "a"
			else:
				return "b"
	
	elif game == "chicken":
		# again there are two pure eq strategies and one mixed strategy eq: play a with 1/2
		eq_to_play = random.randint(1,3)
		if eq_to_play == 1:
			return "a"
		elif eq_to_play == 2:
			return "b"
		else:
			if random.randint(0,1) == 1: 
				return "a"
			else:
				return "b"

	elif game == "pennies":
		# unique nash eq in mixed strategies is to play each strategy with p=1/2
		if random.randint(1,5) <= 3: 
			return "a"
		else:
			return "b"