'''
demo1.py - demonstration code to start Prac Test 3, Tasks 1 & 2

Student Name: 
Student ID  :

Version History:
 - 9/9/24 - original version
 - 11/9/24 - updated as follows: (use ":set number" to show line numbers) 
       line 30 - sets a value in the grid to 10 - stretching the colours
       line 31 - "b" for colour in Tree creation (not numeric on scatter)
       line 33 - swapped xlim/ylim
       line 37 - moved plt.colorbar() to immediately after plt.imshow()
'''
import random
import numpy as np
import matplotlib.pyplot as plt
from canopy import *

def overlay(g, item):
    coords = item.get_topleft()
    size = item.get_size()
    print(coords, size)
    print(f"g[{coords[0]}:{coords[0]}+{size},{coords[1]}:{coords[1]}+{size}] = ({size},{size})")
    g[coords[0]:coords[0]+size,coords[1]:coords[1]+size] = item.get_image()[:,:]


def main():
    xlim = 60
    ylim = 80
    grid = np.zeros((ylim,xlim))
    
    grid[0,0] = 10                # updated 11/9
    t = Tree((20, 30), "b", 100)  # updated 11/9

    #t = Tree((random.randint(20, xlim-20),random.randint(20, ylim-20)), 5, 10)
    print(t)

    plt.imshow(grid)
    plt.colorbar()                # updated 11/9
    plt.scatter(t.get_coord()[0], t.get_coord()[1], c=t.get_colour(), s=t.get_size())
    plt.show()

if __name__ == "__main__":
    main()
