# image reconstruction from line measurements (tomography via least-squares)
#
# given a grid of n by n square pixels, and a line over that grid,
# this function computes the length of line that goes over each pixel
#
# INPUTS
# d:     displacement of line,
#        distance of line from center of image,
#        measured in pixel lengths (and orthogonally to line)
# theta: angle of line,
#        measured in radians from x-axis
# n:     image size is n by n
#
# OUTPUTS
# L:     matrix of size n by n (same as image),
#        length of the line over each pixel (most entries are zero)
#
# expects an angle theta in [0,pi]
# (but will work at least for angles in [-pi/4,pi])
import numpy as np
from math import pi, cos, sin, ceil, sqrt


pi = np.pi
print_to_screen = False


def line_pixel_length(d, theta, n):
    # Convert line to lie between [0, pi/4]

    # for angle in [pi/4,3*pi/4],
    # flip along diagonal (transpose) and call recursively
    if theta > pi / 4 and theta < 3 / 4 * pi:
        L = line_pixel_length(d, pi / 2 - theta, n).T
        return L

    # for angle in [3*pi/4,pi],
    # redefine line to go in opposite direction
    if theta > pi / 2:
        d = -d
        theta = theta - pi

    # for angle in [-pi/4,0],
    # flip along x-axis (up/down) and call recursively
    if theta < 0:
        L = np.flipud(line_pixel_length(-d, -theta, n))
        return L

    if theta > pi / 2 or theta < 0:
        print("invalid angle")
        return

    L = np.zeros((n, n))

    ct = np.cos(theta)
    st = np.sin(theta)

    # Find any point on line
    # Here it is closest point to center on line
    x0 = n / 2 - d * st
    y0 = n / 2 + d * ct

    # Find y intercept
    y = y0 - x0 * st / ct
    jy = ceil(y)
    dy = (y + n) % 1

    for jx in range(n):
        dynext = dy + st / ct
        # if slope is small, it fits in one box.
        if dynext < 1:
            if jy >= 1 and jy <= n:
                L[n - jy, jx] = 1 / ct
            dy = dynext
        # else it fits in 2 boxes.
        else:
            if jy >= 1 and jy <= n:
                L[n - jy, jx] = (1 - dy) / st
            if jy + 1 >= 1 and jy + 1 <= n:
                L[n - (jy + 1), jx] = (dynext - 1) / st
            dy = dynext - 1
            jy = jy + 1
        print_matrix(L, n)
    return L


def print_matrix(M, n):
    if print_to_screen == True:
        for i in range(n):
            for j in range(n):
                print(np.round(M[i, j], decimals=2), end=" ")
            print()
        print()


if __name__ == "__main__":
    print_to_screen = True
    L = line_pixel_length(1 / sqrt(2), pi / 8, 8)
    print_matrix(L, 8)
