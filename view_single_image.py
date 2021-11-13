from image_creator import ImageCreator
import matplotlib.pyplot as plt

def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

ic = ImageCreator(bc=0)
ic.generate_displacement()
plt.figure()
plt.imshow(ic.incl_mask)
forceAspect(plt.gca())
plt.title('Inclusion mask')
plt.figure()
print('sim dfield shape:', ic.simdfield.shape)
plt.imshow(ic.simdfield)
forceAspect(plt.gca())
plt.title('Displacement field')
plt.show()
