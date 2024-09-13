"""
canopy.py - module of files for canopy simulations

Student Name: Sean McDougall
Student ID  : 21495140

Version History:
    - 9/11/24 - original version released (temp_basecode.zip)
    - 11/9/24 - extended version released for tasks 3 & 4

"""
import numpy as np
from utils import sigmoid


class Item:
    def __init__(self, pos, colour, size, name, thermal_coeff, temp):
        self.pos = pos
        self.colour_code = colour
        self.size = size  # symmetrical, if noy, need height and width
        self.name = name
        self.thermal = thermal_coeff
        self.temp = temp

    def get_image(self, heat=False):
        s = self.size
        # print(s)
        img = np.ones((s, s)) * self.temp if heat else self.colour_code
        return img

    def get_shape(self):
        # tuple to allow for future code that may be axb
        return (self.size, self.size)

    def get_topleft(self):
        xleft = self.pos[0] - self.size // 2
        ytop = self.pos[1] - self.size // 2
        return (xleft, ytop)

    def update_temp(self, surrounding_temps):
        # for the temps arround the object, average them by the items thermal_coeff (how well it takes in heat)
        # and its size, mapped between 0 and 1
        temp_arr = [
            temp * self.thermal * sigmoid(self.size)
            for temp in surrounding_temps
        ]

        self.temp = np.average(temp_arr)


class Tree(Item):
    def __init__(self, pos, size):
        name = "Tree"
        thermal_coeff = 0.8
        super().__init__(pos, 37.5, size, name, thermal_coeff, 25)


class House(Item):
    def __init__(self, pos, size):
        name = "House"
        thermal_coeff = 0.3
        super().__init__(pos, 25, size, name, thermal_coeff, 25)


class Block:
    def __init__(self, size, topleft, col, thermal_coeff):
        # size can either be x or y, or just a square
        if size is not tuple:
            size = (size, size)
        self.x = size[0]  # size of Block square
        self.y = size[1]
        self.topleft = topleft  # (x,y) coord of topleft of Block
        self.items = []  # empty list to hold items
        self.color = col
        self.thermal_coeff = thermal_coeff
        self.timesteps = 0
        # empty var
        self.grid = ""

    def get_topleft(self):
        return self.topleft

    def add_item(self, item):
        self.items.append(item)

    def generate_image(self, heat=False):
        # create an array full of the values of our bg colour that we set
        # use heat value of 0 if we are in heatmap mode
        self.grid = np.full((self.x, self.y), 0 if heat else self.color)

        for item in self.items:
            topleft = item.get_topleft()  # topleft coord of item within Block
            (img_x, img_y) = item.get_shape()
            cx_start = topleft[0]  # x is columns
            ry_start = topleft[1]  # y is rows
            cx_stop = cx_start + img_y
            ry_stop = ry_start + img_x

            # update our heat

            if heat:
                # slice out cutout that is 1 pixel wider than our image
                sub_grid = self.grid[ry_start-1:ry_stop+1, cx_start-1:cx_stop+1]
                # temporary indexer
                i = 1
                # check to see if the grid is 0 degrees (needs heat)
                while not np.any(sub_grid):
                    
                    


            
                item.update_temp()
            img = item.get_image(heat)  # 1D image of item (not 3D rgb)

            self.grid[ry_start:ry_stop, cx_start:cx_stop] = img
        return grid


# instantiate our class to create the environment
class Water(Block):
    def __init__(self, size, topleft):
        super().__init__(size, topleft, 0, 1)


class Earth(Block):
    def __init__(self, size, topleft):
        super().__init__(size, topleft, 12.5, 0.8)


class Dirt(Block):
    def __init__(self, size, topleft):
        super().__init__(size, topleft, 40, 0.6)


class Ice(Block):
    def __init__(self, size, topleft):
        super().__init__(size, topleft, 50, 0.2)
