import numpy as np
from kernel_gen import kernel_gen


class ImageCreator:
    def __init__(self, bc):
        # Define all universal parameters
        self.nz = 1568  # Samples in Z direction
        self.ny = 255  # Samples in Y direction

        self.dz = 29.5e-3 / self.nz  # Z step (m)
        self.dy = 38e-3 / self.ny  # Y step (m)

        self.rho = 1e3  # Density of sample (kg/m^3)
        self.nu = 0.49  # Poisson's Ratio (0.49)
        self.E = 10000
        self.h = 5e-3
        self.lam = (
            self.E * self.nu / (1 + self.nu) / (1 - 2 * self.nu)
        )  # lambda Lame parameter (Pa)
        self.mu = self.E / 2 / (1 + self.nu)  # mu (shear modulus) Lame parameter (Pa)

        self.sy = 100e-3  # full lateral extent of sample in (m)
        self.sz = 80e-3  # full axial extent of sample in (m)

        self.dimy = 10e-3  # lateral extent of inclusion in (m)
        self.dimz = 10e-3  # axial extent of inclusion in (m)
        self.botz = 18.171e-3  # bottom surface of inclusion from the top boundary of B-mode AND sample in (m)
        self.topz = 8.171e-3  # top surface of inclusion from the top boundary of B-mode AND sample in (m)
        self.bmlefty = 15.026e-3  # left surface of inclusion from the left boundary of B-mode in (m)
        self.bmrighty = 25.026e-3  # right surface of inclusion from the left boundary of B-mode in (m)
        self.slefty = 45e-3  # location of left surface of inclusion from left boundary of sample in (m)

        self.leftexcess = round((self.slefty - self.bmlefty) / self.dy)
        self.top = round(self.topz / self.dz)
        self.bot = round(self.botz / self.dz)
        self.left = round(self.bmlefty / self.dy)
        self.right = round(self.bmrighty / self.dy)
        self.incl_mask = np.zeros((self.nz, self.ny))
        self.incl_mask[self.top : self.bot, self.left : self.right] = 1

        self.bc = bc
        self.set_bcs()

    def set_bcs(self):
        if self.bc == 0:
            self.wts = np.ones(self.incl_mask.shape)

    def generate_displacement(self):
        print("testing:", self.dz)
        print("left excess:", self.leftexcess)
        K = kernel_gen(
            self.nz * 4,
            self.ny * 2,
            self.dz,
            self.dy,
            self.h,
            self.lam,
            self.mu,
            self.rho,
        )

