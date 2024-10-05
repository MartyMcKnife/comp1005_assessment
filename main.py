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

# ignore warnings
import warnings

warnings.filterwarnings("ignore")

THERMAL_COL = "hot"
RGB_COL = "terrain"
timestep = 1
sweeps = 1
sweep_handler = ""


# read our configuration files
def setup():
    config = ConfigParser()
    config.read("config.ini")
    settings = config["SIMULATION_SETTINGS"]
    resolution = settings.get("Resolution", 30)
    cols = settings.get("Rows", 2)
    sweep = settings.getboolean("Parameter_sweep", False)
    return int(resolution), int(cols), bool(sweep)


def main(blocksize=30, col_count=2, sweep=False):
    blocksize = 30  # defines resolution of heatmap
    blocks = []
    img_path = os.getcwd() + "/output_images"

    # count how many blocks we have
    # honestly could just call len() everytime but this is ever so slightly more memory efficient
    blocks_added = 0

    with open("input.csv", "r") as f:
        # read each line in csv file and parse it
        for line in f.readlines():
            vals = line.rstrip().split(",")
            if vals[1].lower() == "block":
                try:
                    # add our block
                    blocks.append(
                        # find the class from the lookup table
                        block_lookup[vals[2]](
                            blocksize,
                            (
                                # our row cycles between 0 -> 1 0 -> 1 or whatever our col_count - 1 is
                                # we can take the floor of our blocks_added divide by the column count to find this number
                                blocksize * ((blocks_added) // col_count),
                                # the column increases by one for every n blocks, where n is the col_count
                                # can just take the modulo of this
                                blocksize * (blocks_added % col_count),
                            ),
                        )
                    )
                    blocks_added += 1
                # handle undefined block type
                except KeyError:
                    print(f"No block type found for {vals[2]}! Skipping...")
            elif vals[1].lower() == "item":
                try:
                    # really unelegant code but just adds the item to the block using the user defined values
                    blocks[int(vals[6]) - 1].add_item(
                        item_lookup[vals[2]](
                            (int(vals[4]), int(vals[5])), int(vals[3])
                        )
                    )
                # handle index errror - maybe the user typed the wrong block id?
                except IndexError as e:
                    print("Error when adding item. Skipping...")
                    print(e)
                except KeyError:
                    print(f"No item type found for {vals[2]}! Skipping...")

        # pad out our grid if the user does not supply enough boxes
        # uses the same positioning algorithm seen above
        while blocks_added % col_count != 0:
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

    # calculate our map shape
    map_shape = (col_count, ceil(blocks_added / col_count))

    # clear our output_images folder / create it if it doesn't exist
    try:
        shutil.rmtree(img_path)
    except FileNotFoundError:
        print("Output image directory not found. Creating...")

    Path(img_path).mkdir(parents=True, exist_ok=True)

    # handler to draw temp grid
    def update_temp_plot():
        global sweeps
        with open(f"output_{sweeps}.csv", "w+") as w:
            item_temps = []
            for block in blocks:
                temps = block.get_item_temps()
                # write the headers and extract the temp value
                for temp in temps:
                    w.write(temp["id"] + ",")
                    item_temps.append(temp["temp"])
                    ax[2].plot(
                        temp["temp"],
                        label=temp["id"],
                        color=cm.hot(Normalize(0, 50)(temp["col"])),
                    )
                    ax[2].set_xlabel("Timestep")
                    ax[2].set_ylabel("Temperature")
            # clear new line from headers
            w.write("\n")
            # use the zip function to pair the temps together:
            # de-construct the current temp list thingy
            for item_temp in zip(*item_temps):
                w.write(",".join(str(round(i, 2)) for i in item_temp) + "\n")

    # handler to update grid with button
    def update_grid(e):
        for block in blocks:
            block.update_heatmap()
        ax[1].imshow(
            generate_image(blocks, blocksize, map_shape, True),
            vmin=0,
            vmax=100,
            cmap=THERMAL_COL,
        )

        update_temp_plot()
        global timestep, sweeps
        timestep += 1
        fig.savefig(
            img_path
            + "/Output_Sweep"
            + str(sweeps)
            + "Timestep"
            + str(timestep)
        )

        plt.draw()

    def update_sweep_steps(e):
        for block in blocks:
            block.update_items_start_temp()

        ax[1].imshow(
            generate_image(blocks, blocksize, map_shape, True),
            vmin=0,
            vmax=100,
            cmap=THERMAL_COL,
        )

        global timestep, sweeps, sweep_handler
        sweeps += 1
        timestep = 1

        sweep_handler.set_text(f"Sweeps: {sweeps}")

        # reset out temp plot
        ax[2].cla()
        update_temp_plot()
        ax[2].legend()

        fig.savefig(
            img_path
            + "/Output_Sweep"
            + str(sweeps)
            + "Timestep"
            + str(timestep)
        )

        plt.draw()

    fig, ax = plt.subplots(1, 3)

    rgb = ax[0].imshow(
        generate_image(blocks, blocksize, map_shape, False),
        vmin=0,
        vmax=50,
        cmap=RGB_COL,
    )
    # fractions taken from https://stackoverflow.com/questions/18195758/set-matplotlib-colorbar-size-to-match-graph
    plt.colorbar(rgb, fraction=0.046, pad=0.04)

    heat = ax[1].imshow(
        generate_image(blocks, blocksize, map_shape, True),
        vmin=0,
        vmax=100,
        cmap=THERMAL_COL,
    )
    # as above
    plt.colorbar(heat, fraction=0.046, pad=0.04)

    update_temp_plot()

    ax[2].legend()
    global sweep_handler
    sweep_handler = plt.figtext(0.45, 0.01, f"Sweeps: {sweeps}")

    # draws simulate button
    baxes = fig.add_axes([0.01, 0, 0.1, 0.075])
    bnext = Button(baxes, "Simulate")
    bnext.on_clicked(update_grid)

    # draw next sweep button
    if sweep:
        caxes = fig.add_axes([0.2, 0, 0.1, 0.075])
        cnext = Button(caxes, "Sweep")
        cnext.on_clicked(update_sweep_steps)

    fig.set_figwidth(10)

    fig.tight_layout()
    fig.savefig(
        img_path + "/Output_Sweep" + str(sweeps) + "Timestep" + str(timestep)
    )
    plt.show()


if __name__ == "__main__":
    resolution, cols, sweep = setup()
    main(resolution, cols, sweep)
