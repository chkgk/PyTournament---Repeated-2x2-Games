# strategy pavlov
# parameters: game (string), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements the strategy pavlov (win-stay loose-shift)
# which is to cooperate only if both players chose the same action
# in the last round and to defect otherwise.
#
class pavlov:

        def move(self, game, player, history):
                if not history:
                        return "a"
                else:
                        if history[-1][0] == history[-1][1]:
                                return "a"
                        else:
                                return "b"


