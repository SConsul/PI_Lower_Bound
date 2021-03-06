import numpy as np
import sys

if len(sys.argv) != 2:
	print("Usage python tempHowardMDPdumper.py <numActions>")
numStates = 4
numActions = int(sys.argv[1])

rewards = [1, 8, 6, 3, 1, 4, 2, 5, 7, 9, 0]
printRewards = np.zeros((numStates, numActions, numStates))
print(numStates)
print(numActions)
for i in range(numStates):
	for j in range(numActions):
		if j == 0:
			nextState = (i + 1) % numStates
		elif j == 1:
			nextState = (i - 1) % numStates
			printRewards[i][j][nextState] = rewards[i]
		else:
			nextState = (i + 1) % numStates
			printRewards[i][j][nextState] = rewards[i] * (float(j)/numActions)
		output = [0.0] * numStates
		output[nextState] = 1.0
		print('\t'.join([str(x) for x in output]))

printRewards[numStates - 1, 0, 0] = 28

for i in range(numStates):
	for j in range(numActions):
		print('\t'.join(list([str(x) for x in printRewards[i, j]])))
