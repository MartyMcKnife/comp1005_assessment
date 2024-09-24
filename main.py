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

from classes import Tree, House, Earth, Water
from utils import generate_image

THERMAL_COL = "hot"
RGB_COL = "terrain"
heat = False
# holds our matplotlib color bar so we can reset it
cb = ""


def main():
    blocksize = 30  # each block is a 20x20 square
    map_shape = (2, 1)
    blocks = []

    blocks.append(Water(blocksize, (0, 0)))
    blocks.append(Earth(blocksize, (0, blocksize)))

    blocks[0].add_item(Tree((10, 10), 3))
    blocks[0].add_item(Tree((5, 15), 3))
    blocks[1].add_item(House((12, 6), 5))

    # handler to draw temp grip
    def update_temp_plot():
        for block in blocks:
            temps = block.get_item_temps()
            for temp in temps:

                ax[1].plot(
                    temp["temp"],
                    label=temp["id"],
                    color=cm.hot(Normalize(0, 50)(temp["col"])),
                )
                ax[1].set_xlabel("Timestep")
                ax[1].set_ylabel("Temperature")

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

    plt.show()


if __name__ == "__main__":
    main()
