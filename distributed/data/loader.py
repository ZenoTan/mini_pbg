import torch as th

class DataLoader(object):
	def __init__(self, order):
		self.order = order
		if order == 'head-rel-tail':
			self.cols = [0, 1, 2]
		elif order == 'head-tail-rel':
			self.cols = [0, 2, 1]
		elif order == 'rel-head-tail':
			self.cols = [1, 0, 2]
		else:
			self.cols = None

	def load(self, file_name, num_line):
		if self.cols == None:
			return None
		file = open('data/' + file_name)
		head_index = th.zeros([num_line], dtype=th.long)
		tail_index = th.zeros([num_line], dtype=th.long)
		rel_index = th.zeros([num_line], dtype=th.long)
		num = 0
		while (not num_line) or num < num_line:
			line = file.readline()
			num += 1
			if line == '':
				break
			cols = line.split()
			head_index[i] = int(cols[self.cols[0]])
			rel_index[i] = int(cols[self.cols[1]])
			tail_index[i] = int(cols[self.cols[2]])
		file.close()
		return {'head_index': head_index, 'tail_index': tail_index, 'rel_index': rel_index}
