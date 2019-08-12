from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import torch as th

class SharedEmbeddingServer(object):
	def __init__(self, port):
		self.server = SimpleXMLRPCServer(("127.0.0.1", port), logRequests=False)
		self.handlers = {}
	
		def get_embedding(name, emb_type, emb_id):
			if name not in self.handlers:
				return None
			if emb_type == 'entity':
				return self.handlers[name].get_entity(th.tensor(emb_id)).tolist()
			elif emb_type == 'relation':
				return self.handlers[name].get_relation(th.tensor(emb_id)).tolist()
			else:
				return None

		def put_embedding(name, emb_type, emb_id, data):
			if name not in self.handlers:
				return
			if emb_type == 'entity':
				return self.handlers[name].put_entity(th.tensor(emb_id), th.tensor(data))
			elif emb_type == 'relation':
				return self.handlers[name].put_relation(th.tensor(emb_id), th.tensor(data))
			else:
				return

		self.server.register_function(get_embedding, "get_embedding")
		self.server.register_function(put_embedding, "put_embedding")

	def add_handler(self, handler):
		if handler.name not in self.handlers:
			self.handlers[handler.name] = handler

	def remove_handler(self, handler_name):
		if handler_name in self.handlers:
			del self.handlers[handler_name]

	def run(self):
		self.server.serve_forever()

class SharedEmbeddingClient(object):
	def __init__(self, port):
		self.client = xmlrpc.client.ServerProxy('http://localhost:' + str(port))

	def get_entity_embedding(self, name, emb_id):
		return self.client.get_embedding(name, 'entity', emb_id)

	def get_relation_embedding(self, name, emb_id):
		return self.client.get_embedding(name, 'relation', emb_id)

	def put_entity_embedding(self, name, emb_id, data):
		self.client.put_embedding(name, 'entity', emb_id, data)

	def put_relation_embedding(self, name, emb_id, data):
		self.client.put_embedding(name, 'relation', emb_id, data)
