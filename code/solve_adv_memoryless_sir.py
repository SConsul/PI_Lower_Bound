import numpy as np
import math
from utils import calculate_value_function, calculate_Q_matrix


def solve_adv(num_states, num_actions, reward_function, transition_function, discount_factor, type_mdp):
    # Choose random Policy to begin the iteration
    print("MEMORYLESS_SIR")
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
        num_iterations = num_iterations+1
        pol_x = np.array(next_policy[::2][:-1])
        pol_y = np.array(next_policy[1::2])
        S = pol_x.size
        pow_arr = np.geomspace(1,num_actions**(S-1),S)
        x = np.dot(pow_arr,pol_x)
        y = np.dot(pow_arr,pol_y)
        # print("Time",num_iterations,"Current:", np.flip(policy[::2][:-1],axis=0)," | ",np.flip(policy[1::2],axis=0), "Next: ",np.flip(next_policy[::2][:-1],axis=0)," | ", np.flip(next_policy[1::2],axis=0))
        
        # print("Time",num_iterations,np.flip(next_policy[::2][:-1],axis=0)," | ", np.flip(next_policy[1::2],axis=0),"x=",x,"y=",y)
        print("Time",num_iterations,next_policy,"x=",x,"y=",y)
        
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
    pol_x = np.array(curr_policy[::2][:-1])
    pol_y = np.array(curr_policy[1::2])
    S = pol_x.size
    pow_arr = np.geomspace(1,num_actions**(S-1),S)
    x = np.dot(pow_arr,pol_x)
    y = np.dot(pow_arr,pol_y)

    if np.all(curr_policy == optimal_pol):
        done_flag = True  
        return 0, True
    else:
        d = y-x
        if d==0:
            print('t1')
            for i in range(S):
                if pol_x[i] != num_actions-1:
                    break
            return 2*i+1, False
        else:
            L = math.floor(round(math.log(d,num_actions),8))
        if d==1:
            print('t2')
            return 0, False
        elif pol_y[0]==num_actions-1:
            print('t3')
            print(L)
            return int(2*L-1), False
        else:
            print('t4')
            return int(2*L), False
