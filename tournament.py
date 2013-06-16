import random

# function determine_payoff
# parameters: game, p1Act, p2Act (all string)
# returns: payoff (tuple)
#
def determine_payoff(game, p1Act, p2Act):
	#print "play:" + p1Act + " " + p2Act
	if p1Act != "a" and p1Act != "b":
		raise MoveException(1)
	if p2Act != "a" and p2Act != "b":
		raise MoveException(2)
	games = {
		'prison':{'aa':(1,1), 'ab':(3,0), 'ba':(0,3), 'bb':(2,2)},
		'staghunt':{'aa':(8,8), 'ab':(0,4), 'ba':(4,0), 'bb':(6,6)},
		'chicken':{'aa':(2,2), 'ab':(1,3), 'ba':(3,1), 'bb':(0,0)},
		'pennies':{'aa':(1,-1), 'ab':(-1,1), 'ba':(-1,1), 'bb':(1,-1)}
	}
	code = p1Act+p2Act #combine actions to reference cell of normal form game
	return games[game][code]; # return corresponding payoff

# function play_round
# parameters: game(string), history(array), strnatA(instance), stratB(instance)
# returns: tuple(string, string)
#
def play_round(game, historyA, historyB, stratA, stratB):
	PLAYER_1 = 1
	PLAYER_2 = 1
	
	try:
		a = stratA.move(game, PLAYER_1, historyA)
	except Exception as e:
		me = MoveException(1)
		me.exception = e
		raise me
	try:
		b = stratB.move(game, PLAYER_2, historyB)
	except Exception as e:
		me = MoveException(2)
		me.exception = e
		raise me
	if a != "a" and a != "b":
		raise MoveException(1)
	if b != "a" and b != "b":
		raise MoveException(2)
	# keep the player position in matching pennies game
	if game == "pennies":
		return ((a, b), (b, switch_move(a)))
	return ((a, b), (b, a))

def switch_move(move):
	return "a" if move == "b" else "b"

# function determine_rounds
# Determines the number of played rounds. After 1000 rounds each round ends with independet
# chance of 1/10.
# parameters: -
# returns: number of rounds 
#
def determine_rounds():
	i = 1000
	while random.randint(0, 9) != 0:
		i += 1
	return i

# function play_game
# Returns an array with the history of all rounds. Each round is represented by
#	a touple of two
# strings containing the player moves.
# parameters: game(string), rounds(int), stratA(instance), stratB(instance)
# returns: history object containing the respective history for playerX's point
# 	of view
#
def play_game(game, rounds, stratA, stratB):
        histA = []
	histB = []
	if rounds == -1:
		rounds = determine_rounds()
	for i in range(rounds):
		try:
			(roundA, roundB) = play_round(game, histA, histB, stratA, stratB)
			histA.append(roundA)
			# keep the player position in matching pennies game
			histB.append(roundB)
		except MoveException as e:
			e.round = i
			raise e
	return (histA, histB)

# function play_repeatedly
# Repeatedly plays the game and returns an array containing the history arrays 
#	from play_game.
# parameters: game(string), times(int), rounds(int), stratA(instance), stratB(instance)
# returns: array
#
def play_repeatedly(game, times, rounds, stratA, stratB):
	rhistory = []

        #create a new instance for each iteration
        new_stratA = stratA.__class__()
        del stratA
        stratA = new_stratA

        new_stratB = stratB.__class__()
        del stratB
        stratB = new_stratB

	for i in range(times):
		try:
			rhistory.append(play_game(game, rounds, stratA, stratB))
		except MoveException as e:
			e.iteration = i
			raise e
	return rhistory

# function play_tournament
# Plays a round robin tournement between all strategies.
# parameters: game(string), strategies(array), times(integer), rounds(integer)
# returns: dict (accessed like this: 
# 					tournement[stratA][stratB][iteration][round][player])
#
def play_tournament(game, strategies, times, rounds):
	# initialize result object
	res = {}
	for stratA in sorted(strategies.keys()):
		res[stratA] = {}

	# let's play
	for stratA in sorted(strategies.keys()):
		for stratB in sorted(strategies.keys()):
			if stratA == stratB:
				break
			try:
				rhistory = play_repeatedly(game, times, rounds, strategies[stratA], \
					strategies[stratB])
			except MoveException as e:
				e.strategy = stratA if e.player == 1 else stratB
				raise e
			hisA = []
			hisB = []
			for i in range(len(rhistory)):
				hisA.append(rhistory[i][0])
				hisB.append(rhistory[i][1])
			res[stratA][stratB] = hisA
			res[stratB][stratA] = hisB
	return res

# class MoveException
# An exception class holding the player information.
#
class MoveException(Exception):

	def __init__(self, player):
		self.player = player
		self.round = -1
		self.iteration = -1
		self.strategy = ""
		self.exception = None

	def __str__(self):
		if self.exception:
			return "Exception in code from " + self.strategy + " in round " + \
				str(self.round) + ": " + str(self.exception)
		else:
			return "Illegal move from " + self.strategy + " in round " + str(self.round)
