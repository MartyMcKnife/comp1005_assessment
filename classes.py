"""
canopy.py - module of files for canopy simulations

Student Name: Sean McDougall
Student ID  : 21495140

Version History:
    - 9/11/24 - original version released (temp_basecode.zip)
    - 11/9/24 - extended version released for tasks 3 & 4

"""

import numpy as np
from random import uniform


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

    def check_inside(self, y, x):
        x_top, y_top = self.get_topleft()
        x_len, y_len = self.get_shape()

        # not very elegant way to check if item is inside bounding box
        return x_top <= x and x <= x_top + x_len and y_top <= y and y <= y_top + y_len


class Tree(Item):
    def __init__(self, pos, size):
        name = "Tree"
        thermal_coeff = 0.8
        super().__init__(pos, 37.5, size, name, thermal_coeff, 25)


class Rock(Item):
    def __init__(self, pos, size):
        name = "Rock"
        thermal_coeff = 0.4
        super().__init__(pos, 45, size, name, thermal_coeff, 25)


class House(Item):
    def __init__(self, pos, size):
        name = "House"
        thermal_coeff = 0.3
        super().__init__(pos, 25, size, name, thermal_coeff, 25)


class Person(Item):
    def __init__(self, pos, size):
        name = "Person"
        thermal_coeff = 0.1
        super().__init__(pos, 22, size, name, thermal_coeff, 25)


class Fire(Item):
    def __init__(self, pos, size):
        name = "Fire"
        thermal_coeff = 1
        super().__init__(pos, 22, size, name, thermal_coeff, 25)


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
        self.grid_gen = False
        self.heatmap = ""
        self.item_temps = []

    def get_topleft(self):
        return self.topleft

    def add_item(self, item):
        self.items.append(item)

    def generate_item(self, item):
        topleft = item.get_topleft()  # topleft coord of item within Block
        (img_x, img_y) = item.get_shape()
        cx_start = topleft[0]  # x is columns
        ry_start = topleft[1]  # y is rows
        cx_stop = cx_start + img_y
        ry_stop = ry_start + img_x

        img_col = item.get_image()  # 1D image of item (not 3D rgb)
        img_heat = item.get_image(True)

        self.grid[ry_start:ry_stop, cx_start:cx_stop] = img_col
        self.heatmap[ry_start:ry_stop, cx_start:cx_stop] = img_heat

    def generate_grid(self, heat=False):
        # only generate our grid if we don't have it
        # if we don't have a heatmap, create one
        if not self.grid_gen:
            # create an array full of the values of our bg colour that we set
            # create both a heatmap and colour map
            self.grid = np.full((self.x, self.y), self.color)
            self.heatmap = np.full((self.x, self.y), 0)

            for item in self.items:
                self.generate_item(item)

            self.grid_gen = True

        # return our grid only if we don't want the heatmap
        return self.heatmap if heat else self.grid

    def update_heatmap(self):
        # create temporary array to hold our updated values
        temp_grid = np.zeros(self.grid.shape)
        # loop through every element in the grid
        for y, x in np.ndindex(self.grid.shape):
            y_max, x_max = self.grid.shape
            # get our surrounding temps
            # if the temp is out of bounds (on an edge), we ignore the value
            top_temp = (self.heatmap[y - 1, x] if y > 0 else 0,)
            bottom_temp = (self.heatmap[y + 1, x] if y < y_max - 1 else 0,)
            left_temp = (self.heatmap[y, x - 1] if x > 0 else 0,)
            right_temp = (self.heatmap[y, x + 1] if x < x_max - 1 else 0,)

            # check if this cell is inside an item
            # if it is, take our items thermal_coeff into account
            item_thermal_coeff = 1
            for item in self.items:
                if item.check_inside(y, x):
                    item_thermal_coeff = self.thermal_coeff

            # update the cells temp based on the average of the surrounding squares, and the cells thermal coefficient
            temps = [top_temp, bottom_temp, left_temp, right_temp]
            # we divide our cell's thermal coefficient by the items thermal coeff to get a nice ratio between how much heat we gain vs loss
            # we also multiply by a slight amount of noise
            temp_grid[y, x] = (
                np.average(temps)
                * (self.thermal_coeff / item_thermal_coeff)
                * uniform(0.8, 1)
            )
        self.heatmap = temp_grid

    def get_item_temps(self):
        for idx, item in enumerate(self.items):
            topleft = item.get_topleft()
            (img_x, img_y) = item.get_shape()
            cx_start = topleft[0]
            ry_start = topleft[1]
            cx_stop = cx_start + img_y
            ry_stop = ry_start + img_x

            avg_temp = np.average(self.heatmap[ry_start:ry_stop, cx_start:cx_stop])
            # loop through and check to see if the temp has already been added
            updated = False
            for item_temp in self.item_temps:
                # we have had temperature before; update
                if item_temp["id"] == item.name + str(idx):
                    item_temp["temp"].append(avg_temp)
                    updated = True
            # if we don't update, append
            if not updated:
                self.item_temps.append(
                    {
                        "name": item.name,
                        "temp": [avg_temp],
                        "id": item.name + str(idx),
                        "col": item.colour_code,
                    }
                )

        return self.item_temps


# instantiate our class to create the environment
class Water(Block):
    def __init__(self, size, topleft):
        super().__init__(size, topleft, 0, 0.4)


class Earth(Block):
    def __init__(self, size, topleft):
        super().__init__(size, topleft, 12.5, 0.9)


class Dirt(Block):
    def __init__(self, size, topleft):
        super().__init__(size, topleft, 40, 0.6)


class Ice(Block):
    def __init__(self, size, topleft):
        super().__init__(size, topleft, 50, 0.3)
