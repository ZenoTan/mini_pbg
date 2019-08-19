#include "partgraph.h"

namespace part {
	void PartGraph::Process(const string &data_file_name) {
		ifstream file;
		file.open(data_file_name);
		int src, dst, rel, src_part, dst_part;
		string first_line;
		file >> first_line;
		for (int i = 0; i < num_node; i++) {
			// if (i % 10000 == 0) {
			// 	cout << i << endl;
			// }
			file >> src;
			file >> dst;
			file >> rel;
			src_part = partmap.GetPart(src);
			dst_part = partmap.GetPart(dst);
			if (subgraphs[src_part].find(src) == subgraphs[src_part].end()) {
				subgraphs[src_part][src] = Node(src);
			}
			if (subgraphs[dst_part].find(dst) == subgraphs[dst_part].end()) {
				subgraphs[dst_part][dst] = Node(dst);
			}
			if (src_part == dst_part) {
				subgraphs[src_part][src].Add(rel, dst);
			}
		}
		int sum = 0;
		for (int i = 0; i < num_part; i++) {
			sum += subgraphs[i].size();
		}
		cout << "Size: " << sum << endl;
		file.close();
	}
	void PartGraph::Output(int p, const string &file_name, int *N, int *E) {
		vector<Node> vec_node = Reorder(p, N);
		//*N = vec_node.size();
		ofstream file;
		file.open(file_name);
		int num_edge = 0;
		for (auto &node: vec_node) {
			int id = node.id;
			for (auto &edge: node.edges) {
				file << id << ' ';
				file << edge.dst_id << ' ';
				file << edge.rel_id << endl;
				num_edge++;
			}
			
		}
		*E = num_edge;
		file.close();
	}
	vector<PartGraph::Node> PartGraph::Reorder(int p, int *N) {
		unordered_map<int, int> id_map;
		int seq_id = 0;
		for (auto &kv: subgraphs[p]) {
			if (id_map.find(kv.first) == id_map.end()) {
				id_map[kv.first] = seq_id++;
			}
			for (auto &edge: kv.second.edges) {
				if (id_map.find(edge.dst_id) == id_map.end()) {
					id_map[edge.dst_id] = seq_id++;
				}
			}
		}
		*N = id_map.size();
		vector<PartGraph::Node> ret(*N);
		for (auto &kv: subgraphs[p]) {
			PartGraph::Node node = kv.second;
			int id = id_map[node.id];
			node.id = id;
			for (auto &edge: node.edges) {
				edge.dst_id = id_map[edge.dst_id];
			}
			ret[id] = node;
		}
		return ret;
	}
}

int main() {
	part::PartGraph partgraph(86054151, 64, "dataset.txt.part.64");
	partgraph.Process("triple2id.txt");
	int N, E;
	for (int i = 0; i < 4; i++) {
		partgraph.Output(i, "part" + to_string(i) + ".txt", &N, &E);
		cout << i << ": " << N << " " << E << endl;
	}
	return 0;
}