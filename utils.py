import numpy as np
import math


# used to generate our image for the first time
def generate_image(b, s, mshape, heat=False):
    # create our grid - empty array of 0s
    grid = np.zeros((mshape[0] * s, mshape[1] * s))
    # loop through each block object
    for block in b:
        # get top left corner
        (
            cx_start,
            ry_start,
        ) = block.get_topleft()
        # update grid to represent whats expected in that corner
        grid[
            ry_start : ry_start + s, cx_start : cx_start + s
        ] = block.generate_grid(heat)
    return grid


# maps a size value (0~n) between 1 and 0
# used to make the dial down the impact of the thermal coeff.
def sigmoid(x):
    return 1 / (1 + math.exp(-10 / x))
