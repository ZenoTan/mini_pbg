from model import *
from config import ModelConfig, TrainConfig
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
	model_config = ModelConfig(head_operator, tail_operator, comparator, 1305371, 14824, 400, 1, 1000, 1000, 'Adagrad')
	# model = Model(config)
	loss_func = SoftmaxLoss(1000)
	train_config = TrainConfig('part0.txt', 'head-tail-rel', 80000, model_config, 4, 1, loss_func)
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
	index = th.randint(0, 10000, [10])
	data = th.randn(10)
	print('Start')
	print(type(index))
	#client.put_entity_embedding('simple', index, data)
	data_ = client.get_entity_embedding('simple', index)
	print(data_)

if __name__ == '__main__':
	test_rpc()
