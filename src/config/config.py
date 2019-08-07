class ModelConfig(object):
	def __init__(self, head_operator, tail_operator, comparator, ent_size, rel_size, dim, chunk_size, pos_num, neg_num, optim):
		self.head_operator = head_operator
		self.tail_operator = tail_operator
		self.comparator = comparator
		self.num_dict = {}
		self.num_dict['ent_size'] = ent_size
		self.num_dict['rel_size'] = rel_size
		self.num_dict['dim'] = dim
		self.num_dict['chunk_size'] = chunk_size
		self.num_dict['pos_num'] = pos_num
		self.num_dict['neg_num'] = neg_num
		self.optim = optim