# Strategies testing will trigger an unbreakable BB:
#       1:      grimmtrigger
#       1/2:    immitation
#
# Strategies that can be exploited:
#       1:      allA
#       1/2:    tftt, pavlov
#
# Detection works for:
#       allA, allB(cournot, nash), rando, tft, tftt, pavlov, grimtrigger, imitation
#
#
# Results:
#       performs very good without testing in the pool: 
#               gt, tft, tftt, immi, allA, allB, rando
#       --> similiar to gt!!!
#       --> 1st place with gt
#       --> slightly better then tft, because he exploits rando
#
# vim:foldmethod=marker

class testing:

        #number of strategies
        NOS = 10

        TESTING_ROUND = 10
        
        #number of rejected strategies
        rejected = 0

        belief = {}

        observed_A = 0
        observed_B = 0

        played_A = 0
        played_B = 0

        always_B = False
        always_A = False
        always_AB = False

        detected = False

        def __init__(self):
                self.reset()

        
        def reset(self):
                self.belief.update({"allA": 1/float(self.NOS)})
                self.belief.update({"allB": 1/float(self.NOS)})
                self.belief.update({"rando": 1/float(self.NOS)})
                self.belief.update({"tft": 1/float(self.NOS)})
                self.belief.update({"cournot": 1/float(self.NOS)})
                self.belief.update({"pavlov": 1/float(self.NOS)})
                self.belief.update({"gt": 1/float(self.NOS)})
                self.belief.update({"imitation": 1/float(self.NOS)})
                self.belief.update({"nash": 1/float(self.NOS)})
                self.belief.update({"tftt": 1/float(self.NOS)})

                self.rejected = 0

                self.observed_A = 0
                self.observed_B = 0

                self.played_A = 0
                self.played_B = 0

                self.always_B = False


        def normalize(self):
                s = 0
                for bel in self.belief.values():
                        s += bel

                for strat in self.belief.keys():
                        if s != 0:
                                self.belief[strat] = self.belief[strat]/float(s)
                        else:
                                self.reset()
        
        def set_bel_zero(self):
                for s in self.belief.keys():
                        self.belief[s] = 0

        def set_detected(self):
                for s in self.belief.keys():
                        if self.belief[s] < 0.001:
                                self.belief[s] = 0
                self.normalize()

        def play(self,x):
                self.normalize()
                self.set_detected()
                if(x == "a"):
                        self.played_A += 1
                        return "a"
                else:
                        self.played_B += 1
                        return "b"

        def move(self, game, player, history):
                
                if game == "prison": #{{{
                        #first turn cooperate
                        if not history:
                                self.reset()
                                return self.play("a")

                        else:
                                last_i = history[-1][0]
                                last_he = history[-1][1]
                                if last_he == "a":
                                        self.observed_A += 1
                                else:
                                        self.observed_B += 1

                        #round
                        r = len(history)
                        if False:
                                print "Round: " + str(r-1)
                                for i in self.belief.keys():
                                       print i + ": " + str(self.belief[i])
                                print "-> ("+last_i + "," + last_he + ")"
                                print ""

                        #first round
                        if r == 1:
                                #print "First: (a, " + last_he + ")"
                                if self.observed_A == 0:
                                        self.belief["allA"] = 0
                                        self.belief["tft"] = 0
                                        self.belief["tftt"] = 0
                                        self.belief["pavlov"] = 0
                                        self.belief["gt"] = 0

                                        self.belief["allB"] = 2
                                        self.belief["nash"] = 2
                                        self.belief["rando"] = 1
                                        self.belief["cournot"] = 1
                                        self.belief["imitation"] = 1

                                        self.normalize()
                                        self.always_B = True
                                        #self.detected = True
                                        #print "Detected AllB! In round " + str(r) + ". Play B"
                                        return self.play("b")
                                if self.observed_B == 0:
                                        self.belief["allB"] = 0
                                        self.belief["nash"] = 0

                                        self.belief["allA"] = 2
                                        self.belief["tft"] = 2
                                        self.belief["tftt"] = 2
                                        self.belief["gt"] = 2
                                        self.belief["pavlov"] = 2
                                        self.belief["rando"] = 1
                                        self.belief["cournot"] = 1
                                        self.belief["imitation"] = 1

                                        self.normalize()
                                        return self.play("a")
                        else:

                                if not self.detected:
                                        if last_he == "a":
                                                self.belief["allB"] = 0
                                                self.belief["nash"] = 0
                                                self.belief["cournot"] = 0

                                                if history[-2][0] == "b":
                                                        self.belief["tft"] = 0
                                                        self.belief["gt"] = 0
                                                        self.belief["imitation"] = 0
                                                        if history[-3][0] == "b":
                                                                self.belief["tftt"] = 0

                                                if self.observed_B == 0:
                                                        self.belief["rando"] = self.belief["rando"]/float(2)
                                                else: 
                                                        self.belief["gt"] = 0
                                                        self.belief["imitation"] = 0
                                                        #if history[-3][0] == "b":
                                                                #print "###Hello!###"
                                                                #self.set_bel_zero()
                                                                #self.belief["rando"] = 1
                                                                #self.always_B = True
                                                                #self.detected = True

                                        if last_he == "b":
                                                self.belief["allA"] = 0

                                                #if he played B, what we played A before, it cannot be tft
                                                if history[-2][0] == "a":
                                                        self.belief["tft"] = 0

                                                #if we observe a B, but we never played one and he also played an A before
                                                #the strategy has to be rando
                                                if r == 2:
                                                        if last_he == "b" and history[0][1] == "a":
                                                                self.belief["gt"] = 0
                                                                self.belief["pavlov"] = 0
                                                                self.belief["tft"] = 0
                                                                self.belief["tftt"] = 0

                                                if self.played_B == 0 and self.observed_A != 0 and r>2:
                                                        self.set_bel_zero()
                                                        self.belief["rando"] = 1
                                                        #self.always_B = True
                                                        #self.detected = True
                                                        #print "Detected Random! In round " + str(r) + ". Play B"

                                                if self.observed_A == 0:
                                                        self.belief["rando"] = self.belief["rando"]/float(2)

                                        #if self.always_B: 
                                                #self.detected = True
                                                #return self.play("b")
                                        

                                        if not self.detected and r == self.TESTING_ROUND:
                                                #print "TESTING"
                                                return self.play("b")

                                        if not self.detected and r == self.TESTING_ROUND+1:
                                                return self.play("b")
                                        if not self.detected and r == self.TESTING_ROUND+2:
                                                if last_he == "a":
                                                        self.belief["tft"] = 0
                                                        self.belief["gt"] = 0
                                                        self.belief["imitation"] = 0
                                                        self.belief["pavlov"] = 0
                                                else:
                                                        self.belief["tftt"] = 0

                                                return self.play("a")

                                        if not self.detected and r == self.TESTING_ROUND+3:
                                                if last_he == "a":
                                                        self.belief["imitation"] = 0
                                                else:
                                                        self.belief["pavlov"] = 0

                                                return self.play("a")

                                        if not self.detected and r == self.TESTING_ROUND+4:
                                                if last_he == "a":
                                                        self.belief["imitation"] = 0


                                        if self.belief["allA"] == 1:
                                               #print "Detected AllA! In round "+str(r)+". Play B"
                                                self.always_B = True
                                                self.detected = True

                                        elif self.belief["allB"] == 1:
                                               #print "Detected AllB! In round "+str(r)+". Play B"
                                                self.always_B = True
                                                self.detected = True

                                        elif self.belief["rando"] == 1:
                                               #print "Detected rando! In round "+str(r)+". Play B"
                                                self.always_B = True
                                                self.detected = True

                                        elif self.belief["tft"] == 1:
                                               #print "Detected tft! In round "+str(r)+". Play A"
                                                self.always_A = True
                                                self.detected = True

                                        elif self.belief["cournot"] == 1:
                                               #print "Detected cournot! In round "+str(r)+". Play B"
                                                self.always_B = True
                                                self.detected = True

                                        elif self.belief["pavlov"] == 1:
                                               #print "Detected Pavlov! In round "+str(r)+". Play A"
                                                self.always_B = True
                                                self.detected = True
                                                
                                        elif self.belief["gt"] == 1:
                                               #print "Detected grimtrigger! In round "+str(r)+". Play B"
                                                self.always_B = True
                                                self.detected = True

                                        elif abs(self.belief["gt"]+self.belief["imitation"]-1) < 0.001:
                                               #print "Detected a grimtrigger-like strategy! In round "+str(r)+". Play B"
                                                self.always_B = True
                                                self.detected = True

                                        elif self.belief["imitation"] == 1:
                                               #print "Detected imitation! In round "+str(r)+". Play B"
                                                self.always_B = True
                                                self.detected = True

                                        elif self.belief["tftt"] == 1:
                                               #print "Detected tftt! In round "+str(r)+". Play AB"
                                                self.always_AB = True
                                                self.detected = True

                                        elif self.belief["nash"] == 1:
                                               #print "Detected Nash! In round "+str(r)+". Play B"
                                                self.always_B = True
                                                self.detected = True

                                        elif abs(self.belief["nash"]+self.belief["allB"]+self.belief["cournot"]+self.belief["imitation"] -1) < 0.001:
                                               #print "Detected a AllB-like Strategy! In round "+str(r)+". Play B"
                                                self.always_B = True
                                                self.detected = True
#}}}

                        if self.always_A:
                                return self.play("a")
                        elif self.always_B:
                                return self.play("b")
                        elif self.always_AB:
                                if last_i == "a":
                                        return self.play("b")
                                else:
                                        return self.play("a")



                        if history[-1][1] == "a":
                                return self.play("a")
                        else:
                                return self.play("b")


