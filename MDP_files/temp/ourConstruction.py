import numpy as np
import sys

if len(sys.argv) != 3:
	print("Usage python tempHowardMDPdumper.py <numStates> <numActions>")
numStates = int(sys.argv[1])
numActions = int(sys.argv[2])
infinity = 50000000
k = numActions - 1

actionZeroRewards = []
for i in range(numStates - 3):
	actionZeroRewards.append( k ** (i + 1) - (k ** i) / 2.0 - sum(actionZeroRewards))
actionZeroRewards += [k ** (numStates - 2), infinity, 0]
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
			elif i < numStates - 2:
				printRewards[i][j][nextState] = (k - j) * (k ** i)

		output = [0.0] * numStates
		output[nextState] = 1.0
		print('\t'.join([str(x) for x in output]))

printRewards[numStates - 1, 0, 0] = 28

for i in range(numStates):
	for j in range(numActions):
		print('\t'.join(list([str(x) for x in printRewards[i, j]])))
