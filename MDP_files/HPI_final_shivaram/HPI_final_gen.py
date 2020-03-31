S = 3
A = 7
gamma = 1
typ = "episodic"

import numpy as np
import os


for A in range(3, 11):
	dir_path = "{}_action_MDP".format(A)
	if not os.path.isdir(dir_path):
		os.mkdir(dir_path)
	for S in range(3, 11):
		R = np.zeros((S, A, S))
		T = np.zeros((S, A, S))		

		for s in range(S-1):
			for a in range(A-1):
				if s != S-2:
					#North
					R[s][a][S-1] = -2**s
					seq = np.linspace(0.55, 1.0, num=A-1)[::-1]
					T[s][a][S-1] = seq[a] #between 0.5 and 1
					T[s][a][s+1] = 1-seq[a]
				else:
					#Just the state before terminal needs special treatment
					seq = np.linspace(0.55, 1.0, num=A-1)[::-1]
					R[s][a][S-1] = (-2**s)*seq[a]
					T[s][a][S-1] = 1.0
			#East
			T[s][A-1][s+1] = 1.0

		#Sink state definition
		for a in range(A):
			T[S-1][a][S-1] = 1


		filename = dir_path+"/MDP_{}s_{}a_SPI.txt".format(S, A)
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
		file.write(typ+'\n')
		file.close()