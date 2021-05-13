class ImageCreator
  def __init__(self):
    # Define all universal parameters
    self.nz = 1568 # Samples in Z direction 
    self.ny = 255 # Samples in Y direction 

    self.dz = 29.5E-3/nz # Z step (m)
    self.dy= 38E-3/ny # Y step (m)

    self.rho = 1e3 # Density of sample (kg/m^3)
    self.nu=0.49 # Poisson's Ratio (0.49)
    self.E=10000
    self.h=5E-3
    self.lam=E*nu/(1+nu)/(1-2*nu) # lambda Lame parameter (Pa)
    self.mu=E/2/(1+nu) # mu (shear modulus) Lame parameter (Pa)

    self.sy=100E-3 # full lateral extent of sample in (m)
    self.sz=80E-3 # full axial extent of sample in (m)

    self.dimy=10E-3 # lateral extent of inclusion in (m)
    self.dimz=10E-3 # axial extent of inclusion in (m)
    self.botz=18.171E-3 # bottom surface of inclusion from the top boundary of B-mode AND sample in (m)
    self.topz=8.171E-3 # top surface of inclusion from the top boundary of B-mode AND sample in (m)
    self.bmlefty=15.026E-3 # left surface of inclusion from the left boundary of B-mode in (m)
    self.bmrighty =25.026E-3 # right surface of inclusion from the left boundary of B-mode in (m)
    self.slefty=45E-3 # location of left surface of inclusion from left boundary of sample in (m)
    

  def generate_displacement(self):
    print('testing:', self.dz)
 
  
