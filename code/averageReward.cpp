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
int min(int a, int b){if (a < b) return a; return b;}

struct Q {
	float value, potential;

	bool operator >(const Q & rhs) {
		return (value < rhs.value) || ( abs(value - rhs.value) < epsilon && potential < rhs.potential);
	}
};

void computeValues(float * policyRewards, int * policy, Q * v)
{
	// Identify the cycles
	int visited[numStates];
	for (int i = 0 ; i < numStates ; i ++) visited[i] = -1;
	vector<int> startNodes(0);
	int numHeadsSoFar = 0;
	for (int startNode = 0 ; startNode < numStates ; startNode ++)
	{
		if (visited[startNode] > -1) continue;
		int nextNode = policy[startNode], currentNode = startNode;
		while (visited[currentNode] == -1)
		{
			visited[currentNode] = numHeadsSoFar;
			if (visited[nextNode] == numHeadsSoFar) {startNodes.push_back(nextNode);}
			int temp = policy[nextNode];
			currentNode = nextNode;
			nextNode = temp;
		}
		numHeadsSoFar ++;
	}

	// Identify the heads of the cycles
	int heads[numStates];
	float headValues[numStates];
	for (int i = 0 ; i < numStates ; i ++) heads[i] = -1;
	for (int i = 0 ; i < startNodes.size() ; i ++)
	{
		// Identify head
		int nextNode = policy[startNodes[i]];
		int currentHead = startNodes[i];
		while (nextNode != startNodes[i])
		{
			currentHead = min(nextNode, currentHead);
			nextNode = policy[nextNode];
		}
		
		// Store value for every element of cycle
		nextNode = policy[startNodes[i]];
		int length = 1;
		float totalReward = policyRewards[startNodes[i]];
		heads[startNodes[i]] = currentHead;
		while (nextNode != startNodes[i])
		{
			heads[nextNode] = currentHead;
			length ++;
			totalReward += policyRewards[nextNode];
			nextNode = policy[nextNode];
		}
		headValues[currentHead] = totalReward / ((float) length);
	}

	// Compute the values and potentials - CAN BE MADE MORE EFFICIENT 0(n^2) -> O(n)
	for (int node = 0 ; node < numStates ; node ++)
	{
		int currentNode = node;
		int length = 0;
		float rewards = 0.0;
		while (heads[currentNode] != currentNode)
		{
			length ++;
			rewards += policyRewards[currentNode];
			currentNode = policy[currentNode];
		}
		// At this point, currentNode is the head. length has length of path to head. rewards has reward along this path
		v[node].value = headValues[currentNode];
		v[node].potential = rewards - length * v[node].value;
	}
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
			for (int k = 0 ; k < numStates ; k ++)
				file >> transitions[i][j][k];
	for (int i = 0 ; i < numStates ; i ++)
		for (int j = 0 ; j < numActions ; j ++)
			for (int k = 0 ; k < numStates ; k ++)
				file >> rewards[i][j][k];
	file.close();
	// Since this is a deterministic MDP, construct the nextState table directly
	vector<vector<int> > nextStates(numStates, vector<int>(numActions, -1));
	for (int i = 0 ; i < numStates ; i ++)
		for (int j = 0 ; j < numActions ; j ++)
			for (int k = 0 ; k < numStates ; k ++)
				if (transitions[i][j][k] > 0.99)
					nextStates[i][j] = k;
	//////////////////////////////////////////////////////////////////////////////////////////////////////


	///////////////////////////////////////////// SOVLER LOOP /////////////////////////////////////////////
	// Initialize the start policy
	int rawPolicy[numStates];
	for (int i = 0 ; i < numStates - 1 ; i ++) rawPolicy[i] = 0;
	rawPolicy[numStates - 1] = 1;

	Q q[numStates][numActions];
	bool improvable = true;
	int iterations = 0;
	Q v[numStates];
	while (improvable)
	{
		iterations ++;
		// Compute and store the next states in the policy and their rewards
		int policy[numStates];
		float policyRewards[numStates];
		for (int i = 0 ; i < numStates ; i ++)
		{
			int action = rawPolicy[i];
			int nextState = nextStates[i][action];
			policy[i] = nextState;
			policyRewards[i] = rewards[i][action][nextState];
		}

		// Find the cycles and compute the V values
		computeValues(policyRewards, policy, v);

		// Compute the Q values
		for (int currentState = 0 ; currentState < numStates ; currentState ++)
			for (int currentAction = 0 ; currentAction < numActions ; currentAction ++)
			{
				int nextState = nextStates[currentState][currentAction];
				q[currentState][currentAction].value = v[nextState].value - v[currentState].value;
				q[currentState][currentAction].potential = rewards[currentState][currentAction][nextState] - v[currentState].value + 
																v[nextState].potential - v[currentState].potential;
			}
		
		// Find all the better actions
		improvable = false;
		int newRawPolicy[numStates];
		for (int i = 0 ; i < numStates ; i ++) newRawPolicy[i] = rawPolicy[i];
		for (int currentState = 0 ; currentState < numStates ; currentState ++)
		{
			for (int action = 0 ; action < numActions ; action ++)
			{
				if (q[currentState][action] > q[currentState][newRawPolicy[currentState]])
				{
					improvable = true;
					newRawPolicy[currentState] = action;
				}
			}
		}
		for(int i = 0 ; i < numStates ; i ++)
			rawPolicy[i] = newRawPolicy[i];

		// Print relevant details
		cout<<"Iteration "<<iterations<<": ";
		for (int i = 0 ; i < numStates ; i ++)
			cout<<rawPolicy[i]<<" ";
		cout<<endl;
	}
	//////////////////////////////////////////////////////////////////////////////////////////////////////


	return 0;
}