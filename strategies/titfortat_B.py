import random
#same as titfortat but plays b with a probability
class titfortat_B:

        def move(self, game, player, history):
                if not history:
                        return "a"
                else:
                        if history[-1][1] == "a" and random.randint(0,3) != 0:
                                return "a"
                        else:
                                return "b"


