import glob
from keras.applications import vgg19
from keras.preprocessing.image import save_img
from keras import backend as K
import logging
import os
from scipy.optimize import fmin_l_bfgs_b


# My modules...
from utils.log_config import logger

from preprocessing import preprocessImg
from preprocessing import depreprocessImg
from preprocessing import baseParams

from losses import loadModel
from losses import getLayers
from losses import styleLoss
from losses import contentLoss
from losses import variationLoss

from losses import Evaluator

def main(contentImg, styleImg, saveImgPath):
	variationWeight = 1.0
	styleWeight = 1.5
	contentWeight = 0.75
	nRows, nCols = baseParams(contentImg)

	contentImage = K.variable(preprocessImg(contentImg, vgg19, nRows, nCols))
	styleImage = K.variable(preprocessImg(styleImg, vgg19, nRows, nCols))

	if K.image_data_format() == 'channels_first':
		genImage = K.placeholder((1, 3, nRows, nCols))
	else:
		genImage = K.placeholder((1, nRows, nCols, 3))

	inTensor = K.concatenate([contentImage, styleImage, genImage], axis=0)

	model = loadModel(inTensor)
	layerDesc = getLayers(model)

	totalLoss = K.variable(0.0)
	contentLayers = layerDesc['block5_conv2']
	contentFeatures = contentLayers[0, :, :, :]
	genFeatures = contentLayers[2, :, :, :]
	totalLoss += contentWeight * contentLoss(contentFeatures, genFeatures)

	styleLayers = ['block1_conv1', 'block2_conv1','block3_conv1', 'block4_conv1','block5_conv1']

	for layer in styleLayers:
		layerFeatures = layerDesc[layer]

		styleFeatures = layerFeatures[1, :, :, :]
		genFeatures = layerFeatures[2, :, :, :]
		theStLoss = styleLoss(styleFeatures, genFeatures, nRows, nCols)

		totalLoss += (styleWeight / len(styleLayers)) * theStLoss

	totalLoss += variationWeight * variationLoss(genImage, nRows, nCols)

	grads = K.gradients(totalLoss, genImage)
	outputs = [totalLoss]

	if(isinstance(grads, (list, tuple))):
		outputs += grads
	else:
		outputs.append(grads)

	funcedOutputs = K.function([genImage], outputs)

	evaluator = Evaluator(nRows, nCols, funcedOutputs)


	x = preprocessImg(contentImg, vgg19, nRows, nCols)
	for i in range(20):
		logger.debug('ITERATION: {}'.format(i))
		x, _, _ = fmin_l_bfgs_b(evaluator.loss, x.flatten(), fprime = evaluator.grads, maxfun = 30)
	
		img = depreprocessImg(x.copy(), K, nRows, nCols)
		fname = saveImgPath + '/generated_img_at_iteration_%d.png' % i
		save_img(fname, img)

		logger.info('Saved iteration: {} as {}'.format(i, fname))



if __name__ == "__main__":
	logger.setLevel(logging.DEBUG)

	content_path = 'content_image.jpg'

	styles = glob.glob('styles/*.jpg')
	for style in styles:
		style_path = style
		logger.info('Styling content image with: {}'.format(style_path))


		logger.info('Creating iters folder for style')
		base = os.path.basename(style_path)
		iters = os.path.splitext(base)[0]
		save_path = 'gen_imgs/'+iters
		os.mkdir(save_path)
		logger.info('Created iters folder: {}'.format(save_path))


		main(content_path, style_path, save_path)


