import numpy as np
from utils import calculate_value_function, calculate_Q_matrix, Reverse


def solve_hpi(num_states, num_actions, reward_function, transition_function, discount_factor, type_mdp):
    #Choose random Policy to begin the iteration
    num_iterations = 0
    optimized = False
    policy = [0] * num_states  # Initialization
    while(optimized == False):
        value_function = calculate_value_function(
            policy, num_states, num_actions, transition_function, reward_function, discount_factor)
        Q_matrix = calculate_Q_matrix(num_states, num_actions, reward_function,
                                      transition_function, value_function, discount_factor, type_mdp)
        next_policy = []
        improvables = []
        for it in range(num_states):
            col = np.squeeze(Q_matrix[it, :])
            if sum(col > col[policy[it]])>0:
                imp_action = np.flatnonzero(col > col[policy[it]])[0]
                improvables.append(True)
            else:
                imp_action = policy[it]
                improvables.append(False)
            next_policy.append(imp_action)
        
        print("Current:", policy, "Next: ", next_policy, "Improvables: ", improvables)
        if policy == next_policy:
            optimized = True
        else:
            num_iterations = num_iterations+1
            policy = next_policy
    #Printing Final Answer
    for iter in range(num_states):
        print(str(np.asscalar(value_function[iter])) + " " + str(policy[iter]))
    print("Total Number of Iterations: "+str(num_iterations))
