"""
canopy.py - module of files for canopy simulations

Student Name: Sean McDougall
Student ID  : 21495140

Version History:
    - 9/11/24 - original version released (temp_basecode.zip)
    - 11/9/24 - extended version released for tasks 3 & 4

"""
import numpy as np


class Item:
    def __init__(self, pos, colour, size, name, thermal_coeff):
        self.pos = pos
        self.colour_code = colour
        self.size = size  # symmetrical, if noy, need height and width
        self.name = name
        self.thermal = thermal_coeff

    def get_image(self):
        s = self.size
        # print(s)
        img = np.ones((s, s)) * self.colour_code  # row_y/col_x
        return img

    def get_coord(self):
        return self.pos

    def get_topleft(self):
        xleft = self.pos[0] - self.size // 2
        ytop = self.pos[1] - self.size // 2
        return (xleft, ytop)

    def get_size(self):
        return self.size

    def get_colour(self):
        return self.colour_code

    def set_size(self, size):
        self.size = size

    def set_colour(self, colour):
        self.colour_code = colour

    def __str__(self):
        return f"{self.name}: {self.pos}"


class Tree(Item):
    def __init__(self, pos, colour, size):
        name = "Tree"
        thermal_coeff = 0.8
        super().__init__(pos, colour, size, name, thermal_coeff)


class Block:
    def __init__(self, size, topleft):
        self.size = size  # size of Block square
        self.topleft = topleft  # (x,y) coord of topleft of Block
        self.items = []  # empty list to hold items

    def get_topleft(self):
        return self.topleft

    def add_item(self, item):
        self.items.append(item)

    def generate_image(self):
        grid = np.zeros(
            (self.size, self.size)
        )  # temporary grid for Block img

        for item in self.items:
            topleft = item.get_topleft()  # topleft coord of item within Block
            img = item.get_image()  # 1D image of item (not 3D rgb)
            cx_start = topleft[0]  # x is columns
            ry_start = topleft[1]  # y is rows
            cx_stop = cx_start + img.shape[1]
            ry_stop = ry_start + img.shape[0]
            grid[ry_start:ry_stop, cx_start:cx_stop] = img[
                :, :
            ]  # overlay item on grid

        print(grid)
        return grid

    def __str__(self):
        return f"Block: {self.topleft}, #items = {len(self.items)}"
