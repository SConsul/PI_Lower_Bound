import numpy as np
from main import *
def solve_rpi(num_states, num_actions, reward_function, transition_function, discount_factor, type_mdp):
	#Choose random Policy to begin the iteration
	num_iterations = 0
	S = int((num_states-2)/2)
	num_seeds = 50
	for rs in range(num_seeds):
		rng = np.random.RandomState(rs)
		optimized = False
		policy = [0] * num_states #Initialization
		while(optimized == False):
			value_function = calculate_value_function(policy, num_states, num_actions, transition_function, reward_function, discount_factor)
			Q_matrix = calculate_Q_matrix(num_states, num_actions, reward_function, transition_function, value_function, discount_factor, type_mdp)
			improvable_policy = []

			for it in range(num_states):
				col = np.squeeze(Q_matrix[it, :])
				
				ind = np.flatnonzero(col > col[policy[it]])
				# indE = np.flatnonzero(col == col[policy[it]])
				# indE = indE[indE<policy[it]]
				# ind = np.concatenate((indG,indE))
				if np.size(ind)>0:
					imp_action = rng.choice(ind)
				else:
					imp_action = policy[it]
				improvable_policy.append(imp_action)
					
			iter = num_states-1
			policy_improved = False
			next_policy = policy[:]
			while (iter>-1 and not policy_improved):
				if (improvable_policy[iter] != policy[iter]):
					next_policy[iter] = improvable_policy[iter]
					policy_improved = True
				iter = iter-1

			# vfcn = Reverse(value_function.reshape(-1).tolist())
			# vfcn_top = vfcn[0:S]
			# vfcn_top.append(vfcn[-1])
			# vfcn_bottom = vfcn[S:-1]
			# p = Reverse(policy)
			# p_top = p[0:S]
			# p_top.append(p[-1])
			# p_bottom = p[S:-1]
			# print("Current:", p_top, "Value function:", vfcn_top)
			# # print("        ", p_bottom, "               ", vfcn_bottom)
			if policy == next_policy:
			    optimized = True
			else:
			    num_iterations = num_iterations+1
			    policy = next_policy
		# for iter in range(num_states):
		# 	print(str(value_function[iter].item()) + " " + str(policy[iter]))
		# print(num_iterations)
	num_iterations = float(num_iterations)/float(num_seeds)
	print(str(int(S))+" States "+str(num_actions)+" Actions \t Total Number of Iterations: "+str(num_iterations))