# strategy titfortat_B
#
# returns: "a" or "b" (string)
#
# This function implements a version of tit-for-tat
# which also starts with "a" but retaliates a defection
# of the other player only with probability 1/4


import random
class titfortat_B:

        def move(self, game, player, history):
                if not history:
                        return "a"
                else:
                        if history[-1][1] == "a" and random.randint(0,3) != 0:
                                return "a"
                        else:
                                return "b"


