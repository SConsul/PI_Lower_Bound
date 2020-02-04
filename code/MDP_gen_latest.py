import numpy as np
import os

gamma = 1
types = "episodic"
n_sinks = 2
top_dir_path = "../MDP_files"
if not os.path.isdir(top_dir_path):
    os.mkdir(top_dir_path)
top_dir_path = top_dir_path+"/SPI_new"

if not os.path.isdir(top_dir_path):
    os.mkdir(top_dir_path)

for n_actions in range(2, 11):
    dir_path = top_dir_path + "/{}_action_MDP".format(n_actions)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    for n_states in range(2, 11):
        # Define Parameters of MDP
        # n_actions = 4
        # n_states = 4
        S = 2*n_states+2
        A = n_actions
        R = np.zeros((S, A, S))
        T = np.zeros((S, A, S))

        # Define MDP
        # Defining Average states
        for s in range(n_sinks):
            for a in range(A):
                T[s][a][s] = 1

        for a in range(A):
            T[2][a][1] = 1
            T[3][a][0] = 0.5
            T[3][a][2] = 0.5

        for s in range(n_sinks+2, n_sinks+n_states):
            for a in range(A):
                T[s][a][s-1] = 0.5
                T[s][a][s+n_states-2] = 0.5

        # Main states setting
        p = np.linspace(0, n_actions-1, n_actions)
        p[1:]+=1 # So that probabilities for action > 1 start from 1/4
        p = -1*p
        p = pow(2, p)  # Geometric probabilities
        T[n_states+2][0][0] = 1
        for a in range(1, n_actions):
            print('action=', a, ' p=', p[a-1])
            T[n_states+2][a][2] = p[a-1]
            T[n_states+2][a][0] = 1-p[a-1]

        for s in range(n_states+3, S):
            for a in range(1, n_actions):
                sPrime = min(n_states+1, s-n_states)
                T[s][a][sPrime] = p[a-1]
                sPrime = s-1
                T[s][a][sPrime] = 1-p[a-1]
            if s != n_states+2:
                T[s][0][s-1] = 1

        print(np.sum(T, axis=2))
        assert np.all(np.sum(T, axis=2) == np.ones((S, A)))

        for s in range(n_sinks, S):
            for a in range(A):
                R[s][a][0] = -1

        # Generate MDP file

        filename = dir_path+"/MDP_{}s_{}a_SPI.txt".format(n_states, n_actions)
        print("generating "+filename)
        file = open(filename, "w")

        file.write(str(S)+'\n')
        file.write(str(A)+'\n')

        for s in range(0, S):
            for a in range(0, A):
                for sPrime in range(0, S):
                    file.write(str(R[s][a][sPrime]) + "\t")

                file.write("\n")

        for s in range(0, S):
            for a in range(0, A):
                for sPrime in range(0, S):
                    file.write(str(T[s][a][sPrime]) + "\t")

                file.write("\n")

        file.write(str(gamma)+'\n')
        file.write(types+'\n')
        file.close()
