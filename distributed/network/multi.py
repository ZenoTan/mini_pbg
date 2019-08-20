import torch as th
import torch.multiprocessing as mp
from .network import BaseServer, BaseClient
import threading

class Proxy(object):
	def __init__(self, config):
		# super(WorkerManager, self).__init__()
		self.num_rank = config.num_rank
		self.network = config.network
		self.method = config.method
		self.channels = {}
		if self.method == 'pipe':
			for pair in self.network:
				if pair not in self.channels:
					self.channels[pair] = mp.Pipe(duplex=False)
		elif self.method == 'queue':
			for pair in network:
				self.channels[pair] = mp.SimpleQueue()

	def get_channel(self, pair):
		if pair in self.channels:
			return self.channels[pair]
		else:
			return None

	def send(self, src, dst, data):
		ch = self.get_channel((src, dst))
		if ch == None:
			return -1
		else:
			if self.method == 'pipe':
				ch[1].send(data)
			else:
				ch.put(data)

	def recv(self, src, dst):
		ch = self.get_channel((src, dst))
		if ch == None:
			return -1
		else:
			if self.method == 'pipe':
				data = ch[0].recv()
				return data
			else:
				data = ch.get()
				return data

def listen(handler, proxy, local, remote):
	while True:
		header = proxy.recv(remote, local)
		emb_id = proxy.recv(remote, local)
		if header == 'get':
			data = handler.get_entity(emb_id)
			proxy.send(local, remote, data)
		elif header == 'put':
			data = proxy.recv(remote, local)
			handler.put_entity(emb_id, data)
		else:
			pass

class SharedMultiServer(BaseServer):
	def __init__(self, proxy):
		super(SharedMultiServer, self).__init__()
		self.proxy = proxy
		self.channels = []
	
	def init_channel(self):
		for src, dst in self.proxy.network:
			if src in self.handlers and (dst, src) in self.proxy.network:
				self.channels.append((src, dst))

	# def get_embedding(self, src, dst, emb_type, emb_id):
	# 	if name not in self.handlers:
	# 		return None
	# 	if (src, dst) not in self.proxy.network
	# 		return None
	# 	if emb_type == 'entity':
	# 		data = self.handlers[name].get_entity(emb_id)
	# 		proxy.send(src, dst, data)
	# 	elif emb_type == 'relation':
	# 		data = self.handlers[name].get_relation(emb_id)
	# 		proxy.send(src, dst, data)
	# 	else:
	# 		return None

	# def put_embedding(self, src, dst, emb_type, emb_id):
	# 	if name not in self.handlers:
	# 		return
	# 	if (src, dst) not in self.proxy
	# 		return
	# 	if emb_type == 'entity':
	# 		return self.handlers[name].put_entity(emb_id, data)
	# 	elif emb_type == 'relation':
	# 		return self.handlers[name].put_relation(emb_id, data)
	# 	else:
	# 		return

	def run(self):
		self.init_channel()
		threads = []
		for src, dst in self.channels:
			thread = threading.Thread(target=listen, args=(self.handlers[src], self.proxy, src, dst))
			thread.start()
			threads.append(thread)
		for thread in threads:
			thread.join()
class SharedMultiClient(BaseClient):
	def __init__(self, sender, proxy):
		super(SharedMultiClient, self).__init__()
		self.sender = sender
		self.proxy = proxy

	def get_entity_embedding(self, name, emb_id):
		self.proxy.send(self.sender, name, 'get')
		self.proxy.send(self.sender, name, emb_id)
		data = self.proxy.recv(name, self.sender)
		return data

	def get_relation_embedding(self, name, emb_id):
		return None

	def put_entity_embedding(self, name, emb_id, data):
		self.proxy.send(self.sender, name, 'put')
		self.proxy.send(self.sender, name, emb_id)
		self.proxy.send(self.sender, name, data)

	def put_relation_embedding(self, name, emb_id, data):
		pass
