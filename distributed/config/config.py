class ModelConfig(object):
	def __init__(self, head_operator, tail_operator, comparator, ent_size, rel_size, dim, num_chunk, pos_num, neg_num, optim):
		self.head_operator = head_operator
		self.tail_operator = tail_operator
		self.comparator = comparator
		self.num_dict = {}
		self.num_dict['ent_size'] = ent_size
		self.num_dict['rel_size'] = rel_size
		self.num_dict['dim'] = dim
		self.num_dict['num_chunk'] = num_chunk
		self.num_dict['pos_num'] = pos_num
		self.num_dict['neg_num'] = neg_num
		self.optim = optim

class TrainConfig(object):
	def __init__(self, data_path, data_order, num_edge, model_config, num_proc, num_epoch, loss_func):
		self.data_path = data_path
		self.data_order = data_order
		self.num_edge = num_edge
		self.model_config = model_config
		self.num_proc = num_proc
		self.num_epoch = num_epoch
		self.loss_func = loss_func

class DistributedTrainConfig(TrainConfig):
	def __init__(self, local_path, remote_paths, data_order, num_edge, remote_edges, model_config, num_proc, num_epoch, loss_func):
		super(DistributedTrainConfig, self).__init__(local_path, data_order, num_edge, model_config, num_proc, num_epoch, loss_func)
		self.remote_paths = remote_paths
		self.remote_edges = remote_edges

class MultiProcessConfig(object):
	def __init__(self, num_rank, is_connected=True, network=None, method='pipe'):
		self.num_rank = num_rank
		if not is_connected:
			self.network = network
		else:
			self.network = []
			for src in range(num_rank):
				for dst in range(num_rank):
					if src != dst:
						self.network.append((src, dst))
		self.method = method
class SharedKVConfig(object):
	def __init__(self, name, port, namebook):
		header = '127.0.0.1:'
		self.name = name
		self.addr = header + str(port)
		self.namebook = {}
		for name in namebook:
			self.namebook[name] = header + str(namebook[name])

class GlobalKVConfig(object):
	def __init__(self, name, addr, namebook):
		self.name = name
		self.addr = addr
		self.namebook = namebook

class DataConfig(object):
	def __init__(self, file, order):
		self.file_name = file_name
		self.num_line = num_line
		self.order = order
		self.num_proc
