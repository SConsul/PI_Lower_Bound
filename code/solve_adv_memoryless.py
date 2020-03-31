import numpy as np
from utils import calculate_value_function, calculate_Q_matrix


def solve_adv(num_states, num_actions, reward_function, transition_function, discount_factor, type_mdp):
    # Choose random Policy to begin the iteration
    print("MEMORYLESS")
    num_iterations = 0
    S = int((num_states-1)/2)
    optimized = False
    policy = np.array([0] * num_states)  # Initialization    
    done_flag = False

    while optimized is False:
        value_function = calculate_value_function(
            policy, num_states, num_actions, transition_function, reward_function, discount_factor)
        Q = calculate_Q_matrix(num_states, num_actions, reward_function,
                               transition_function, value_function, discount_factor, type_mdp)
        improved_state,done_flag = get_next_IS(policy, num_actions,done_flag)
        if(done_flag is True):
            break
        # print('IS = ', improved_state)
        # print(Q[improved_state,:])
        for improving_action in range(num_actions):
            if Q[improved_state,improving_action] > Q[improved_state,policy[improved_state]]:
                break
        # print(improved_state,improving_action)
        next_policy = policy.copy()
        next_policy[improved_state] = improving_action
        # print("Current:",np.flip(policy[::2][:-1],axis=0))
        print("Current:", np.flip(policy[::2][:-1],axis=0)," | ",np.flip(policy[1::2],axis=0), "Next: ",np.flip(next_policy[::2][:-1],axis=0)," | ", np.flip(next_policy[1::2],axis=0))

        num_iterations = num_iterations+1
        policy = next_policy
    
        # if np.all(next_policy == num_actions-1):
        #     break
        # if num_iterations >= num_actions**(num_states/2):
            # break
    # Printing Final Answer
    for iter in range(num_states):
        print(str(np.asscalar(value_function[iter])) + " " + str(policy[iter]))

    print("Total Number of Iterations: ",num_iterations)


def get_next_IS(curr_policy, num_actions,done_flag):
    num_states = len(curr_policy)
    optimal_pol = (num_actions-1)*np.ones(len(curr_policy))
    optimal_pol[-1] = 0
    # print("Optimal Policy = ",optimal_pol)

    if np.all(curr_policy == optimal_pol):
        done_flag = True  
        return 0, True

    elif curr_policy[0]!= curr_policy[1]:
        return 0, False
    elif np.all(curr_policy[1::2] == curr_policy[::2][:-1]):
        if curr_policy[0] == (num_actions-1):
            for i in range(1,num_states,2):
                if curr_policy[i] != (num_actions-1):
                    return i, False
        else:
            return 1, False
                 
    else:
        if curr_policy[0]==0:
            for i in range(0,num_states-1,2):
                if curr_policy[i] != curr_policy[i+1]:
                    return i, False
        elif curr_policy[0]==num_actions-1:
            for i in range(1,num_states-1,2):
                if (curr_policy[i+1] != num_actions-1) or (curr_policy[i+2] == 0):
                    return i, False
        else:
            print('damn')
            return 1, False