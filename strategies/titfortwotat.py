# function titfortwotat
# parameters: game (string), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements the strategy tit-for-two-tat
# which only retaliates if the other player defected twice,
# starting with "a" if the history is empty.
#
class titfortwotat:
	def move(self, game, player, history):
		if not history:
			return "a"
		else:
			if history[-1][1] == "a":
				return "a"
			else:
				if len(history) > 1 and history[-2][1] == "b":
					return "b"
				else:
					return "a"
