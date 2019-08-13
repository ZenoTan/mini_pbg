class BaseServer(object):
	def __init__(self):
		self.handlers = {}

	def add_handler(self, handler):
		if handler.name not in self.handlers:
			self.handlers[handler.name] = handler

	def remove_handler(self, handler_name):
		if handler_name in self.handlers:
			del self.handlers[handler_name]

	def run(self):
		pass

class BaseClient(object):
	def __init__(self):
		pass

	def get_entity_embedding(self, name, emb_id):
		return None

	def get_relation_embedding(self, name, emb_id):
		return None

	def put_entity_embedding(self, name, emb_id, data):
		pass

	def put_relation_embedding(self, name, emb_id, data):
		pass
