#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <math.h>
#include <queue>

using namespace std;

int n, k, numStates;
vector<pair<int, int> > edgeOrder;
vector<vector<int> > firstNodeMap, secondNodeMap; // These store, for each state of the graph, a list of states that are 
// adjacent to the left (and right) node (in the underlying MDP) of the state in the graph

template <class T> void print(vector<T> & v) {for (int i = 0 ; i < v.size() ; i ++) cout<<v[i]<<' '; cout<<endl;}
template <class T> void print(vector<vector<T> > & vv) {for (int i = 0 ; i < vv.size() ; i ++) print(vv[i]);}

int getStateFromString(string s)
{
	// convert string (length n and base k) to state number
	int answer = 0, multiplier = 1;
	for (int i = s.size() - 1 ; i >= 0 ; i --)
	{
		answer += (s[i] - '0') * multiplier;
		multiplier *= k;
	}
	return answer;
}

void init()
{
	// create firstNodeMap and secondNodeMap
	int potentialFirstNode, potentialSecondNode;
	for (int i = 0 ; i < numStates ; i ++)
	{
		firstNodeMap.push_back(vector<int> (0));
		secondNodeMap.push_back(vector<int> (0));
		for (int j = 0 ; j < k ; j ++)
		{
			potentialFirstNode = (i + j * k) % numStates;
			if (potentialFirstNode != i) // not the current node
				firstNodeMap[firstNodeMap.size() - 1].push_back(potentialFirstNode);
			potentialSecondNode = (i / k)*k + j;
			if (potentialSecondNode != i) // not the current node
				secondNodeMap[secondNodeMap.size() - 1].push_back(potentialSecondNode);
		}
	}
}

void readEdgeOrder()
{
	// use n and k to open the correct file and read the edge order from there
	ifstream myfile;
  	myfile.open ("edges" + string(1, char((int('0') + n))) + "_" + string(1, char((int('0') + k))) + ".txt");
  	string current1, current2;
  	while (myfile >> current1 && myfile >> current2)
  	{
  		edgeOrder.push_back(make_pair<int, int> (getStateFromString(current1), getStateFromString(current2)));
  	}
  	myfile.close();
}

vector<vector<int> > getAllPossibilites(int nn, int kk)
{
	// generate a vector of vectors which stores a list of all possible n length base k strings
	vector<vector<int> > answer;
	long long int maxx = pow((long long int)kk, (long long int) nn);
	for (long long int i = 0 ; i < maxx ; i ++)
	{
		long long int current = i;
		vector<int> currentVector(nn);
		for (int ii = nn - 1 ; ii >= 0 ; ii --)
		{
			currentVector[ii] = current % kk;
			current /= kk;
		}
		answer.push_back(currentVector);
	}

	return answer;
}

vector<vector<bool> > convertToTransitionMatrix(vector<int> & edges)
{
	// using 0 / 1 to indicate the direction of edges create the transition matrix
	vector<vector<bool> > transitions(numStates, vector<bool>(numStates, false));
	for (int i = 0 ; i < edgeOrder.size() ; i ++)
	{
		if (edges[i] == 0)
			transitions[edgeOrder[i].first][edgeOrder[i].second] = true;
		else if (edges[i] == 1)
			transitions[edgeOrder[i].second][edgeOrder[i].first] = true;
		else
			cerr<<"somethign wrong with the edges vector recevied in convertToTransitionMatrix"<<endl;
	}
	return transitions;
}

bool dfs (vector<vector<bool> > & transitions, vector<int> & visited, int currentNode)
{
	// return true if cycle is found
	visited[currentNode] = 2;
	for (int i = 0 ; i < numStates ; i ++)
	{
		if (transitions[currentNode][i]) 
		{
			if (visited[i] == 2) return true;
			if (visited[i] == 0)
				if (dfs(transitions, visited, i))
					return true;
		}
	}
	visited[currentNode] = 1;
	return false;
}

bool isAcyclic(vector<vector<bool> > & transitions)
{
	// Depending on the transition matrix find if the graph is acyclic or not
	vector<int> visited(numStates, 0);
	int node;
	for (int i = 0 ; i < numStates ; i ++)
	{
		if (visited[i] == 0)
		{
			if (dfs(transitions, visited, i)) return false;
		}
	}
	return true;
}

bool outMapIsPermutation(vector<vector<bool> > & transitions)
{
	// Depending on the transition matrix find if the graph has all possible out maps or not
	vector<vector<bool> > outMapPresent(k, vector<bool> (k, false));
	int numFirst, numSecond;
	for (int i = 0 ; i < numStates ; i ++)
	{
		numFirst = 0; numSecond = 0;
		for (int j = 0 ; j < 2 ; j ++)
		{
			if (transitions[i][firstNodeMap[i][j]] == 1)
				numFirst ++;
			if (transitions[i][secondNodeMap[i][j]] == 1)
				numSecond ++;
		}
		if (outMapPresent[numFirst][numSecond]) return false;
		outMapPresent[numFirst][numSecond] = true;
	}
	return true;
}

int checkPath(vector<vector<bool> > & transitions, vector<int> & order)
{
	int count = 0;
	for (int i = 0 ; i < numStates - 1 ; i ++)
		if (transitions[order[i]][order[i + 1]])
			count ++;
		else
			return count;
	return count;
}

int findLongestPathRecursively(vector<vector<bool> > & transitions, vector<int> & orderSoFar, vector<bool> & used, int position)
{
	if (position == numStates) 
	{
		return checkPath(transitions, orderSoFar);
	}
	int currentBest = 0;
	for (int i = 0 ; i < numStates ; i ++)
	{
		if (! used[i])
		{
			used[i] = true;
			orderSoFar[position] = i;
			currentBest = max(currentBest, findLongestPathRecursively(transitions, orderSoFar, used, position + 1));
			orderSoFar[position] = -1;
			used[i] = false;
		}
	}
	return currentBest;
}

int findLongestPath(vector<vector<bool> > & transitions)
{
	// Find the length of the longest path in the graph
	vector<int> order(numStates, -1);
	vector<bool> used(numStates, false);
	return findLongestPathRecursively(transitions, order, used, 0);
}

int main(int argc, char * argv[])
{
	if (argc != 3)
	{
		cout<<"Usage ./a.out <n> <k>"<<endl;
		exit(1);
	}

	n = stoi(argv[1]);
	k = stoi(argv[2]);
	numStates = pow(k, n);

	init();
	readEdgeOrder();
	// for (int i = 0 ; i < numStates ; i ++)	{ cout<<i<<"->"; print(firstNodeMap[i]);}
	// for (int i = 0 ; i < numStates ; i ++)	{ cout<<i<<"->"; print(secondNodeMap[i]);}
	
	vector<vector<int> >allEdgeConfigurations = getAllPossibilites(edgeOrder.size(), 2);




	// vector<int> temp(allEdgeConfigurations[0].size(), 0);
	// temp[1] = 1;
	// vector<vector<bool> > t = convertToTransitionMatrix(temp);
	// cout<<findLongestPath(t)<<endl;



	// int numSelected = 0;
	// for (int i = 0 ; i < allEdgeConfigurations.size() ; i ++)
	// {
	// 	vector<vector<bool> > transitions = convertToTransitionMatrix(allEdgeConfigurations[i]);
	// 	bool temp = outMapIsPermutation(transitions) && isAcyclic(transitions);

	// 	if (temp) numSelected ++;
	// }
	// cout<<numSelected<<" "<<allEdgeConfigurations.size()<<endl;


	int longestPath = 0, count = 0;
	for (int i = 0 ; i < allEdgeConfigurations.size() ; i ++)
	{
		vector<vector<bool> > transitions = convertToTransitionMatrix(allEdgeConfigurations[i]);
		if (isAcyclic(transitions) && outMapIsPermutation(transitions))
		{
			count ++;
			int current = findLongestPath(transitions);
			cout<<i<<" "<<longestPath<<" "<<current<<endl;
			longestPath = max(longestPath, current);
		}
		if (i % 10000 == 1)
			cout<<i<<' '<<count<<' '<<longestPath<<endl;
	}

	return 0;
}