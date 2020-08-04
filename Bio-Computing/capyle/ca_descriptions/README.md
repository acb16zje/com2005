# Team 11 Forest Fire Simulation
### ZerJun Eng, Grace JiaMei Lim, James Evans, Oliver Long


## Constant Variables
### Terrain colour
1. CHAPARRAL
    * Colour for chaparral (greenish yellow)
2. GRASSLAND
    * Colour for grassland / scrubland (grey)
3. FOREST
    * Colour for dense forest (dark green)
4. LAKE
    * Colour for lake (blue)
5. HIGH_FIRE
    * Colour for high intensity fire (dark red)
6. MED_FIRE
    * Colour for medium intensity fire (lighter red)
7. LOW_FIRE
    * Colour for low intensity fire (orange)
8. DEAD
    * Colour for burnt cell (black)
9. TOWN
    * Colour for town (white)


### Timescale and Burning Duration
The timescale is set as 500 time steps as 5 days.
1. TIMESCALE = 1500
    * 500 time steps as 5 days, has to set 1500 as default for fire starting at incinerator to reach the town
2. CHAPARRAL_DURATION = 350
    * 3.5 days
3. GRASSLAND_DURATION = 21
    * 5 hours
4. FOREST_DURATION = 15000
    * 1 month


### Base ignition probability for terrain
1. BASE_CHAPARRAL = 0.4
    * 40% base chance for the chaparral to ignite if it has a burning neighbour
2. BASE_GRASSLAND = 0.8
    * 80% base chance for the grassland to ignite if it has a burning neighbour
3. BASE_FOREST = 0.0387
    * 3.87% base chance for the forest to ignite if it has a burning neighbour


### Wind Speed and Direction
1. Wind direction
    * The wind direction is set as SOUTH by default. Change the `SOUTH` in `wind_direction =
      Direction.SOUTH` to `NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTHWEST, WEST, NORTHWEST` or
      `wind_direction = None` for no wind direction.

2. Wind speed
    * The neighbour cells are splitted into 5 states
        * Positive parallel
            * Top neighbour of the centre cell
        * Negative parallel
            * Botton neighbour of the centre cell
        * Perpendicular sides
            * Left and Right neighbour of the centre cell
        * Positive corner slope
            * Top corners of the centre cell
        * Negative corner slope
            * Bottom corners of the centre cell
    * Change the value of `a` and `b` in `random.uniform(a, b)` to adjust the wind speed


### Fire starting point
Comment or uncomment one of `config.initial_grid[0][0] = 4  # Power plant` or
`config.initial_grid[0][-1] = 4 # proposed incinerator` in the `def setup(args)` function to change
the fire starting point