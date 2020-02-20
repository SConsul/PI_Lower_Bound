import numpy as np
import sys

if len(sys.argv) != 2:
	print("Usage python tempHowardMDPdumper.py <numActions>")
numStates = 4
numActions = int(sys.argv[1])
infinity = 5000

actionZeroRewards = [numActions - 1.5, numActions ** 2, infinity, 0]
printRewards = np.zeros((numStates, numActions, numStates))
print(numStates)
print(numActions)
for i in range(numStates):
	for j in range(numActions):
		if j == 0:
			nextState = (i - 1) % numStates
			printRewards[i][j][nextState] = actionZeroRewards[i]
		else:
			nextState = (i + 1) % numStates
			if i == numStates - 1: 
				printRewards[i][j][nextState] = infinity
			if i == numStates - 2 and j > 1:
				printRewards[i][j][nextState] = infinity
			if i == 0:
				printRewards[i][j][nextState] = numActions - 1 - j
			if i == 1:
				printRewards[i][j][nextState] = (numActions - 1 - j) * numActions

		output = [0.0] * numStates
		output[nextState] = 1.0
		print('\t'.join([str(x) for x in output]))

printRewards[numStates - 1, 0, 0] = 28

for i in range(numStates):
	for j in range(numActions):
		print('\t'.join(list([str(x) for x in printRewards[i, j]])))
