import numpy as np
from utils import calculate_value_function, calculate_Q_matrix


def solve_adv(num_states, num_actions, reward_function, transition_function, discount_factor, type_mdp):
    # Choose random Policy to begin the iteration
    num_iterations = 0
    S = int((num_states-1)/2)
    optimized = False
    policy = np.array([0] * num_states)  # Initialization
    mode = "normal"
    sp_ind = 0
    sp_c = 0
    while optimized is False:
        value_function = calculate_value_function(
            policy, num_states, num_actions, transition_function, reward_function, discount_factor)
        Q = calculate_Q_matrix(num_states, num_actions, reward_function,
                               transition_function, value_function, discount_factor, type_mdp)
        next_policy, improved_states,mode,sp_ind,sp_c = get_next_policy(policy.copy(), num_actions,mode,sp_ind,sp_c)
        print("Current:", policy, "Next: ", next_policy, "Mode:", mode)
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

        # if np.all(next_policy == num_actions-1):
        #     break
        # if num_iterations >= num_actions**(num_states/2):
            # break
    # Printing Final Answer
    for iter in range(num_states):
        print(str(np.asscalar(value_function[iter])) + " " + str(policy[iter]))

    print("Total Number of Iterations: "+str(num_iterations))


def get_next_policy(curr_policy, num_actions,mode,sp_ind,sp_c):
    improved_states = []
    num_states = len(curr_policy)
    if mode =="special":
        if sp_c ==0:
            index = sp_ind
            curr_policy[index] +=1
            improved_states.append(index)
            sp_c +=1
        elif sp_c ==sp_ind:    
            index = sp_ind-1
            curr_policy[index] +=1
            mode = "normal"
            sp_c = 0
        elif sp_c < (sp_ind)/2:
            index = sp_ind-2*sp_c
            curr_policy[index] = 0
            improved_states.append(index)
            sp_c +=1
        else: 
            index = int(2*(sp_c-(sp_ind+1)/2))
            curr_policy[index] = 0
            improved_states.append(index)
            sp_c +=1
        return curr_policy, improved_states, mode, sp_ind, sp_c
    elif mode == "normal":
        if curr_policy[0] == curr_policy[1]:
            curr_policy[1] += 1
            improved_states.append(1)
        else:
            curr_policy[0] += 1
            improved_states.append(0)
            if curr_policy[0] == num_actions-1:
                mode = "special"
                for sp_ind in range(num_states):
                    if curr_policy[sp_ind] != num_actions-1:
                        sp_ind+=1
                        break
        return curr_policy, improved_states,mode,sp_ind,0