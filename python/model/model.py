import torch as th
import torch.nn as nn
import torch.multiprocessing as mp
import torch.nn.functional as F
# from .config.config import ModelConfig


class Operator(nn.Module):
	def __init__(self, rel_size, dim):
		super(Operator, self).__init__()
		self.rel_size = rel_size
		self.dim = dim

	def forward(self, input, op_index):
		pass

class ComplExOperator(Operator):
	def __init__(self, rel_size, dim):
		super(ComplExOperator, self).__init__(rel_size, dim)
		self.real = nn.Parameter(th.rand(rel_size, dim // 2))
		self.imag = nn.Parameter(th.rand(rel_size, dim // 2))
		# self.head_imag = nn.Parameter(th.rand(rel_size, dim // 2))
		# self.tail_imag = nn.Parameter(th.rand(rel_size, dim // 2))

	def forward(self, emb, rel_index):
		rel_real = F.embedding(rel_index, self.real, sparse=True)
		rel_imag = F.embedding(rel_index, self.imag, sparse=True)
		emb_real = emb[..., :self.dim // 2]
		emb_imag = emb[..., self.dim // 2:]
		emb_complex = th.empty_like(emb)
		emb_complex[..., :self.dim // 2] = emb_real * rel_real - emb_imag * rel_imag
		emb_complex[..., self.dim // 2:] = emb_real * rel_imag + emb_imag * rel_real
		return emb_complex

class DismultOperator(Operator):
	def __init__(self, rel_size, dim):
		super(DismultOperator, self).__init__(rel_size, dim)
		self.relation = nn.Parameter(th.rand(rel_size, dim))

	def forward(self, emb, rel_index):
		rel = F.embedding(rel_index, self.relation, sparse=True)
		return emb * rel

class Comparator(nn.Module):
	def __init__(self):
		super(Comparator, self).__init__()

	def forward(self, head, pos, neg):
		pass

class DotComparator(nn.Module):
	def __init__(self):
		super(DotComparator, self).__init__()

	def forward(self, head, pos, neg):
		pos_scores = (head * pos).sum(-1)
		neg_scores = th.bmm(head, neg.transpose(-1, -2))
		#pos_scores = pos_scores.unsqueeze(1)
		return pos_scores, neg_scores

class Model(nn.Module):
	def __init__(self, model_config):
		super(Model, self).__init__()
		self.ent_size = model_config.num_dict['ent_size']
		self.rel_size = model_config.num_dict['rel_size']
		self.dim = model_config.num_dict['dim']
		self.emb = nn.Parameter(th.rand(self.ent_size, self.dim))
		self.head_operator = model_config.head_operator
		self.tail_operator = model_config.tail_operator
		self.comparator = model_config.comparator
		self.num_chunk = model_config.num_dict['num_chunk']
		self.pos_num = model_config.num_dict['pos_num']
		self.neg_num = model_config.num_dict['neg_num']
		self.mask = th.zeros([self.pos_num, self.pos_num + self.neg_num])
		for i in range(self.pos_num):
			self.mask[i][i] = -1e9
		if model_config.optim == 'Adagrad':
			self.optim = th.optim.Adagrad(self.parameters(), lr=0.001)

	# TODO: need seperately foward remote batch
	def forward(self, head_index, tail_index, head_neg_index, tail_neg_index, rel_index):
		head = F.embedding(head_index, self.emb, sparse=True)
		tail = F.embedding(tail_index, self.emb, sparse=True)
		head_neg_index = th.cat((head_index, head_neg_index), dim=-1)
		tail_neg_index = th.cat((tail_index, tail_neg_index), dim=-1)
		head_neg = F.embedding(head_neg_index, self.emb, sparse=True)
		tail_neg = F.embedding(tail_neg_index, self.emb, sparse=True)
		head = head.view(self.num_chunk, self.pos_num, self.dim)
		tail = tail.view(self.num_chunk, self.pos_num, self.dim)
		head_neg = head_neg.view(self.num_chunk, self.pos_num + self.neg_num, self.dim)
		tail_neg = tail_neg.view(self.num_chunk, self.pos_num + self.neg_num, self.dim)
		if self.head_operator:
			head_ = self.head_operator(head, rel_index)
		else:
			head_ = head
		if self.tail_operator:
			tail_ = self.tail_operator(tail, rel_index)
		else:
			tail_ = tail
		head_pos_scores, head_neg_scores = self.comparator(head_, tail, tail_neg)
		tail_pos_scores, tail_neg_scores = self.comparator(tail_, head, head_neg)
		head_neg_scores += self.mask
		tail_neg_scores += self.mask
		# head_pos_scores.flatten(0, 1)
		# tail_pos_scores.flatten(0, 1)
		# head_neg_scores.flatten(0, 1)
		# tail_neg_scores.flatten(0, 1)
		# head_pos_scores.unsqueeze(1)
		# tail_pos_scores.unsqueeze(1)
		head_pos_scores = head_pos_scores.view(self.pos_num * self.num_chunk, -1)
		tail_pos_scores = tail_pos_scores.view(self.pos_num * self.num_chunk, -1)
		head_neg_scores = head_neg_scores.view(self.pos_num * self.num_chunk, -1)
		tail_neg_scores = tail_neg_scores.view(self.pos_num * self.num_chunk, -1)
		return head_pos_scores, tail_pos_scores, head_neg_scores, tail_neg_scores
