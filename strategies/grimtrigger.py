import random
import tournament

# Strategy: grimtrigger
# parameters: game (string), player (int), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements so called grim trigger strategy.
# It cooperates until the opponent defects once, then it always defects. 
#
class grimtrigger:

    def move(self, game, player, history):

            if not history: # first round cooperate
                    return "a"

            else: 

                    sumB = 0
                    for run in history: # let's count how often opponent defected so far
                            if run[1] == "b":
                                    sumB =+ 1

                    if sumB == 0: # if no defect, play a
                            return "a"
                    else: # if opponent ever defected, play b
                            return "b"
