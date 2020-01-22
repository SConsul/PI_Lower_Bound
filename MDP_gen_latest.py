import numpy as np

n_actions = 4
n_states = 4
S = 2*n_states+2
A = n_actions
gamma = 1
types = "episodic"
R = np.zeros((S, A, S))
T = np.zeros((S, A, S))
n_sinks = 2
# n_states = int((S-n_sinks)/2)
#Order of States = [sinks, avg_states, max_states/actual_states]

#Define MDP
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

#Main states setting
# p = np.linspace(0, 1, n_actions)

# for s in range(n_states+2, S-1):
#     for a in range(2, n_actions):
#         sPrime = s-n_states+1
#         T[s][a][sPrime] = 1
#     a = 1
#     sPrime = min(s-n_states, n_states+1)
#     T[s][a][sPrime] = 1
#     if s > n_states+3:
#         T[s][0][s-2] = 1
#     print(T[s, :, :])
p = np.linspace(0, n_actions-1, n_actions)
p = -1*p
# p = reversed(p)
p = pow(2, p)
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
        # T[s][a][sPrime] += 1-p[n_actions-a]
    # a = 1
    # sPrime = min(s-n_states, n_states+1)
    # T[s][a][sPrime] = 1
    if s != n_states+2:
        T[s][0][s-1] = 1
# p = np.linspace(0, 1, n_actions)
# p = np.linspace(-1, 0, n_actions)
# p = -1*p
# for a in range(2, n_actions):
#     print('action=', a, ' p=', p[a-1])
#     T[S-1, a, n_states+1] = p[a-1]
#     T[S-1, a, S-2] = 1-p[a-1]

print(np.sum(T, axis=2))

for s in range(n_sinks, S):
    for a in range(A):
        R[s][a][0] = -1

# for s in range(n_states+3, S):
#     a=0
#     R[s][a][s-1] = -1

filename = "./MDP_{}s_{}a_new3.txt".format(n_states, n_actions)
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
