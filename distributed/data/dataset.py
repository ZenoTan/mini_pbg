from .loader import DataLoader, MetaLoader
import torch as th
import torch.multiprocessing as mp

class Dataset(object):
	def __init__(self, config):
		data_loader = DataLoader(config.order)
		print("Load data")
		index_dict = data_loader.load(config.data_path, config.data_line)
		self.head = index_dict['head_index']
		self.tail = index_dict['tail_index']
		self.rel = index_dict['rel_index']
		meta_loader = MetaLoader(config.part)
		print("Load meta")
		local_id, remote_id = meta_loader.load(config.meta_path, config.meta_line)
		self.num_edge = config.data_line
		self.num_node = config.meta_line
		#print(self.num_node)
		self.num_proc = config.num_proc
		self.proc_start = self.num_proc * [0]
		self.proc_limit = self.num_proc * [0]
		self.proc_cur = self.num_proc * [0]
		for i in range(self.num_proc):
			self.proc_start[i] = i * self.num_edge // self.num_proc
		for i in range(self.num_proc - 1):
			self.proc_limit[i] = self.proc_start[i + 1]
		self.proc_limit[self.num_proc - 1] = self.num_edge
		for i in range(self.num_proc):
			self.proc_cur[i] = self.proc_start[i]
		self.to_local = {}
		self.to_global = {}
		local = 0
		print("Remap")
		for i in range(self.num_edge):
			if i % 100000 == 0:
				print(i)
			if self.head[i] not in self.to_local:
				self.to_local[self.head[i]] = local
				self.to_global[local] = self.head[i]
				local += 1
			self.head[i] = self.to_local[self.head[i]]
			if self.tail[i] not in self.to_local:
				self.to_local[self.tail[i]] = local
				self.to_global[local] = self.tail[i]
				local += 1
			self.tail[i] = self.to_local[self.tail[i]]
		#self.num_node = local
		local_local_list = []
		global_local_list = []
		local_remote_list = []
		global_remote_list = []
		node_max = 0
		for node in local_id:
			if node in self.to_local:
				global_local_list.append(node)
				local_local_list.append(self.to_local[node])
			if node > node_max:
				node_max = node
		for node in remote_id:
			if node in self.to_local:
				global_remote_list.append(node)
				local_remote_list.append(self.to_local[node])
		self.local_local = th.tensor(local_local_list)
		self.global_local = th.tensor(global_local_list)
		self.local_remote = th.tensor(local_remote_list)
		self.global_remote = th.tensor(global_remote_list)
		self.head_index = th.tensor(self.head)
		self.tail_index = th.tensor(self.tail)
		self.rel_index = th.tensor(self.rel)
		print('Node max: ' + str(node_max))
		# self.head_index.share_memory()
		# self.tail_index.share_memory()
		# self.rel_index.share_memory()

	def shuffle(self):
		perm = th.randperm(self.num_edge)
		self.head_index = self.head_index[perm]
		self.tail_index = self.tail_index[perm]
		self.rel_index = self.rel_index[perm]

	def reset(self):
		for i in range(self.num_proc):
			self.proc_cur[i] = self.proc_start[i]

	def fetch(self, proc, batch_size):
		if self.proc_cur[proc] >= self.proc_limit[proc]:
			return None, None, None, 0
		size = batch_size
		if size > self.proc_limit[proc] - self.proc_cur[proc]:
			size = self.proc_limit[proc] - self.proc_cur[proc]
		self.proc_cur[proc] += size
		return self.head_index[self.proc_cur[proc] - size: self.proc_cur[proc]], self.tail_index[self.proc_cur[proc] - size: self.proc_cur[proc]], self.rel_index[self.proc_cur[proc] - size: self.proc_cur[proc]], size
