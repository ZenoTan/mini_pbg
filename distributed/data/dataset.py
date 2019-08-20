from .loader import DataLoader
import torch as th
import torch.multiprocessing as mp

class Dateset(obejct):
	def __init__(self, config):
		data_loader = DataLoader(config.order)
		self.head_index, self.tail_index, self.rel_index = data_loader.load(config.file_name, config.num_line)
		self.num_edge = config.num_line
		self.num_proc = config.num_proc
		self.proc_start = self.num_proc * [0]
		self.proc_limit = self.num_proc * [0]
		self.proc_cur = self.num_proc * [0]
		for i in range(self.num_proc):
			self.proc_start[i] = i * self.num_edge // self.num_proc
		for i in range(self.num_proc - 1):
			self.proc_limit[i] = self.proc_start[i + 1]
		self.proc_limit[num_proc - 1] = self.num_edge
		for i in range(self.num_proc):
			self.proc_cur[i] = self.proc_start[i]
		self.to_local = {}
		self.to_global = {}
		local = 0
		for i in range(num_line):
			if self.head_index[i] not in self.to_local:
				self.to_local[head_index[i]] = local
				self.to_global[local] = self.head_index[i]
				local += 1
			self.head_index[i] = to_local[self.head_index[i]]
			if self.tail_index[i] not in self.to_local:
				self.to_local[tail_index[i]] = local
				self.to_global[local] = self.tail_index[i]
				local += 1
			self.tail_index[i] = to_local[self.tail_index[i]]
		self.head_index.shared_memory()
		self.tail_index.shared_memory()
		self.rel_index.shared_memory()

	def shuffle(self):
		perm = th.randperm(self.num_edge)
		self.head_index = self.head_index[perm]
		self.tail_index = self.tail_index[perm]

	def reset(self):
		for i in range(self.num_proc):
			self.proc_cur[i] = self.proc_start[i]

	def fetch(self, proc, batch_size):
		if self.proc_cur[proc] >= self.proc_limit[proc]:
			return None
		size = batch_size
		if size > self.proc_limit[proc] - self.proc_cur[proc]:
			size = self.proc_limit[proc] - self.proc_cur[proc]
		self.proc_cur[proc] += size
		return self.head_index[self.proc_cur[proc] - size: self.proc_cur[proc]], self.tail_index[self.proc_cur[proc] - size: self.proc_cur[proc]], self.rel_index[self.proc_cur[proc] - size: self.proc_cur[proc]], size