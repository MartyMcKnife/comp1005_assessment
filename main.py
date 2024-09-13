"""
demo2.py - starter code for Pract Test 3 Tasks 3 & 4

Student Name: 
Student ID  :

Version History:
    - 11/9/24 - original version released
"""
import matplotlib.pyplot as plt

from canopy import Tree, House, Earth, Water
from utils import generate_image

THERMAL_COL = "hot"
RGB_COL = "terrain"


def main():
    # there are many ways to set up the assignment, this is an example
    blocksize = 20  # each block is a 20x20 square
    map_shape = (2, 1)  # 2 rows of blocks, 1 column
    blocks = []

    blocks.append(Water(blocksize, (0, 0)))
    blocks.append(Earth(blocksize, (0, blocksize)))

    blocks[0].add_item(Tree((10, 10), 3))
    blocks[0].add_item(Tree((5, 15), 3))
    blocks[1].add_item(House((12, 6), 5))

    plt.imshow(
        generate_image(blocks, blocksize, map_shape, heat=True),
        vmin=0,
        vmax=50,
        cmap=THERMAL_COL,
    )
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    main()
