import torch as th
import time
import torch.nn as nn
import torch.multiprocessing as mp
import torch.nn.functional as F

class Model(nn.Module):
        def __init__(self, all_size, rel_size, batch_size, dim):
                super(Model, self).__init__()
                self.all_size = all_size
                self.batch_size = batch_size
                self.dim = dim
                self.emb = nn.Parameter(th.rand(all_size, dim))
                self.head_real = nn.Parameter(th.rand(rel_size, dim // 2))
                self.tail_real = nn.Parameter(th.rand(rel_size, dim // 2))
                self.head_imag = nn.Parameter(th.rand(rel_size, dim // 2))
                self.tail_imag = nn.Parameter(th.rand(rel_size, dim // 2))
                self.mask = th.zeros([batch_size, 2 * batch_size])
                for i in range(batch_size):
                        self.mask[i][i] = -1e9
                self.optim = th.optim.Adagrad(self.parameters(), lr=0.001)
        def side(self, head, pos, neg_index, real, imag):
                #head = F.embedding(head_index, self.emb, sparse=True)
                #pos = F.embedding(pos_index, self.emb, sparse=True)
                neg = F.embedding(neg_index, self.emb, sparse=True)
                head_real = pos[..., :self.dim // 2]
                head_imag = pos[..., self.dim // 2:]
                #neg_real = neg[..., :self.dim // 2]
                #neg_imag = neg[..., self.dim // 2:]
                head2 = th.empty_like(head)
                #pos2 = pos
                head2[..., :self.dim // 2] = head_real * real - head_imag * imag
                head2[..., self.dim // 2:] = head_real * imag + head_imag * real
                #neg2 = th.empty_like(neg)
                #neg2 = neg
                #neg2[..., :self.dim // 2] = neg_real * self.real - neg_imag * self.imag
                #neg2[..., self.dim // 2:] = neg_real * self.imag + neg_imag * self.real
                pos2 = pos.view(1, self.batch_size, self.dim)
                neg2 = neg.view(1, 2 * self.batch_size, self.dim)
                head2 = head2.view(1, self.batch_size, self.dim)
                pos_scores = (head2 * pos2).sum(-1)
                neg_scores = th.bmm(head2, neg2.transpose(-1, -2))
                pos_scores = pos_scores.flatten(0, 1)
                neg_scores = neg_scores.flatten(0, 1)
                pos_scores = pos_scores.unsqueeze(1)
                #scores = th.cat([pos_scores, neg_scores], dim=1)
                return pos_scores, neg_scores
        def forward(self, head_index, tail_index, head_neg, tail_neg, rel_index):
                head = F.embedding(head_index, self.emb, sparse=True)
                tail = F.embedding(tail_index, self.emb, sparse=True)
                head_real = F.embedding(rel_index, self.head_real, sparse=True)
                head_imag = F.embedding(rel_index, self.head_imag, sparse=True)
                tail_real = F.embedding(rel_index, self.tail_real, sparse=True)
                tail_imag = F.embedding(rel_index, self.tail_imag, sparse=True)
                head_scores_pos, head_scores_neg = self.side(head, tail, tail_neg, head_real, head_imag)
                tail_scores_pos, tail_scores_neg = self.side(tail, head, head_neg, tail_real, tail_imag)
                head_scores_neg += self.mask
                tail_scores_neg += self.mask
                return head_scores_pos, head_scores_neg, tail_scores_pos, tail_scores_neg
def train(model, target, rank, head_set, tail_set, rel_set):
        head_neg_index = th.randint(0, model.all_size, [12, 1000])
        tail_neg_index = th.randint(0, model.all_size, [12, 1000])
        head_index = head_set[rank]
        tail_index = tail_set[rank]
        rel_index = rel_set[rank]
        th.set_num_threads(1)
        t0 = time.time()
        for i in range(12):
                #if i % 10 == 0:
                #        print("Rank: " + str(rank) + " " + str(i) + "step")
                model.optim.zero_grad()
                head_pos, head_neg, tail_pos, tail_neg = model(head_index[i], tail_index[i], th.cat((head_index[i], head_neg_index[i]), dim=-1), th.cat((tail_index[i], tail_neg_index[i]), dim=-1), rel_index[i])
                head_scores = th.cat([head_pos, head_neg.logsumexp(dim=1, keepdim=True)], dim=1)
                tail_scores = th.cat([tail_pos, tail_neg.logsumexp(dim=1, keepdim=True)], dim=1)
                #target = th.cat([th.ones([1]), th.zeros([1000])]).expand(1000, -1)
                loss = F.cross_entropy(head_scores, target) + F.cross_entropy(tail_scores, target)
                #loss = th.mean(scores)
                loss.backward()
                model.optim.step()
        t1 = time.time()
        print("Rank: " + str(rank) + " " + str(t1 - t0))
def load(file_name):
        file = open(file_name)
        head_index = th.zeros([16, 12, 1000], dtype=th.long)
        tail_index = th.zeros([16, 12, 1000], dtype=th.long)
        rel_index = th.zeros([16, 12, 1000], dtype=th.long)
        #count = 192000
        for i in range(16):
                for j in range(12):
                        for k in range(1000):
                                line = file.readline()
                                src, dst, rel = line.split(' ')
                                head_index[i][j][k] = int(src)
                                tail_index[i][j][k] = int(dst)
                                rel_index[i][j][k] = int(rel)

        file.close()
        return head_index, tail_index, rel_index


#th.set_num_threads(16)
num_entity = 1305371
num_process = 16
num_edge = 200000
model = Model(num_entity, 14824, 1000, 400)
model.share_memory()

#target = th.cat([th.ones([2], dtype=th.long), th.zeros([2000], dtype=th.long)]).unsqueeze(0).expand(1000, -1)
target = th.zeros([1000], dtype=th.long)
t0 = time.time()
head_set, tail_set, rel_set = load("part0.txt")
t1 = time.time()
print("Load: " + str(t1 - t0))
processes = []
for rank in range(num_process):
        p = mp.Process(target=train, args=(model, target, rank, head_set, tail_set, rel_set))
        p.start()
        processes.append(p)
for p in processes:
        p.join()


