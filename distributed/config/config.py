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

class DistributedTrainConfig(object):
	def __init__(self, data_config, model_config, kvconfig, num_proc, num_epoch, loss_func):
		self.kvconfig = kvconfig
		self.data_config = data_config
		self.model_config = model_config
		self.num_proc = num_proc
		self.num_epoch = num_epoch
		self.loss_func = loss_func

class KVConfig(object):
	def __init__(self, name, addr, namebook):
		self.name = name
		self.addr = addr
		self.namebook = namebook

class DataConfig(object):
	def __init__(self, part, meta_path, data_path, meta_line, data_line, order, num_proc):
		self.meta_path = meta_path
		self.data_path = data_path
		self.meta_line = meta_line
		self.data_line = data_line
		self.order = order
		self.num_proc = num_proc
		self.part = part
