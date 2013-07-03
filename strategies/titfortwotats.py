# strategy titfortats
# parameters: game (string), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements the strategy tit-for-two-tats
# which is similar to tit-for-tat but retaliates only after 
# the opponent has defected twice.
# It starts with "a" if the history is empty.
#
class titfortwotats:

        def move(self, game, player, history):
                if not history:
                        return "a"
                elif len(history) == 1:
                        return "a"
                else:
                        if history[-1][1] == "b" and history[-2][1] == "b":
                                return "b"
                        else:
                                return "a"


