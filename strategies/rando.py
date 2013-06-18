import random

# function rando
# parameters: game (string), history (list of tupels)
# returns: "a" or "b" (string)
#
class rando:

        def move(self, game, player, history):
                if random.randint(0,1) == 0: # play "a" or "b" with prob. 1/2
                        return "a"
                else:
                        return "b"


