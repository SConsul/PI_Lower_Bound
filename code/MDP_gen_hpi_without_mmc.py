import numpy as np
import os

gamma = 1
types = "episodic"
top_dir_path = "../MDP_files"
if not os.path.isdir(top_dir_path):
    os.mkdir(top_dir_path)
top_dir_path = top_dir_path+"/HPI_without_mmc"

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
        S = n_states+2
        A = n_actions
        R = np.zeros((S, A, S))
        T = np.zeros((S, A, S))

        # Define MDP
        # Defining Average states