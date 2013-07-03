# strategy B_titfortat
# parameters: game (string), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements the strategy tit-for-tat
# which mirrors the other player's last action,
# starting with "b" if the history is empty.
#
class B_titfortat:

        def move(self, game, player, history):
                if not history:
                        return "b"
                else:
                        if history[-1][1] == "a":
                                return "a"
                        else:
                                return "b"


