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
		save_figure("plots/"+game + "-" + stratA + "-" + stratB + "-" + str(iteration_print) + ".pdf")
		reset_figure(game)
	return True

#plots average payoffs and total payoffs for all strategy combinations
def plot_all(game, path, history):
        path_pr = path + game + "/per_round/"
        path_total = path + game + "/total/"

        
        count = 1
        for i in history.keys():
                for j in history[i].keys():
                        iterations = len(history[i][j])

                        payoff_hist_A = [] 
                        payoff_hist_B = [] 
                        payoff_total_A = [] 
                        payoff_total_B = [] 

                        rounds = len(history[i][j][0])

                        for n in range(rounds):
                                payoff_hist_A.append(0) 
                                payoff_hist_B.append(0) 
                                payoff_total_A.append(0) 
                                payoff_total_B.append(0) 

                        for k in range(iterations):
                                this_iter = ga.make_payoff_history(game, history[i][j][k])
                                
                                total_A = 0
                                total_B = 0
                                for n in range(rounds):
                                        payoff_hist_A[n] = payoff_hist_A[n] + this_iter[n][0]/float(iterations) 
                        #payoff_hist_A[n], averaged payoffs for round[n] over all iterations for for A
                                        payoff_hist_B[n] = payoff_hist_B[n] + this_iter[n][1]/float(iterations) 

                                        total_A += this_iter[n][0]/float(iterations)
                                        total_B += this_iter[n][1]/float(iterations)
                                        payoff_total_A[n] += total_A
                                        payoff_total_B[n] += total_B

                        #plot average
                        plt.figure(count)
                        plotname = path_pr+i+"_vs_"+j+".pdf"
                        title = "Average Payoff: "+i+" vs "+j
                        plt.plot(range(rounds),payoff_hist_A,label=i)
                        plt.plot(range(rounds),payoff_hist_B,label=j)
                        plt.legend(loc="upper left")
                        plt.title(title)
                        plt.axis([0,rounds,-1,4])
                        plt.savefig(plotname)
                        count += 1

                        #plot total
                        plt.figure(count)
                        plotname = path_total+i+"_vs_"+j+".pdf"
                        title = "Total Payoff: "+i+" vs "+j
                        plt.plot(range(rounds),payoff_total_A,label=i)
                        plt.plot(range(rounds),payoff_total_B,label=j)
                        plt.legend(loc="upper left")
                        plt.title(title)
                        plt.axis([0,rounds,-1,max(payoff_total_A[-1],payoff_total_B[-1])])
                        plt.savefig(plotname)
                        count += 1

                        



#        analysis = ga.prep_for_analysis(game, "allA", history)
#        (po_history, po_stepsums, po_iter_sums, po_iter_avgs, avg_of_sums, avg_of_avgs) 

        if not os.path.exists(path_pr):
                os.makedirs(path_pr)

        if not os.path.exists(path_total):
                os.makedirs(path_total)
                
