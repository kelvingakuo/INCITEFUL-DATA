from keras.preprocessing.image import load_img, img_to_array
from scipy.misc import imsave
import numpy as np

def baseParams(base_img):
	""" Return default image params
	Params:
		base_img - Path to content image
	Returns:
		img_nrows - Rows
		img_ncols - Columns
	"""
	width, height = load_img(base_img).size
	img_nrows = 400
	img_ncols = int(width * img_nrows / height)

	return img_nrows, img_ncols

def preprocessImg(image_path, vgg19, rows, cols):
	""" Return array of loaded image
	Params: 
		image_path - Path to image
		vgg19 - Keras loaded vgg19
		rows - Rows to reshape image to (as computed from content image)
		cols - Columns to reshape image to 
	Returns:
		img - The array
	"""
	img = load_img(image_path, target_size = (rows, cols))
	img = img_to_array(img)
	img = np.expand_dims(img, axis=0)
	img = vgg19.preprocess_input(img)

	return img


def depreprocessImg(x, K, rows, cols):
	""" Reverse preprocessing of image
	Params:
		x - Output tensor of preprocessing
		K - Keras backend
		rows - Image rows
		cols - Image columns
	Returns:
		img - The image
	"""

	if K.image_data_format() == 'channels_first':
		x = x.reshape((3, rows, cols))
		x = x.transpose((1, 2, 0))
	else:
		x = x.reshape((rows, cols, 3))
	# Remove zero-center by mean pixel
	x[:, :, 0] += 103.939
	x[:, :, 1] += 116.779
	x[:, :, 2] += 123.68
	# 'BGR'->'RGB'
	x = x[:, :, ::-1]
	x = np.clip(x, 0, 255).astype('uint8')

	return x