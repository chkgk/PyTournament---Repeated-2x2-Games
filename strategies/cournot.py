import random

# Strategy: cournot
# parameters: game (string), player (int), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements so called cournot adjustment.
# First, each strategy is chosen with equal probability. In subsequent rounds, the best response to the opponent's 
# strategy in the previous round is played.
#
class cournot:

        def move(self, game, player, history):

                br_prison = {"a":"b", "b":"b"}
                br_staghunt = {"a":"a","b":"b"}
                br_chicken = {"a":"b","b":"a"}
                br_pennies_p1 = {"a":"a","b":"b"}
                br_pennies_p2 = {"a":"b","b":"a"}

                best_response = {"prison":br_prison, "staghunt":br_staghunt, "chicken":br_chicken, "pennies_p1":br_pennies_p1, "pennies_p2":br_pennies_p2}

                if not history: # first round
                        if random.randint(0,1) == 0: # play "a" or "b" with prob. 1/2
                                return "a"
                        else:
                                return "b"
                else: # subsequent rounds
                        if game == "pennies": # if we play matching pennies, the player number matters for the best response
                                if player == 1:
                                        game = "pennies_p1"
                            else:
                                    game = "pennies_p2"	
                    return best_response[game][history[-1][1]]



