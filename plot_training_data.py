import argparse
from numpy import load
from matplotlib import pyplot

p = argparse.ArgumentParser(description='visualize training data for the ultrasound inverter')
p.add_argument('path', help='path to the compressed Numpy file to load')
opts = p.parse_args()
# load the dataset
data = load(opts.path)
src_images, tar_images = data['arr_0'], data['arr_1']
print('Loaded: ', src_images.shape, tar_images.shape)
# plot source images
n_samples = 3
for i in range(n_samples):
	pyplot.subplot(2, n_samples, 1 + i)
	pyplot.axis('off')
	pyplot.imshow(src_images[i])
# plot target image
for i in range(n_samples):
	pyplot.subplot(2, n_samples, 1 + n_samples + i)
	pyplot.axis('off')
	pyplot.imshow(tar_images[i].astype('uint8'))
pyplot.show()