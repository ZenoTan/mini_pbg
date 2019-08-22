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

	def load(self, file_name, num_line=1e12):
		if self.cols == None:
			return None
		file = open('data/' + file_name)
		head_index = th.zeros([num_line], dtype=th.long)
		tail_index = th.zeros([num_line], dtype=th.long)
		rel_index = th.zeros([num_line], dtype=th.long)
		num = 0
		while num < num_line:
			if num % 100000 == 0:
				print(num)
			line = file.readline()
			num += 1
			if line == '':
				break
			head, tail, rel = line.split()
			head = int(head)
			tail = int(tail)
			rel = int(rel)
			head_index[num - 1], tail_index[num - 1], rel_index[num - 1] = head, tail, rel
		file.close()
		return {'head_index': head_index, 'tail_index': tail_index, 'rel_index': rel_index}

class MetaLoader(object):
	def __init__(self, part):
		self.part = part

	def load(self, file_name, num_line=1e12):
		local = []
		remote = []
		file = open('data/' + file_name)
		index = 0
		while index < num_line:
			if num % 100000 == 0:
				print(num)
			line = file.readline()
			if line == '':
				break
			part = int(line)
			if part == self.part:
				local.append(index)
			else:
				remote.append(index)
			index += 1
		return local, remote
		
