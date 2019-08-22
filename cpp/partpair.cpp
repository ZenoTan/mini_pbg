#include "partpair.h"

namespace part {
	void PartPair::Process(const string &data_file_name) {
		ifstream file;
		file.open(data_file_name);
		int src, dst, rel, src_part, dst_part;
		string first_line;
		file >> first_line;
		for (int i = 0; i < num_edge; i++) {
			file >> src;
			file >> dst;
			file >> rel;
			src_part = partmap.GetPart(src);
			dst_part = partmap.GetPart(dst);
			pair<int, int> p;
			if (src_part <= dst_part) {
				p = {src_part, dst_part};
			} else {
				p = {dst_part, src_part};
			}
			if (edges.find(p) == edges.end()) {
				edges[p] = {};
			}
			vector<int> edge{src, dst, rel};
			edges[p].push_back(edge);
		}
		file.close();
	}
	void PartPair::OutputPair(vector<pair<int, int>> pairs, const string &file_name) {
		ofstream file;
		file.open(file_name);
		for (auto &p: pairs) {
			for (auto &edge: edges[p]) {
				file << edge[0] << ' ';
				file << edge[1] << ' ';
				file << edge[2] << endl;
			}
		}
		file.close();
	}
}

int main() {
	part::PartPair partpair(86054151, 338586276, 16, "dataset.txt.part.16");
	partpair.Process("triple2id.txt");
	for (int i = 0; i < 16; i++) {
		vector<pair<int, int>> pairs;
		for (int j = 0; j < 16; j++) {
			int small, large;
			if (i <= j) {
				small = i;
				large = j;
			} else {
				small = j;
				large = i;
			}
			pairs.push_back(make_pair<int, int>(small, large));
		}
		partpair.OutputPair(pairs, to_string(i) + ".txt")
	}
	return 0;
}