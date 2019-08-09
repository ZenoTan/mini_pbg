from model import Model

import torch as th
import torch.nn.functional as F
import time

class Handler(object):
	def __init__(self, name, model):
		self.name = name
		self.model = model

	def get_entity(self, emb_id):
		return None

	def put_entity(self, emb_id, data):
		pass

	def get_relation(self, emb_id):
		return None

	def put_relation(self, emb_id, data):
		pass

class SimpleHandler(Handler):
	def __init__(self, name, model):
		super(SimpleHandler, self).__init__(name, model)

	def get_entity(self, emb_id):
		t0 = time.time()
		entity = F.embedding(th.tensor(emb_id), self.model.emb.data, sparse=True).tolist()
		t1 = time.time()
		print('get: ' + str(t1 - t0))
		return entity

	def put_entity(self, emb_id, data):
		t0 = time.time()
		self.model.emb.data[emb_id] = th.tensor(data)
		t1 = time.time()
		print('put: ' + str(t1 - t0))
		#for i in range(len(data)):
		#	self.model.emb.data[emb_id[i]] = th.tensor(data[i])
		return 1

	def get_relation(self, emb_id):
		return None

	def put_relation(self, emb_id, data):
		pass
		
