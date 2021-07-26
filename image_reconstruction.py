# Least Square Estimation from line integral measurements.
# y_j = Σ(1,n^2) l_ij*x_i + v_j
# where v is small measurement noise.
# y_j's are known
# l_ij's can be found using slope and distance from center
# See: line_pixel_length.py

from tomodata import n_pixels, N, y, lines_d, lines_theta
from line_pixel_length import line_pixel_length

import numpy as np
import matplotlib.pyplot as plt

M = np.zeros((N, n_pixels ** 2))
for meas in range(N):
    L = line_pixel_length(lines_d[meas], lines_theta[meas], n_pixels)
    M[meas, :] = L.reshape((1, n_pixels ** 2))

y = np.array(y).reshape((N, 1))

# Least Squares Solution
x = np.linalg.inv(M.T @ M) @ M.T @ y
X = x.reshape((n_pixels, n_pixels))
plt.imshow(X, cmap="gray", vmin=0, vmax=255)
plt.show()
