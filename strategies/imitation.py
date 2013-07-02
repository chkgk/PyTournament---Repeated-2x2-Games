import random
import tournament

# Strategy: imitation
# parameters: game (string), player (int), history (list of tupels)
# returns: "a" or "b" (string)
#
# This function implements so called imitation strategy.
# First, each strategy is chosen with equal probability. 
# In subsequent rounds, the previous round's winning strategy is played. 
#
class imitation:

        def move(self, game, player, history):

                if not history: # first round - randomize
                        if random.randint(0,1) == 0: # play "a" or "b" with prob. 1/2
                                return "a"
                        else:
                                return "b"
                else: # determine payoffs of last round
                        last_payoffs = tournament.determine_payoff(game, history[-1][0], history[-1][1])

                        best_result = max(last_payoffs) 
                        
                        for i in range(len(last_payoffs)): # look up which player got the best payoff this round
                                if last_payoffs[i] == best_result:
                                        best_key = i

                        return history[-1][best_key] # play the best strategy of last round

