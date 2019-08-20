#include "partpair.h"

namespace part {
	void PartPair::Process(const string &data_file_name) {
		ifstream file;
		file.open(data_file_name);
		int src, dst, rel, src_part, dst_part;
		string first_line;
		file >> first_line;
		for (int i = 0; i < num_node; i++) {
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
	part::PartPair partpair(86054151, 4, "dataset.txt.part.4");
	partpair.Process("triple2id.txt");
	partpair.OutputPair({make_pair<int, int>(0, 0)}, "0-0.txt");
	return 0;
}