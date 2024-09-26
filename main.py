"""
demo2.py - starter code for Pract Test 3 Tasks 3 & 4

Student Name: 
Student ID  :

Version History:
    - 11/9/24 - original version released
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.widgets import Button

from pathlib import Path
import os
import shutil
from math import ceil
from configparser import ConfigParser

from classes import item_lookup, block_lookup, Water
from utils import generate_image

THERMAL_COL = "hot"
RGB_COL = "terrain"
heat = False
timestep = 1


# holds our matplotlib color bar so we can reset it
cb = ""


def setup():
    config = ConfigParser()
    config.read("config.ini")
    settings = config["SIMULATION_SETTINGS"]
    resolution = settings.get("Resolution", 30)
    cols = settings.get("Columns", 2)
    return int(resolution), int(cols)


def main(blocksize=30, col_count=2):
    blocksize = 30  # defines resolution of heatmap
    blocks = []
    img_path = os.getcwd() + "/output_images"

    blocks_added = 0

    with open("input.csv", "r") as f:
        for line in f.readlines():
            vals = line.rstrip().split(",")
            if vals[1].lower() == "block":
                try:
                    blocks.append(
                        block_lookup[vals[2]](
                            blocksize,
                            (
                                blocksize * ((blocks_added) // col_count),
                                blocksize * (blocks_added % col_count),
                            ),
                        )
                    )
                    blocks_added += 1
                except IndexError:
                    print("No block type found! Skipping...")
            elif vals[1].lower() == "item":
                try:
                    blocks[int(vals[6]) - 1].add_item(
                        item_lookup[vals[2]](
                            (int(vals[4]), int(vals[5])), int(vals[3])
                        )
                    )
                except IndexError as e:
                    print("Error when adding item. Skipping...")
                    print(e)

        # pad out our grid if the user does not supply enough boxes
        while blocks_added % col_count != 0:
            print(blocks_added)
            blocks.append(
                Water(
                    blocksize,
                    (
                        blocksize * ((blocks_added) // col_count),
                        blocksize * (blocks_added % col_count),
                    ),
                ),
            )
            blocks_added += 1

    map_shape = (col_count, ceil(blocks_added / col_count))

    try:
        shutil.rmtree(img_path)
    except FileNotFoundError:
        print("Output image directory not found. Creating...")

    Path(img_path).mkdir(parents=True, exist_ok=True)

    # handler to draw temp grip
    def update_temp_plot():
        with open("output.csv", "w+") as w:
            item_temps = []
            for block in blocks:
                temps = block.get_item_temps()
                # write the headers and extract the temp value
                for temp in temps:
                    w.write(temp["id"] + ",")
                    item_temps.append(temp["temp"])

                    ax[1].plot(
                        temp["temp"],
                        label=temp["id"],
                        color=cm.hot(Normalize(0, 50)(temp["col"])),
                    )
                    ax[1].set_xlabel("Timestep")
                    ax[1].set_ylabel("Temperature")
            # clear new line from headers
            w.write("\n")
            # use the zip function to pair the temps together:
            # de-construct the current temp list thingy
            for item_temp in zip(*item_temps):
                w.write(",".join(str(round(i, 2)) for i in item_temp) + "\n")

    # handler to update grid with button
    def update_grid(e):
        global heat
        cmap = THERMAL_COL if heat else RGB_COL

        for block in blocks:
            block.update_heatmap()
        ax[0].imshow(
            generate_image(blocks, blocksize, map_shape, heat),
            vmin=0,
            vmax=50,
            cmap=cmap,
        )

        update_temp_plot()
        global timestep
        timestep += 1
        fig.savefig(img_path + "/Output" + str(timestep))

        plt.draw()

    def update_heatmode(e):
        global heat
        heat = not heat

        # work out our color paletter
        cmap = THERMAL_COL if heat else RGB_COL

        # draw the image
        img = ax[0].imshow(
            generate_image(blocks, blocksize, map_shape, heat),
            vmin=0,
            vmax=50,
            cmap=cmap,
        )

        # redraw the colorbar
        global cb
        cb.remove()
        cb = plt.colorbar(img)
        plt.draw()

    fig, ax = plt.subplots(1, 2)

    img = ax[0].imshow(
        generate_image(blocks, blocksize, map_shape, heat),
        vmin=0,
        vmax=50,
        cmap=THERMAL_COL if heat else RGB_COL,
    )
    global cb
    cb = plt.colorbar(img)

    update_temp_plot()

    ax[1].legend()

    # draws simulate button
    baxes = fig.add_axes([0.3, 0.01, 0.1, 0.075])
    bnext = Button(baxes, "Simulate")
    bnext.on_clicked(update_grid)

    # draws heatmap toggle button
    caxes = fig.add_axes([0.05, 0.01, 0.15, 0.075])
    c_heat = Button(caxes, "Heatmap?")
    c_heat.on_clicked(update_heatmode)

    fig.subplots_adjust(bottom=-0.2)

    fig.tight_layout()
    fig.savefig(img_path + "/Output1.png")
    plt.show()


if __name__ == "__main__":
    resolution, cols = setup()
    main(resolution, cols)
