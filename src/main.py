from model import *
from config import ModelConfig, TrainConfig
from data import DataLoader
from train import *
import time

if __name__ == '__main__':
	head_operator = ComplExOperator(14824, 400)
	tail_operator = ComplExOperator(14824, 400)
	comparator = DotComparator()
	model_config = ModelConfig(head_operator, tail_operator, comparator, 1305371, 14824, 400, 1, 1000, 1000, 'Adagrad')
	# model = Model(config)
	loss_func = SoftmaxLoss(1000)
	train_config = TrainConfig('part0.txt', 'head-tail-rel', 320000, model_config, 16, 1, loss_func)
	trainer = new Trainer(train_config)
	t0 = time.time()
	trainer.train()
	t1 = time.time()
	print('Finish all: ' + str(t1 - t0))