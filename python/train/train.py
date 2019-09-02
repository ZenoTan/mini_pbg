import torch as th
import torch.multiprocessing as mp
import torch.nn.functional as F
import time
from data import DataLoader, DataSet
from model import *

def train_proc(model, rank, head_index, tail_index, rel_index, loss_func):
	th.set_num_threads(1)
	num_iter = head_index.size()[0]
	sample0 = time.time()
	head_neg_index = th.randint(0, model.ent_size, [num_iter, model.num_chunk * model.neg_num])
	tail_neg_index = th.randint(0, model.ent_size, [num_iter, model.num_chunk * model.neg_num])
	# rel_neg_index = th.randint(0, model.rel_size, [num_iter, model.num_chunk * model.neg_num])
	sample1 = time.time()
	print('Sample: ' + str(sample1 - sample0))
	forward_time = 0.0
	backward_time = 0.0
	step_time = 0.0
	#t0 = time.time()
	for i in range(num_iter):
		t0 = time.time()
		model.zero_grad()
		head_pos, head_neg, tail_pos, tail_neg = model(head_index[i], tail_index[i], head_neg_index[i], tail_neg_index[i], rel_index[i])
		loss = loss_func.loss(head_pos, head_neg, tail_pos, tail_neg)
		t1 = time.time()
		loss.backward()
		t2 = time.time()
		model.optim.step()
		t3 = time.time()
		forward_time += t1 - t0
		backward_time += t2 - t1
		step_time += t3 - t2
	#t1 = time.time()
	print("Rank " + str(rank) + "forward: " + str(forward_time))
	print("Rank " + str(rank) + "backward: " + str(backward_time))
	print("Rank " + str(rank) + "step: " + str(step_time))

class Loss(object):
	def __init__(self, batch_size):
		self.batch_size = batch_size

	def loss(self, head_pos, head_neg, tail_pos, tail_neg):
		return None

class SoftmaxLoss(Loss):
	def __init__(self, batch_size):
		super(SoftmaxLoss, self).__init__(batch_size)
		self.target = th.zeros([batch_size], dtype=th.long)

	def loss(self, head_pos, head_neg, tail_pos, tail_neg):
		head_scores = th.cat([head_pos, head_neg.logsumexp(dim=1, keepdim=True)], dim=1)
		tail_scores = th.cat([tail_pos, tail_neg.logsumexp(dim=1, keepdim=True)], dim=1)
		loss = F.cross_entropy(head_scores, self.target) + F.cross_entropy(tail_scores, self.target)
		return loss

class BaseTrainer(object):
	def __init__(self):
		pass

	def train(self):
		pass

class Trainer(BaseTrainer):
	def __init__(self, train_config):
		super(Trainer, self).__init__()
		self.data_path = train_config.data_path
		self.data_order = train_config.data_order
		self.num_edge = train_config.num_edge
		self.model_config = train_config.model_config
		self.num_proc = train_config.num_proc
		self.num_epoch = train_config.num_epoch
		self.loss_func = train_config.loss_func

	def train(self):
		# TODO: split local and remote samples
		data_loader = DataLoader(self.data_order)
		dataset = data_loader.load(self.data_path, self.num_edge)
		head_index = dataset['head_index']
		tail_index = dataset['tail_index']
		rel_index = dataset['rel_index']
		model = Model(self.model_config)
		model.share_memory()
		for epoch in range(self.num_epoch):
			# TODO: last batch may not be complete
			perm = th.randperm(self.num_edge)
			head_index = head_index[perm].view(self.num_proc, -1, model.num_chunk * model.pos_num)
			tail_index = tail_index[perm].view(self.num_proc, -1, model.num_chunk * model.pos_num)
			rel_index = rel_index[perm].view(self.num_proc, -1, model.num_chunk * model.pos_num)
			procs = []
			for proc in range(self.num_proc):
				p = mp.Process(target=train_proc, args=(model, proc, head_index[proc], tail_index[proc], rel_index[proc], self.loss_func))
				p.start()
				procs.append(p)
			for p in procs:
				p.join()

class DistributedTrainer(object):
	def __init__(self, train_config):
		self.local_path = train_config.data_path
		self.remote_paths = train_config.remote_paths
		self.data_order = train_config.data_order
		self.local_edge = train_config.num_edge
		self.remote_edges = train_config.remote_edges
		self.model_config = train_config.model_config
		self.num_proc = train_config.num_proc
		self.num_epoch = train_config.num_epoch
		self.loss_func = train_config.loss_func
	
	def train(self):
		# TODO: add all together here
		pass
