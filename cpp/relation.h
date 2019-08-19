#ifndef RELATION_H
#define RELATION_H

#include <vector>
#include <fstream>
#include <string>

using namespace std;

namespace relation {
class RelationStats {
public:
	RelationStats(int N, int E): num_rel(N), num_edge(E) {
		count_rel.resize(N);
	}
	void Process(const string &file_name) {
		ProcessFile(file_name);
		ProcessResult();
	}
	
	vector<int> GetRelCount() {
		return count_rel;
	}

private:
	const int num_rel;
	const int num_edge;
	vector<int> count_rel;
	void ProcessFile(const string &file_name);
	void ProcessResult(){}
};
}

#endif