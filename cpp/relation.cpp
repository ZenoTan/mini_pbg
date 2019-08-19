#include "relation.h"

namespace relation {
void RelationStats::ProcessFile(const string &file_name) {
	ifstream file;
	file.open(file_name);
	string first_line;
	file >> first_line;
	int src, dst, rel;
	for (int i = 0; i < num_edge; i++) {
		file >> src;
		file >> dst;
		file >> rel;
		count_rel[rel]++;
	}
	file.close();
}
}

int main() {
	relation::RelationStats stats(14824, 338586276);
	stats.Process("triple2id.txt");
	vector<int> rel_count = stats.GetRelCount();
	ofstream rel_file;
	rel_file.open("rel.txt");
	for (int i = 0; i < rel_count.size(); i++) {
		rel_file << i << " " << rel_count[i] << endl;
	}
}