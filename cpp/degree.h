#ifndef DEGREE_H
#define DEGREE_H

#include <vector>
#include <string>
#include <fstream>

using namespace std;

namespace degree {

class DegreeBucket {
public:
	DegreeBucket(int N, int E): num_node(N), num_edge(E) {
		count_in.resize(N);
		count_out.resize(N);
		count_all.resize(N);
	}
	void Process(const string &file_name) {
		ProcessFile(file_name);
		ProcessResult();
	}
	vector<int> GetInDegree() {
		return degree_in;
	}
	vector<int> GetOutDegree() {
		return degree_out;
	}
	vector<int> GetAllDegree() {
		return degree_all;
	}
private:
	const int num_node;
	const int num_edge;
	vector<int> degree_in;
	vector<int> degree_out;
	vector<int> count_in;
	vector<int> count_out;
	vector<int> degree_all;
	vector<int> count_all;
	void ProcessFile(const string &file_name);
	void ProcessResult();
	void BucketSort(vector<int> &count, vector<int> &degree);
};

}

#endif
