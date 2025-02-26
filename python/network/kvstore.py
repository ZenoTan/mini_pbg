from dgl.contrib import KVClient, KVServer
from .network import BaseServer, BaseClient
from config import SharedKVConfig
import time

class CustomKVServer(KVServer):
	def __init__(self, name, clients, addr):
		super(CustomKVServer, self).__init__(name, clients, addr)
		self.handlers = {}

	def add_handler(self, handler):
		self.handlers[handler.name] = handler

	def _push_handler(self, name, ID, data):
		if name not in self.handlers:
			return
		self.handlers[name].put_entity(ID, data)

	def _pull_handler(self, name, ID):
		if name not in self.handlers:
			return None
		return self.handlers[name].get_entity(ID)

class SharedKVServer(BaseServer):
	def __init__(self, config):
		super(SharedKVServer, self).__init__()
		self.addr = config.addr
		self.name = config.name
		self.clients = config.namebook
		self.server = CustomKVServer(self.name, self.clients, self.addr)

	def run(self):
		for name in self.handlers:
			self.server.add_handler(self.handlers[name])
		self.server.start()

class SharedKVClient(BaseClient):
	def __init__(self, config, entity_shape):
		super(SharedKVClient, self).__init__()
		self.addr = config.addr
		self.name = config.name
		self.servers = config.namebook
		self.client = KVClient(client_id = self.name, server_namebook = self.servers, client_addr = self.addr)
		time.sleep(1)
		self.client.connect()
		for entity in entity_shape:
			self.client.init_data(name=entity, shape=entity_shape[entity], init_type='zero')

	def get_entity_embedding(self, name, emb_id):
		return self.client.pull(name, emb_id)

	def get_relation_embedding(self, name, emb_id):
		return None

	def put_entity_embedding(self, name, emb_id, data):
		self.client.push(name, emb_id, data)

	def put_relation_embedding(self, name, emb_id, data):
		pass

class GlobalKVServer(SharedKVServer):
	pass

class GlobalKVClient(SharedKVClient):
	pass