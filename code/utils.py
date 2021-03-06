import sys
import numpy as np
from tqdm import tqdm


def Reverse(lst):
    return [ele for ele in reversed(lst)]


def interpret_input_file(file_path):
    mdp = open(file_path, "r")
    num_states = int(mdp.readline())
    num_actions = int(mdp.readline())
    R = np.empty((num_states, num_actions, num_states))
    for s in range(num_states):
        for a in range(num_actions):
            vals = mdp.readline().strip().split('\t')
            val_list = [float(x.strip()) for x in vals]
            sa_val = np.array(val_list)
            R[s][a][:] = sa_val

    T = np.empty((num_states, num_actions, num_states))

    for s in range(num_states):
        for a in range(num_actions):
            vals = mdp.readline().strip().split('\t')
            val_list = [float(x.strip()) for x in vals]
            sa_val = np.array(val_list)
            T[s][a][:] = sa_val

    gamma = float(mdp.readline())
    type_mdp = mdp.readline().strip('\n')
    return num_states, num_actions, R, T, gamma, type_mdp


def calculate_value_function(policy, num_states, num_actions, transition_function, reward_function, discount_factor):

    coeff_matrix = np.zeros((num_states, num_states))
    rhs_vector = np.zeros((num_states, 1))
    value_function = np.zeros((num_states, 1))
    for row in range(num_states):
        rhs_val = 0
        for col in range(num_states):
            # LHS matrix
            if row == col:
                coeff_matrix[row][col] = 1 - discount_factor * \
                    transition_function[row][policy[row]][col]
            else:
                coeff_matrix[row][col] = -1*discount_factor * \
                    transition_function[row][policy[row]][col]
            # RHS Vector
            rhs_val = rhs_val + transition_function[row][policy[row]
                                                         ][col]*reward_function[row][policy[row]][col]
        rhs_vector[row] = rhs_val
    if discount_factor == 1.0:
        coeff_matrix_truncated = coeff_matrix[:-1, :-1]
        value_function[:-1] = np.matmul(np.linalg.inv(coeff_matrix_truncated), rhs_vector[:-1])
        value_function[-1] = 0
    else:
        value_function = np.matmul(np.linalg.inv(coeff_matrix), rhs_vector)

    return value_function


def calculate_Q_matrix(num_states, num_actions, reward_function, transition_function, value_function, discount_factor, type_mdp):
    Q_matrix = np.zeros((num_states, num_actions))
    for iter_state in range(num_states):
        for iter_action in range(num_actions):
            sum_val = 0
            for iter_state_prime in range(num_states):
                sum_val += transition_function[iter_state][iter_action][iter_state_prime]*(
                    reward_function[iter_state][iter_action][iter_state_prime] + discount_factor*value_function[iter_state_prime])
            Q_matrix[iter_state, iter_action] = sum_val
    return Q_matrix


def fromDecimal(base, inputNum):

    index = 0  # Initialize index of result
    res = []
    # Convert input number is given base
    # by repeatedly dividing it by base
    # and taking remainder
    while (inputNum > 0):
        res.append(inputNum % base)
        inputNum = int(inputNum / base)
    return res[::-1]


def makefulllist(num_states, num_actions):
    all_policy = []
    for iter in tqdm(range(num_actions**num_states)):
        curr_policy = fromDecimal(num_actions, iter)
        curr_policy = (num_states-len(curr_policy))*[0] + curr_policy
        all_policy.append(curr_policy)
    return all_policy


def find_max_iterations(num_states, num_actions, reward_function, transition_function, discount_factor, type_mdp):
    '''
    For finding the initial state so that the number of iterations in SPI is maximum
    '''
    all_policy = makefulllist(num_states, num_actions)
    max_iter = 0
    for iter in tqdm(range(len(all_policy))):
        num_iterations = solve_spi_with_initial_policy(
            num_states, num_actions, all_policy[iter], reward_function, transition_function, discount_factor, type_mdp)
        if (num_iterations > max_iter):
            max_iter = num_iterations
            max_iter_policy = all_policy[iter]
    print("Max number of iterations: ", max_iter)
    print("Corresponding Starting State: ", max_iter_policy)
