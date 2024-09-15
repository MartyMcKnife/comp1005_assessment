## Block

- Represents the background
- Should be influenced by surrounding thermal values, but the RGB value is just a default value
- Will have a thermal coeff to govern how much it absorbs heat

## Item

- Will have a base class, each element is instantiated from it
- Contains thermal calculations, rgb calculations
- Thermal calculation will be another thermal coeff, but will be a bit more complex

## Map

- Basically just the matplotlib grid

Needs 6 features for full marks:

- Simulation step through
- heatmap
- rgb
- water, terrain and animals objects
- input file and command line parsing
- variation in blocks

Needs 6 bonus features for extra marks

- output simulation to csv
- click through simulation in matplotlib?
- uhhh idk see how we go
- try to implement rgb view on heat view cause that would be pretty cool
