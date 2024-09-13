import numpy as np
import math


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
        ] = block.generate_image(heat)
    return grid


# maps a size value (0~n) between 1 and 0
# used to make the size of the object play a part in how quick it heats up
def sigmoid(x):
    return 1 / (1 + math.exp(-2 / x))
