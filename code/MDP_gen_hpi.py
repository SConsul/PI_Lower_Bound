import numpy as np

S = 11
A = 2
R = np.zeros((S, A, S))
T = np.zeros((S, A, S))

for i in range(S-1):
    T[i, 1, i+1] = 1
    T[i+1, 0, i] = 1
    R[i, 1, i+1] = 2**0

T[0, 0, S-1] = 1
T[S-1, 1, 0] = 1

R[10, 1, 0] = -2**28

R[1, 0, 0] = -2**8
R[2, 0, 1] = -2**6
R[3, 0, 2] = -2**3
R[4, 0, 3] = -2**1
R[5, 0, 4] = -2**4
R[6, 0, 5] = -2**2
R[7, 0, 6] = -2**5
R[8, 0, 7] = -2**7
R[9, 0, 8] = -2**9
R[10, 0, 9] = 2**0

R[0, 0, 10] = -2**1

gamma = 0.999
types = 'continuos'
dir_path = "../MDP_files/HPI"
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
file.write(types+'\n')
file.close()
