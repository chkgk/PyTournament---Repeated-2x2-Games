import game_analyser as ga
import matplotlib.pyplot as plt
import os


def prepare_figure(game):
	plt.figure(figsize=(8,6), dpi=80)
	plt.xlabel("round")
	plt.ylabel("payoff")
	plt.grid(True)
	return True

def reset_figure(game):
	plt.close()
	return prepare_figure(game)

def save_figure(filename):
	plt.savefig(filename)
	return True

def show_figure():
	plt.show()
	return True

# function plot_game
#
# accepts a prepared tupel(stratA, stratB, step_sum_stratA, step_sum_stratB)
# draws both graphs into a single diagram. stratA is color coded in red, stratB in blue
#
def plot_game(game, stratA, stratB, iteration, histories):
	if iteration == -2: 
		iteration +=1 
	strat_tupel = ga.prep_for_plot(game, stratA, stratB, iteration, histories)
	plt.plot(strat_tupel[2], color="red", label=strat_tupel[0])
	plt.plot(strat_tupel[3], color="blue", label=strat_tupel[1])
	plt.legend(loc="upper left")
	
	iteration += 1 # make sure correct iteration number is printed on the figure.
	if iteration == 0:
		iteration = "last"

	plt.title("Game: "+game+" - Iteration: "+str(iteration))
	return True

def plot_multi(game, stratA, strategies, iteration, histories):
	reset_figure(game)
	if iteration == -2: 
		iteration +=1 
	for stratB in strategies:
		iteration_print = iteration 
		strat_tupel = ga.prep_for_plot(game, stratA, stratB, iteration, histories)
		plt.plot(strat_tupel[2], color="red", label=strat_tupel[0])
		plt.plot(strat_tupel[3], color="blue", label=strat_tupel[1])
		plt.legend(loc="upper left")
		
		iteration_print = iteration + 1 # make sure correct iteration number is printed on the figure.
		if iteration_print == 0:
			iteration_print = "last"

		plt.title("Game: "+game+" - Iteration: "+str(iteration_print))
		if not os.path.exists("plots"):
			os.makedirs("plots")
		save_figure("plots/"+game + "-" + stratA + "-" + stratB + "-" + str(iteration_print) + ".png")
		reset_figure(game)
	return True