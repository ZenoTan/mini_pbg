from dgl.contrib import KVClient, KVServer
import torch as th
import torch.nn.functional as F

class ModelHandler(object):
	def __init__(self, model):
		self.model = model
		self.ent_size = [model.ent_size, model.dim]
		self.rel_size = [model.rel_size, model.head_operator.dim]

	def pull_entity(self, ID):
		return F.embedding(ID, self.model.emb.data, sparse=True)

	def push_entity(self, ID, data):
		self.model.emb.data[ID] = data

	def pull_relation(self):
		return self.model.head_operator.get_embedding(), self.model.tail_operator.get_embedding()

	def push_relation(self, head, tail):
		self.model.head_operator.put_embedding(head)
		self.model.tail_operator.put_embedding(tail)


class KGServer(KVServer):
	def __init__(self, config):
		super(KGServer, self).__init__(config.name, config.namebook, config.addr)
		self.start()

	def _push_handler(self, name, ID, data):
		if name == 'entity':
			for idx in range(ID.shape[0]):
				self._data_store[name][ID[idx]] = data[idx]
		else:
			for idx in range(ID.shape[0]):
				self._data_store[name][ID[idx]] = 0.94 * self._data_store[name][ID[idx]] + 0.06 * data[idx]

class KGClient(object):
	def __init__(self, config, dataset, model_handler):
		self.client = KVClient(config.name, config.namebook, config.addr)
		self.local_local = dataset.local_local
		self.local_remote = dataset.local_remote
		self.global_local = dataset.global_local
		self.global_remote = dataset.global_remote
		self.handler = model_handler
		self.num_node = dataset.num_node
		rel_range = list(range(self.handler.rel_size[0]))
		self.relation = th.tensor(rel_range)
		self.client.connect()

	def pull_remote(self):
		print("pull remote")
		data = self.client.pull('entity', self.global_remote)
		self.handler.push_entity(self.local_remote, data)

	def push_local(self):
		print("push local")
		data = self.handler.pull_entity(self.local_local)
		self.client.push('entity', self.global_local, data)

	def push_relation(self):
		print("push relation")
		head, tail = self.handler.pull_relation()
		self.client.push('head', self.relation, head)
		self.client.push('tail', self.relation, tail)

	def pull_relation(self):
		print("pull relation")
		head = self.client.pull('head', self.relation)
		tail = self.client.pull('tail', self.relation)
		# print("handler push relation")
		self.handler.push_relation(head, tail)

	def init_entity(self):
		self.client.init_data(name='entity', shape=[self.num_node], init_type='zero')

	def init_relation(self):
		self.client.init_data(name='head', shape=self.handler.rel_size, init_type='zero')
		self.client.init_data(name='tail', shape=self.handler.rel_size, init_type='zero')
