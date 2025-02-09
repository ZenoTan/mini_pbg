from network import *
from config import *
import torch.multiprocessing as mp

def server_proc(config):
	server = KGServer(config)

if __name__ == '__main__':
	procs = []
	client_namebook = {0: '127.0.0.1:55501'}
	server_namebook = {0:'127.0.0.1:55500'}
	for proc in range(1):
		config = KVConfig(proc, server_namebook[proc], client_namebook)
		p = mp.Process(target=server_proc, args=(config, ))
		p.start()
		procs.append(p)
	for p in procs:
		p.join()
