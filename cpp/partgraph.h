#ifndef PARTGRAPH_H
#define PARTGRAPH_H
#include "partmap.h"
#include <unordered_map>

namespace part {
class PartGraph {
	struct Edge {
		Edge(int rel, int dst): rel_id(rel), dst_id(dst) {

		}
		int rel_id;
		int dst_id;
	};
	struct Node {
		Node() {

		}
		Node(int id_): id(id_) {

		}
		void Add(int rel, int dst) {
			Edge edge(rel, dst);
			edges.push_back(edge);
		}
		int id;
		vector<Edge> edges; 
	};
public:
	PartGraph(int N, int P, const string &part_file_name): num_node(N), num_part(P), partmap(N, P, part_file_name) {
		subgraphs.resize(P);
	}
	void Process(const string &data_file_name);
	void Output(int p, const string &file_name, int *N, int *E);

private:
	const int num_node;
	const int num_part;
	PartMap partmap;
	vector<unordered_map<int, Node>> subgraphs;
	vector<Node> Reorder(int p, int *N);
};
}
#endif