import numpy as np
from utils import calculate_value_function, calculate_Q_matrix


def solve_adv(num_states, num_actions, reward_function, transition_function, discount_factor, type_mdp):
    # Choose random Policy to begin the iteration
    num_iterations = 0
    S = int((num_states-1)/2)
    optimized = False
    policy = np.array([0] * num_states)  # Initialization
    while optimized is False:
        value_function = calculate_value_function(
            policy, num_states, num_actions, transition_function, reward_function, discount_factor)
        Q = calculate_Q_matrix(num_states, num_actions, reward_function,
                               transition_function, value_function, discount_factor, type_mdp)
        next_policy, improved_states = get_next_policy(policy.copy(), num_actions)
        print("Current:", policy, "Next: ", next_policy)
        check = (Q[improved_states, next_policy[improved_states]]
                 >= Q[improved_states, policy[improved_states]])
        print(Q[improved_states, policy[improved_states]])
        print(Q[improved_states, next_policy[improved_states]])

        print(check)
        if not np.all(check):
            break
        else:
            num_iterations = num_iterations+1
            policy = next_policy

        if num_iterations > 10:
            break
    #Printing Final Answer
    for iter in range(num_states):
        print(str(np.asscalar(value_function[iter])) + " " + str(policy[iter]))

    print("Total Number of Iterations: "+str(num_iterations))


def get_next_policy(curr_policy, num_actions):
    i = 0
    improved_states = []
    num_states = len(curr_policy)
    while True:
        if i >= num_states-1:
            break
        if curr_policy[i]+1 == num_actions:
            curr_policy[i] = 0
            curr_policy[i+1] = 0
            improved_states.append(i)
            improved_states.append(i+1)
            i += 2
        else:
            if curr_policy[i] == curr_policy[i+1]:
                curr_policy[i+1] += 1
                improved_states.append(i+1)
            else:
                curr_policy[i] += 1
                improved_states.append(i)
            break

    return curr_policy, improved_states
