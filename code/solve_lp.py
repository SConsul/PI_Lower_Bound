import sys
import numpy as np
import pulp

def solve_lp(num_states, num_actions, reward_function, transition_function, discount_factor, type_mdp):
	# Cite: http://benalexkeen.com/linear-programming-with-python-and-pulp-part-2/
	# Cite: http://benalexkeen.com/linear-programming-with-python-and-pulp-part-4/
	my_lp_problem = pulp.LpProblem("MDP Solver", pulp.LpMinimize)
	#Defining Variables
	V = []
	for iter in range(num_states):
		V.append("V{}".format(iter))
	val_function_dict = pulp.LpVariable.dicts("Value Function", ((i) for i in V), cat='Continuous')
	# Objective Function
	my_lp_problem += (
		pulp.lpSum([val_function_dict[(i)] for i in V])
		)
	# Constraints
	for iter_state, state_name in enumerate(V):
		for iter_action in range(num_actions):
			my_lp_problem += val_function_dict[(state_name)] >= pulp.lpSum([transition_function[num_actions*iter_state+iter_action][i]*(reward_function[num_actions*iter_state+iter_action][i] + discount_factor * val_function_dict[(i_name)])] for i, i_name in enumerate(V))
	if (discount_factor == 1):
		my_lp_problem += val_function_dict[(V[-1])] == 0
	# Solving LP
	my_lp_problem.solve()
	#print(pulp.LpStatus[my_lp_problem.status])
	optimal_value = []
	for var in val_function_dict:
		var_value = val_function_dict[var].varValue
		optimal_value.append(var_value)
		#print(var_value)
	# Finding optimal action
	optimal_action = []
	for iter_state in range(num_states):
		difference_vector = []
		for iter_action in range(num_actions):
			total_rhs = 0
			for iter_state_prime in range(num_states):
				total_rhs = total_rhs + transition_function[num_actions*iter_state+iter_action][iter_state_prime]*(reward_function[num_actions*iter_state+iter_action][iter_state_prime] + discount_factor * optimal_value[iter_state_prime])
			difference_vector.append(optimal_value[iter_state] - total_rhs)
		optimal_action.append(difference_vector.index(min(difference_vector)))
	# Printing Final Answer
	for iter in range(num_states):
		print(str(optimal_value[iter])+" "+str(optimal_action[iter]))


