# file: tmeasure.py
#
# image reconstruction from line measurements (tomography via least-squares)
#
# this is a pyython script that is used to produce the data in tomodata.py
import numpy as np
import matplotlib.pyplot as plt

from line_pixel_length import line_pixel_length

n_pixels = 30   # image size is n_pixels by n_pixels
N_d = 35        # number of parallel lines for each angle
N_theta = 35    # number of angles (equally spaced from 0 to pi)
N = N_d * N_theta  # total number of lines (i.e. number of measurements)

sigma = 0.7   # noise level (standard deviation for normal dist.)

X =  # ...the image goes here...

# display the original image
plt.imshow(X, cmap="gray", vmin=0, vmax=255)
plt.show()

# write the matrix X (the original image) as one big column vector
# (first column of X goes first, then 2nd column, etc.)
x = X.reshape((1, n_pixel**2))


y = np.zeros(N,1)            # will store the N measurements
lines_d = np.zeros(N,1)      # will store the position of each line
lines_theta = np.zeros(N,1)  # will store the angle of each line

i = 1
for i_theta in range(N_theta):
    for i_d in range(N_d):
        # equally spaced parallel lines, distance from first to
        # last is about 1.4*n_pixels (to ensure coverage of whole
        # image when theta=pi/4)
        lines_d(i) = 0.7 * n_pixels * (i_d - (N_d - 1)/2) / (N_d/2)
        # equally spaced angles from 0 to pi
        lines_theta(i) = pi * itheta/N_theta

        # L is a matrix of the same size as the image
        # with entries giving the length of the line over each pixel
        L = line_pixel_length(lines_d(i),lines_theta(i),n_pixels)
        # make matrix L into a column vector, like X
        l = L.reshape((1, n_pixels**2))

        # "line integral" of line over image,
        # i.e., the intensity of each pixel is multiplied by the
        # length of line over that pixel, and then add for all pixels
        # a random, Gaussian noise, with std sigma is added to the
        # measurement       
        y(i) = l.T @ x + np.random.normal(0, 0.5)
        
        i += 1
