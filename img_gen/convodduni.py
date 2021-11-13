import numpy as np

def convodduni(fn,K):
  nx, nz = fn.shape
  paddedfn = np.zeros((nx*2,nz*2))
  augfn=np.zeros((nx*4,nz*2))

  # hack, leave off one row,column to make even

  paddedfn[0:nx,0:nz] = fn
  # paddedfn(1:nx-1,1:nz-1) = fn(1:nx-1,1:nz-1);

  augfn[0:2*nx,0:2*nz]=-np.flipud(paddedfn)
  augfn[2*nx:4*nx,0:2*nz]=paddedfn
  cv = np.fft.ifft2(np.fft.fft2(augfn)*np.fft.fftshift(K))
  cv = np.real(cv[2*nx:3*nx,0:nz])

  return cv
