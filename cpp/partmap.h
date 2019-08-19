#ifndef PARTMAP_H
#define PARTMAP_H
#include <vector>
#include <string>
#include <fstream>
#include <iostream>

using namespace std;

namespace part {
class PartMap {
public:
	PartMap(int N, int P, const string &file_name): num_node(N), num_part(P) {
		node2part.resize(N);
		ProcessFile(file_name);
	}
	int GetPart(int node) {
		return node2part[node];
	}
private:
	const int num_node;
	const int num_part;
	vector<int> node2part; 
	void ProcessFile(const string &file_name) {
		ifstream file;
		file.open(file_name);
		int partition;
		for (int i = 0; i < num_node; i++) {
			file >> partition;
			node2part[i] = partition;
		}
		file.close();
		cout << "Finish partmap" << endl;
	}
};
}
#endif