# function pavlov
# parameters: game (string), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements the strategy pavlov
# which is to cooperate only if both players chose the same action
# in the last round and to defect otherwise.
#
def move(game, player, history):
	if not history:
		return "a"
	else:
		if history[-1][0] == history[-1][1]:
			return "a"
		else:
			return "b"


