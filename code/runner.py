import os

for i in range(5, 7):
	print(str(i), 'states')
	for j in range(3, 11):
		os.system("python main.py ../MDP_files/SPI_new/" + str(j) + "_action_MDP/MDP_" + str(i) + "s_" + str(j) + "a_SPI.txt spi")