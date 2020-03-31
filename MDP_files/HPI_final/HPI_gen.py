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

		common_difference = np.zeros(S-1) #of the AP that the reward makes
		for it in range(S-1):
			common_difference[it] = (A-1)**it

		first_term = (A-1) - 0.5
		summation = (A-1) - 0.5
		recurrence = [first_term]
		for it in range(1, S-1):
			new_term = (A-1)**(it+1) - 0.5*(A-1)**it - summation
			summation = summation + new_term
			recurrence.append(new_term)

		for s in range(S-1):
			for a in range(1, A):
				#Forward
				R[s][a][s+1] = common_difference[s]*(A-1-a) #AP formula   first_term + (num_terms-1)*common_difference
				T[s][a][s+1] = 1.0
			#Backward
			R[s][0][(s-1)%S] = recurrence[s]
			T[s][0][(s-1)%S] = 1.0

		#R[0][0][2] = (A-1) - 0.5
		#T[0][0][2] = 1.0

		#R[1][0][0] = (A-1)**2
		#T[1][0][0] = 1.0

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