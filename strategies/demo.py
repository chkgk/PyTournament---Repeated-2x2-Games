# Strategy: demo
# parameters: game (string), player (int), history (list of tupels)
# returns: "a" or "b" (string)
#
# This strategy implementation is supposed to be a helping hand in the development of own strategies.
# The basic structure is as follows: Each time the function "move" is called, it is supposed to answer
# with either "a" or "b", depending on which strategy it decides to play.
#
# To make this decision, it is given the name of the game which is played as the parameter "game", which 
# can take the values "prison", "staghunt", "chicken" or "pennies".
#
# It is also given the player number it has been assigned in this iteration. The parameter "player" takes
# integer values 1 or 2. This information is needed when playing the game "pennies".
#
# Finally, the funcion is given the history of all previous rounds against the same opponent strategy. 
# The history is a list of tupels.
# 
# An example illustrates the structure: [("a","b")] is a possible history after 
# a single (first) round. 
# It  only containts one element (only one round played). This element again contains two elements,
# one for each players' choice in that round. The first element is always the own choice, the second
# is the opponent's choice.
#
# Using the history in python is easy and follows the form: history[round][player]
# In our example history[0][0] would evaluate to "a" and thus represent our own choice in round 1.
# history[0][1] would evaluate to "b" and represent our opponent's choice in round 1.
# Note that both list indices start with 0 as the first element!
# 
# Accessing the last item of a list is also easy and can be done using "-1":
# history[-1][1] gives our opponent's move in the last round that has been played.
#
# Now take a look at a very basic structure of the function move
def move(game, player, history):
	# if history is empty, we are in the very first round. Let's cooperate!
	if not history: 
		return "a"
	else: # if we have a history, decide what to do based on which game we are playing:
		if game == "prison":
			# play some prisoners dilemma strategy...
			return "a"
		elif game == "staghunt": # elif is short for "else, if..."
			# play some staghung strategy...
			return "a"
		elif game == "chicken":
			# play some chicken strategy...
			return "a"
		elif game == "pennies":
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


