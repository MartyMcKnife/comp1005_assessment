'''
demo2.py - starter code for Pract Test 3 Tasks 3 & 4

Student Name: 
Student ID  :

Version History:
    - 11/9/24 - original version released
'''
import random
import numpy as np
import matplotlib.pyplot as plt

from canopy import *

def generate_image(b, s, mshape):
    grid = np.zeros((mshape[0]*s, mshape[1]*s))
    print(grid)
    for block in b:
        (cx_start,ry_start) = block.get_topleft() # x,y mapping to column,row
        print(block, cx_start, ry_start)
        grid[ry_start:ry_start+s,cx_start:cx_start+s] = block.generate_image()[:,:]
    return grid

def main():
    # there are many ways to set up the assignment, this is an example
    blocksize = 20       # each block is a 20x20 square
    map_shape = (2,1)    # 2 rows of blocks, 1 column
    blocks = []

    blocks.append(Block(blocksize, (0,0)))
    blocks.append(Block(blocksize, (0,blocksize)))

    blocks[0].add_item(Tree((10,10), 3, 3))
    blocks[0].add_item(Tree((5,15), 3, 3))
    blocks[1].add_item(Tree((12,6), 5, 4))

    plt.imshow(generate_image(blocks, blocksize, map_shape), vmin=0, vmax=10)
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    main()
