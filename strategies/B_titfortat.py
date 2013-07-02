#same as titfortat but starts with B
class B_titfortat:

        def move(self, game, player, history):
                if not history:
                        return "b"
                else:
                        if history[-1][1] == "a":
                                return "a"
                        else:
                                return "b"


