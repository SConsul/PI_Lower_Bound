#include<iostream>
#include<stdlib.h>
#include<vector>
#include<fstream>
#include<string>

using namespace std;

int numStates, numActions;
float epsilon = 1e-10;
float abs(float x){
	if (x > 0) return x;
	return - x;
}

struct Q {
	float value, potential;

	bool operator >(const Q & rhs) {
		return (value < rhs.value) || ( abs(value - rhs.value) < epsilon && potential < rhs.potential);
	}
};

void computeValues(vector<vector<vector<float> > > & transitions, vector<vector<vector<float> > > & rewards, int * policy, Q * v)
{
	// Identify the cycles
	bool visited[numStates];
	for (int i = 0 ; i < numStates ; i ++) visited[i] = false;
	vector<int> startNodes(0);
	for (int startNode = 0 ; startNode < numStates ; startNode ++)
	{
		if (visited[startNode]) continue;
		int nextNode = policy[startNode], currentNode = startNode;
		while (! visited[currentNode])
		{
			visited[currentNode] = true;
			if (nextNode == startNode) {startNodes.push_back(startNode);}
			int temp = policy[nextNode];
			currentNode = nextNode;
			nextNode = temp;
		}
	}
	for (int i = 0 ; i < startNodes.size() ; i ++ )cout<<startNodes[i]<<endl;

	// Identify the heads of the cycles
	int heads[numStates];

	// Compute the values and potentials
}

int main(int argc, char * argv[])
{
	if (argc != 2)
	{
		cout<<"Usage: ./a.out <path/to/mdp/file>"<<endl;
		exit(1);
	}
	///////////////////////////////////////////// READ DATA /////////////////////////////////////////////
	ifstream file(argv[1]);
	file >> numStates;
	file >> numActions;
	vector<vector<vector<float> > > rewards(numStates, vector<vector<float> >(numActions, vector<float> (numStates, 0)));
	vector<vector<vector<float> > > transitions(numStates, vector<vector<float> >(numActions, vector<float> (numStates, 0)));
	for (int i = 0 ; i < numStates ; i ++)
		for (int j = 0 ; j < numActions ; j ++)
			for (int k = 0 ; k < numActions ; k ++)
				file >> rewards[i][j][k];
	for (int i = 0 ; i < numStates ; i ++)
		for (int j = 0 ; j < numActions ; j ++)
			for (int k = 0 ; k < numActions ; k ++)
				file >> rewards[i][j][k];
	float gamma;
	file >> gamma;
	file.close();
	//////////////////////////////////////////////////////////////////////////////////////////////////////


	///////////////////////////////////////////// SOVLER LOOP /////////////////////////////////////////////
	int policy[numStates];
	Q q[numStates][numActions];
	bool improvable = true;
	int iterations = 0;
	Q v[numStates];
	while (improvable)
	{
		// Find the cycles and compute the V values
		computeValues(transitions, rewards, policy, v);

		// Compute the Q values
		
		// Find all the better actions
		improvable = false;

		// Print relevant details
	}
	//////////////////////////////////////////////////////////////////////////////////////////////////////


	return 0;
}