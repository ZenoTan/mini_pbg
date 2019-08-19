#include "degree.h"
#include <iostream>

namespace degree {
	void DegreeBucket::ProcessFile(const string &file_name) {
		ifstream file;
		file.open(file_name);
		string first_line;
		file >> first_line;
		int src, dst, rel;
		for (int i = 0; i < num_edge; i++) {
			file >> src;
			file >> dst;
			file >> rel;
			count_in[dst]++;
			count_out[src]++;
			count_all[src]++;
			count_all[dst]++;
		}
		file.close();
	}
	void DegreeBucket::ProcessResult() {
		BucketSort(count_in, degree_in);
		BucketSort(count_out, degree_out);
		BucketSort(count_all, degree_all);
	}
	void DegreeBucket::BucketSort(vector<int> &count, vector<int> &degree) {
		for (int &num: count) {
			if (num > degree.size()) {
				degree.resize(num, 0);
			} 
			assert(num <= degree.size());
			degree[num - 1]++;
		}
	}
}

int main() {
	degree::DegreeBucket bucket(86054151, 338586276);
	bucket.Process("triple2id.txt");
	vector<int> in_degree = bucket.GetInDegree();
	vector<int> out_degree = bucket.GetOutDegree();
	vector<int> all_degree = bucket.GetAllDegree();
	ofstream in_file;
	in_file.open("in_degree.txt");
	ofstream out_file;
	out_file.open("out_degree.txt");
	ofstream all_file;
	all_file.open("all_degree.txt");
	for (int i = 0; i < all_degree.size(); i++) {
		if (all_degree[i] > 0) {
			all_file << i + 1 << " " << all_degree[i] << endl; 
		}
	}
	for (int i = 0; i < in_degree.size(); i++) {
		if (in_degree[i] > 0) {
			in_file << i + 1 << " " << in_degree[i] << endl; 
		}
	}
	for (int i = 0; i < out_degree.size(); i++) {
		if (out_degree[i] > 0) {
			out_file << i + 1 << " " << out_degree[i] << endl; 
		}
	}
	in_file.close();
	out_file.close();
	all_file.close();
}