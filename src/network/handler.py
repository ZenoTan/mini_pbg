from model import Model

import torch as th
import torch.nn.functional as F

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
		return F.embedding(emb_id, self.model.emb.data, sparse=True)

	def put_entity(self, emb_id, data):
		self.model.emb.data[emb_id] = data

	def get_relation(self, emb_id):
		return None

	def put_relation(self, emb_id, data):
		pass
		
