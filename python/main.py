from model import *
from config import *
from data import DataLoader
from train import *
from network import *
import torch as th
import torch.multiprocessing as mp
import time

def test_train():
	head_operator = ComplExOperator(14824, 400)
	tail_operator = ComplExOperator(14824, 400)
	comparator = DotComparator()
	model_config = ModelConfig(head_operator, tail_operator, comparator, 1305371, 14824, 400, 8, 128, 256, 'Adagrad')
	# model = Model(config)
	loss_func = SoftmaxLoss(1024)
	train_config = TrainConfig('part0.txt', 'head-tail-rel', 192 * 1024,  model_config, 16, 1, loss_func)
	trainer = Trainer(train_config)
	t0 = time.time()
	trainer.train()
	t1 = time.time()
	print('Finish all: ' + str(t1 - t0))

def server_proc(server):
	server.run()

def test_rpc():
	head_operator = ComplExOperator(14824, 400)
	tail_operator = ComplExOperator(14824, 400)
	comparator = DotComparator()
	model_config = ModelConfig(head_operator, tail_operator, comparator, 1305371, 14824, 400, 1, 1000, 1000, 'Adagrad')
	model = Model(model_config)
	handler = SimpleHandler('simple', model)
	server = SharedEmbeddingServer(10314)
	server.add_handler(handler)
	# server.run()
	p = mp.Process(target=server_proc, args=(server, ))
	p.start()
	client = SharedEmbeddingClient(10314)
	index = list(range(40))
	data = th.randn(40, 400).tolist()
	#print(data[0][0])
	#print(type(index))
	t0 = time.time()
	for i in range(1):
		client.put_entity_embedding('simple', index, data)
		data_ = client.get_entity_embedding('simple', index)
	#print(data_[0][0])
	t1 = time.time()
	print(t1 - t0)

def test_ipc(method):
	head_operator = ComplExOperator(14824, 400)
	tail_operator = ComplExOperator(14824, 400)
	comparator = DotComparator()
	model_config = ModelConfig(head_operator, tail_operator, comparator, 1305371, 14824, 400, 1, 1000, 1000, 'Adagrad')
	model = Model(model_config)
	handler = SimpleHandler(0, model)
	multi_config = MultiProcessConfig(2, method)
	proxy = Proxy(multi_config)
	server = SharedMultiServer(proxy)
	server.add_handler(handler)
	p = mp.Process(target=server_proc, args=(server, ))
	p.start()
	client = SharedMultiClient(1, proxy)
	index = th.randint(0, 1000, [1000])
	data = th.randn(1000, 400)
	# print(data[0][0])
	t0 = time.time()
	for i in range(10000):
		client.put_entity_embedding(0, index, data)
		data_ = client.get_entity_embedding(0, index)
		# print(data_[0][0])
	t1 = time.time()
	print(t1 - t0)

def test_kv():
	head_operator = ComplExOperator(14824, 400)
	tail_operator = ComplExOperator(14824, 400)
	comparator = DotComparator()
	model_config = ModelConfig(head_operator, tail_operator, comparator, 1305371, 14824, 400, 1, 1000, 1000, 'Adagrad')
	model = Model(model_config)
	handler = SimpleHandler('test', model)
	client_namebook = {1: 12341}
	server_namebook = {0: 12340}
	server_config = SharedKVConfig(0, 12340, client_namebook)
	client_config = SharedKVConfig(1, 12341, server_namebook)
	server = SharedKVServer(server_config)
	server.add_handler(handler)
	p = mp.Process(target=server_proc, args=(server, ))
	p.start()
	client = SharedKVClient(client_config, {'test': [1305371, 400]})
	index = th.randint(0, 1000, [1000])
	data = th.randn(1000, 400)
	# print(data[0][0])
	t0 = time.time()
	for i in range(100):
		client.put_entity_embedding('test', index, data)
		data_ = client.get_entity_embedding('test', index)
		# print(data_[0][0])
	t1 = time.time()
	print(t1 - t0)

if __name__ == '__main__':
	test_train()
