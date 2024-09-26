# COMP1005 Assessment

## About

Created for COMP1005 Assessment. This program creates both an RGB and Heatmap simulation of various objects. A line plot is created of the average item temperature. The ongoing heat simulation is stored to both image outputs and recorded in a CSV file for further processing

## Dependencies

- `matplotlib`
- `numpy`

## Usage

Inside the directory there are two configuration files: `config.ini` and `input.csv`

`config.ini` contains the broad simulation settings

##### Simulation Settings

- **Resolution** defines the pixel density of each Block. Default is 30
- **Rows** define how many rows are in each simultion. The program will automatically size the required columns for the amount of blocks in `input.csv`. Default is 2

##### Intial Temps

These values define the intial temperatures for each item

##### Thermal Coeffs

These values define the thermal coefficient of each item

`input.csv` contains the definition for how the map works.
_Please ensure that any blocks are defined before any items_

#### Defining blocks

Pass in the data in the following order:
`id, block, type`
Where

- **id** is any non zero integer
- **type** type is a list of valid block types (see below)

##### Valid Block Types

- Water
- Earth
- Dirt
- Ice
- Parkland

#### Defining items

Pass in the data in the following order:
`id, item, type, size, x_pos, y_pos, owned_by`
Where

- **id** is any non zero integer
- **type** is a list of valid item types (see below)
- **size** is an integer value for the size of the item (this cannot exceed the resolution of the block as defined in `config.ini`)
- **x_pos** is an integer value between 0 and the block resolution defined in `config.ini`
- **y_pos** is an integer value between 0 and the block resolution defined in `config.ini`
- **owned_by** is a integer value that maps to a block id that the item will sit on
