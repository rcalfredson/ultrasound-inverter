import argparse
import numpy as np
import os
from img_gen.image_creator import ImageCreator
from matplotlib import pyplot as plt


def forceAspect(ax, aspect=1):
    im = ax.get_images()
    extent = im[0].get_extent()
    ax.set_aspect(abs((extent[1] - extent[0]) / (extent[3] - extent[2])) / aspect)


p = argparse.ArgumentParser(
    description="generate training data for Pix2Pix GAN ultrasound image processor"
)
p.add_argument("ht", help="height of images to generate", type=int)
p.add_argument("wd", help="width of images to generate", type=int)
p.add_argument("n", help="number of images to generate", type=int)
p.add_argument('dest', help='folder to which to write results')
p.add_argument(
    "--plot", help="show inclusion and displacement field as they are generated"
)


opts = p.parse_args()
ic = ImageCreator(bc=0, nz=opts.ht, ny=opts.wd)

def load_images():
  src_list, tar_list = list(), list()
  for _ in range(opts.n):
      ic.generate_displacement()
      if opts.plot:
        plt.figure()
        plt.imshow(ic.incl_mask)
        forceAspect(plt.gca())
        plt.title("Inclusion mask")
        plt.figure()
        plt.imshow(ic.simdfield)
        forceAspect(plt.gca())
        plt.title("Displacement field")
        plt.show()
        input()
      src_list.append(ic.simdfield)
      tar_list.append(ic.incl_mask)
  return [np.asarray(src_list), np.asarray(tar_list)]

[src_images, tar_images] = load_images()
# save as compressed Numpy array
np.savez_compressed(os.path.join(opts.dest, 'ultrasound_trn_data.npz'), src_images, tar_images)
