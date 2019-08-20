#ifndef PARTPAIR_H
#define PARTPAIR_H
#include "partmap.h"
#include <map>

namespace part {
class PartPair {
public:
	PartPair(int N, int P, const string &part_file_name): num_node(N), num_part(P), partmap(N, P, part_file_name) {
		
	}
	void Process(const string &data_file_name);
	void OutputPair(vector<pair<int, int>> pairs, const string &file_name);

private:
	const int num_node;
	const int num_part;
	PartMap partmap;
	// vector<unordered_map<int, int>> id_map;
	map<pair<int, int>, vector<vector<int>>> edges;
};
}
#endif