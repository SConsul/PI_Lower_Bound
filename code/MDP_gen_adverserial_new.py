import numpy as np
import os

gamma = 1
types = "episodic"
top_dir_path = "../MDP_files"
max_actions = 4
min_actions = 3
max_states = 5
min_states = 4
if not os.path.isdir(top_dir_path):
    os.mkdir(top_dir_path)

top_dir_path = os.path.join(top_dir_path, "PI_adv")
if not os.path.isdir(top_dir_path):
    os.mkdir(top_dir_path)

for n_actions in range(min_actions, max_actions):
    dir_path = os.path.join(top_dir_path, "{}_action_MDP".format(n_actions))
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    for n_states in range(min_states, max_states):
        # Define Parameters of MDP
        S = 2*n_states
        A = n_actions
        R = np.zeros((S, A, S))
        T = np.zeros((S, A, S))

        # Define MDP
        # Defining last state as sink state
        for a in range(A):
            T[S-1][a][S-1] = 1

        for s in range(0, S-2, 2):
            for a in range(A):
                if a == 0:
                    T[s][a][s+3] = 1
                    R[s][a][s+3] = 0
                else:
                    T[s][a][s+2] = 1
                    R[s][a][s+2] = ((s/2)*(n_actions-1)+1)*a

        for s in range(1, S-1, 2):
            for a in range(A):
                if a == 0:
                    T[s][a][s+2] = 1
                    R[s][a][s+2] = 0
                else:
                    T[s][a][s+1] = 1
                    R[s][a][s+1] = (((s-1)/2)*(n_actions-1)+1)*a

        # Generate MDP file
        filename = os.path.join(dir_path, "MDP_{}s_{}a_adv.txt".format(n_states, n_actions))
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
