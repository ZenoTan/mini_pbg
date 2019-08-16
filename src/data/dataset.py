from .loader import DataLoader
import torch as th

class DataSet(object):
	def __init__(self, config):
		self.local_file = config.local_file
		self.shared_files = config.shared_files
		self.order = config.order
		self.local = None
		self.shared = {}
		self.local_cur = 0
		self.shared_cur = {}

	def prepare(self):
		loader = DataLoader(self.order)
		self.local = loader.load(local_file)
		for partition_id in self.shared_files:
			self.shared[partition_id] = loader.load(shared_files[partition_id])
			self.shared_cur[partition_id] = 0

	def fetch(self, partition_id, batch_size):
		if not partition_id:
			if self.local_cur >= self.local.size()[0]:
				return None, None
			else:
				if self.local.size(0) >= self.local_cur + batch_size:
					self.local_cur += batch_size
					return self.local[self.local_cur - batch_size: self.local_cur], batch_size
				else:
					left = self.local.size(0) - self.local_cur
					ret = th.zeros([batch_size], dtype=long)
					ret[:left] = self.local[self.local_cur: self.local.size(0)]
					self.local_cur += left
					return ret, left
		else:
			if self.shared_cur[partition_id] >= self.shared[partition_id].size()[0]:
				return None, None
			else:
				if self.shared[partition_id].size(0) >= self.shared_cur[partition_id] + batch_size:
					self.shared_cur[partition_id] += batch_size
					return self.shared[partition_id][self.shared_cur[partition_id] - batch_size: self.shared_cur[partition_id]], batch_size
				else:
					left = self.shared[partition_id].size(0) - self.shared_cur[partition_id]
					ret = th.zeros([batch_size], dtype=th.long)
					ret[:left] = self.shared[self.shared_cur[partition_id]: self.shared[partition_id].size(0)]
					self.shared_cur[partition_id] += left
					return ret, left

	def reset(self, partition_id):
		if not partition_id:
			self.local_cur = 0
		else:
			self.shared_cur[partition_id] = 0

	def shuffle(self, partition_id):
		if not partition_id:
			perm = th.randperm(self.local.size(0))
			self.local = self.local[perm]
		else:
			perm = th.randperm(self.shared[partition_id].size(0))
			self.shared[partition_id] = self.shared[partition_id][perm]
		self.reset(partition_id)
