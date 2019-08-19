#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

#define MAX_COUNT 200000
#define RELATION 145

void extract(const string &input_file, const string &output_file) {
	ifstream input;
	ofstream output;
	input.open(input_file);
	output.open(output_file);
	int count = 0;
	int src, dst, rel;
	while (count < MAX_COUNT) {
		input >> src;
		input >> dst;
		input >> rel;
		if (rel == RELATION) {
			count++;
			output << src << " " << dst << endl;
		}
	}
	input.close();
	output.close();
}

int main() {
	extract("part0.txt", "train0.txt");
	extract("part1.txt", "train1.txt");
	extract("part2.txt", "train2.txt");
	extract("part3.txt", "train3.txt");
}