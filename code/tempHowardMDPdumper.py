numStates = 11
numActions = 2

print(numStates)
print(numActions)
for i in range(numStates):
	for j in range(numActions):
		if j == 0:
			nextState = (i - 1) % numStates
		elif j == 1:
			nextState = (i + 1) % numStates
		else:
			print("DUNNO WHAT TO DO FOR ACTION", j)
		output = [0.0] * numStates
		output[nextState] = 1.0
		print('\t'.join([str(x) for x in output]))

for i in range(numStates):
	for j in range(numActions):
		print('\t'.join(['0'] * numStates))
