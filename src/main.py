from model.model import Model
from config.config import ModelConfig

if __name__ == '__main__':
	config = ModelConfig(None, None, None, 1, 1, 1, 1, 1, 1, 'Adagrad')
	model = Model(config)
