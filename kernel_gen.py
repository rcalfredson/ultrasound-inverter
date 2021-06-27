import numpy as np


def kernel_gen(nz, ny, dz, dy, h, lam, mu, rho):
    kzstep = 1 / (nz * dz)
    kystep = 1 / (ny * dy)
    kz, ky = np.meshgrid([1, 2], [1, 2], indexing="ij")
    kpar = np.sqrt(np.power(kz, 2) + np.power(ky, 2))
    kpar = np.maximum(kpar, 0.5 * np.maximum(kzstep, kystep))
    K = np.multiply(
        1 / (mu * np.power(kpar, 2)), 1 - np.exp(-h / 2 * kpar)
    ) - np.multiply(
        np.divide(lam + mu, np.power(kpar, 4) * mu * (lam + 2 * mu)),
        np.multiply(
            1 - np.multiply(0.5 * (2 + h / 2 * kpar), np.exp(-h / 2 * kpar)),
            np.power(kz, 2),
        ),
    )
    K = K*rho
    return K