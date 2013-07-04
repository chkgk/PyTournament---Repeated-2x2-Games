# strategy feld
#
# returns: "a" or "b" (string)
#
# This function implements a version of tit-for-tat
# which also starts with "a" but has a linearily
# increasing probability to defect without a reason.
# probability starts with p=0 in round 1, then increases by 
# 0.5 percentage points up to round 100.
# That is, in round 100, a is played only with a prob. of 50%, 
# given the other player cooperated in round 99.


import random
class feld:

        def move(self, game, player, history):
                if not history:
                        return "a"
                else:
                        if history[-1][1] == "a" and (random.randint(1,10000) >= (len(history)*50)):
                                return "a"
                        else:
                                return "b"


