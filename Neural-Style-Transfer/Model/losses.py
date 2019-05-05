from keras import backend as K
from keras.applications import vgg19
import numpy as np


def loadModel(inputs):
	""" Return loaded Vgg model
	Params:
		inputs - Input tensor
	Returns:
		model - Loaded Vgg model
	"""

	model = vgg19.VGG19(input_tensor = inputs, weights = 'imagenet', include_top = False)

	return model


def getLayers(model):
	""" Return a dict of model layers
	Params:
		model - The pretrained model
	Returns:
		layerDesc - Description of the layers
	"""

	layerDesc = dict([(layer.name, layer.output) for layer in model.layers])

	return layerDesc


def gramMatrix(x):
	""" Return gram matrix of a tensor
	Params:
		x - Tensor
	Returns:
		gram - The gram matrix
	"""
	if K.image_data_format() == 'channels_first':
		features = K.batch_flatten(x)
	else:
		features = K.batch_flatten(K.permute_dimensions(x, (2, 0, 1)))

	gram = K.dot(features, K.transpose(features))

	return gram


def styleLoss(styleTensor, genTensor, rows, cols):
	""" Return style loss of tensors
	Params:
		styleTensor - Tensor of style image
		genTensor - Tensor of combined images i.e. style, content, generated
		rows - Image rows
		cols - Image cols
	Returns: 
		theStyleLoss - The style loss
	"""
	S = gramMatrix(styleTensor)
	C = gramMatrix(genTensor)
	channels = 3
	size = rows * cols

	theStyleLoss = K.sum(K.square(S - C)) / (4.0 * (channels ** 2) * (size ** 2))

	return theStyleLoss


def contentLoss(contentTensor, genTensor):
	""" Return content loss of tensors
	Params:
		contentTensor - Tensor of content image
		genTensor - Tensor of combined images i.e. style, content, generated
	Returns: 
		theContentLoss - The content loss
	"""

	theContentLoss = K.sum(K.square(genTensor - contentTensor))

	return theContentLoss


def variationLoss(x, rows, cols):
	""" For a clearer output
	"""
	if K.image_data_format() == 'channels_first':
		a = K.square(x[:, :, :rows - 1, :cols - 1] - x[:, :, 1:, :cols - 1])
		b = K.square(x[:, :, :rows - 1, :cols - 1] - x[:, :, :rows - 1, 1:])
	else:
		a = K.square(x[:, :rows - 1, :cols - 1, :] - x[:, 1:, :cols - 1, :])
		b = K.square(x[:, :rows - 1, :cols - 1, :] - x[:, :rows - 1, 1:, :])
		
	varLoss = K.sum(K.pow(a + b, 1.25))

	return varLoss



def lossAndGrads(x, rows, cols, funcedOutputs):
	if K.image_data_format() == 'channels_first':
		x = x.reshape((1, 3, rows, cols))
	else:
		x = x.reshape((1, rows, cols, 3))

	outs = funcedOutputs([x])
	lossVals = outs[0]

	if len(outs[1:]) == 1:
		gradVals = outs[1].flatten().astype('float64')
	else:
		gradVals = np.array(outs[1:]).flatten().astype('float64')

	return lossVals, gradVals






class Evaluator(object):
	""" Required to run the Scipy optimiser
	"""

	def __init__(self, rows, cols, funced):
		self.lossVals = None
		self.gradsVals = None

		self.rows = rows
		self.cols = cols
		self.funced = funced

	def loss(self, x):
		lossVals, gradVals = lossAndGrads(x, self.rows, self.cols, self.funced)
		self.lossVals = lossVals
		self.gradVals = gradVals

		return self.lossVals

	def grads(self, x):
		gradVals = np.copy(self.gradVals)
		self.lossVals = None
		self.gradVals = None

		return gradVals
