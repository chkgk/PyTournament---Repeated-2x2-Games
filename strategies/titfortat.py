# function titfortat
# parameters: game (string), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements the strategy tit-for-tat
# which mirrors the other player's last action,
# starting with "a" if the history is empty.
#
class titfortat:

        def move(self, game, player, history):
                if not history:
                        return "a"
                else:
                        if history[-1][1] == "a":
                                return "a"
                        else:
                                return "b"


