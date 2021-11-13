from img_gen.convodduni import convodduni
from img_gen.kernel_gen import kernel_gen
import numpy as np


class ImageCreator:
    def __init__(self, bc, nz=1568, ny=255):
        # Define all universal parameters
        self.nz = nz  # Samples in Z direction
        self.ny = ny  # Samples in Y direction
        self.z_size = 29.5e-3  # (m)
        self.y_size = 38e-3  # (m)
        self.incl_z_size = {"min": 1.475e-3, "max": 27e-3}
        self.incl_y_size = {"min": 1.9e-3, "max": 35e-3}
        self.incl_corner_max = {
            "z": self.z_size - 1.05 * self.incl_z_size["min"],
            "y": self.y_size - 1.05 * self.incl_y_size["min"],
        }

        self.dz = self.z_size / self.nz  # Z step (m)
        self.dy = self.y_size / self.ny  # Y step (m)

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

        self.K = kernel_gen(
            self.nz * 4,
            self.ny * 2,
            self.dz,
            self.dy,
            self.h,
            self.lam,
            self.mu,
            self.rho,
        )

        self.leftexcess = round((self.slefty - self.bmlefty) / self.dy)
        self.randomize_incl_mask()

        self.bc = bc
        self.set_bcs()

    def set_bcs(self):
        if self.bc == 0:
            self.wts = np.ones(self.incl_mask.shape)

    def set_incl_bounds(self):
        self.top = np.random.uniform(0, self.incl_corner_max["z"])
        self.left = np.random.uniform(0, self.incl_corner_max["y"])
        self.bot = self.top + np.random.uniform(
            self.incl_z_size["min"], self.incl_z_size["max"]
        )
        self.right = self.left + np.random.uniform(
            self.incl_y_size["min"], self.incl_y_size["max"]
        )

    def randomize_incl_mask(self):
        while True:
            self.set_incl_bounds()
            if self.bot < self.z_size and self.right < self.y_size:
                break
        for limit in ("top", "bot", "left", "right"):
            step = getattr(self, "d" + ("z" if limit in ("top", "bot") else "y"))
            setattr(self, limit, round(getattr(self, limit) / step))
        self.incl_mask = np.zeros((self.nz, self.ny))
        self.incl_mask[self.top : self.bot, self.left : self.right] = 1

    def generate_displacement(self):
        self.randomize_incl_mask()

        def forward_op(x):
            return self.wts * convodduni(x, self.K)

        simdfield = forward_op(self.incl_mask)
        snr = 5
        rand_noise = np.random.normal(size=simdfield.shape)
        noise_level = 10 ** (-snr / 20) * np.sqrt(
            np.sum(np.power(np.abs(simdfield), 2)) / simdfield.size
        )
        simdfield = simdfield + rand_noise * noise_level
        simdfield = np.divide(simdfield, np.amax(simdfield))
        self.simdfield = simdfield
