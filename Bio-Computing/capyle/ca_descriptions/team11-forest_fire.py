# Name: Forest Fire Simulation
# Dimensions: 2

import inspect
# --- Set up executable path, do not edit ---
import sys

this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# --------------------------------------------
from capyle.ca import Grid2D
import capyle.utils as utils
import numpy as np
import random
from enum import Enum


class Direction(Enum):
    NORTHWEST = 1
    NORTH = 2
    NORTHEAST = 3
    WEST = 4
    EAST = 5
    SOUTHWEST = 6
    SOUTH = 7
    SOUTHEAST = 8

# Terrain colour
CHAPARRAL = (0.749, 0.741, 0.003)  # 0
GRASSLAND = (0.498, 0.482, 0.529)  # 1
FOREST = (0.102, 0.298, 0.110)  # 2
LAKE = (0.223, 0.454, 0.733)  # 3
HIGH_FIRE = (0.718, 0.055, 0.055)  # 4
MED_FIRE = (0.882, 0.196, 0.196)  # 5
LOW_FIRE = (0.969, 0.4, 0.212)  # 6
DEAD = (0, 0, 0)  # 7
TOWN = (1, 1, 1)  # 8

# Number of generations, 5 days = 500 steps
TIMESCALE = 1500

# Grid size
GRID = (200, 200)

# Burning duration
CHAPARRAL_DURATION = 350  # 3.5 days
GRASSLAND_DURATION = 21  # 5 hours
FOREST_DURATION = 15000  # 1 month

# Base ignition probability
BASE_CHAPARRAL = 0.4
BASE_GRASSLAND = 0.8
BASE_FOREST = 0.0387


def rand(direction):
    """
    Generate the probability for the current cell affected by the
    fire around it. The probability depends on the fire direction
    with respect to the current cell

    :param direction: The direction of fire
    :return: The generated probability
    """

    # No wind, side fire
    if direction == 'side':
        return random.uniform(0.4, 0.6)

    # No wind, corner fire
    elif direction == 'corner':
        return random.uniform(0.187, 0.269)

    # Wind, side perpendicular
    elif direction == 'w_pp_side':
        return random.uniform(0.04, 0.09)

    # Wind, positive parallel
    elif direction == 'w_ppar':
        return random.uniform(0.92, 1.1)

    # Wind, negative parallel
    elif direction == 'w_npar':
        return random.uniform(0.01, 0.05)

    # Wind, corner positive slope
    elif direction == 'w_ps_corner':
        return random.uniform(0.5, 0.65)

    # Wind, corner negative slope
    elif direction == 'w_ns_corner':
        return random.uniform(0.02, 0.06)


def transition_func(grid, neighbourstates, neighbourcounts, terrain_map, decaygrid):
    """
    The transition function required to be calculated for each generation

    :param grid: The grid which display the current state
    :param neighbourstates: The neighbourstates of a cell
    :param neighbourcounts: The neighbourcounts of a cell
    :param terrain_map: The original terrain map for the grid
    :param decaygrid: The array storing the burning duration left
    :return: The new grid for next generation
    """

    # States of the neighbours of each cell
    NW, N, NE, W, E, SW, S, SE = neighbourstates

    # Set the wind direction
    wind_direction = Direction.SOUTH

    med_penalty = 0.5
    low_penalty = 0.29

    # Set the fire bonus and their probability based on the wind direction
    if wind_direction is None:
        fire_bonus = ((N == 4) | (E == 4) | (S == 4) | (W == 4) |
                      (N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (N == 6) | (E == 6) | (S == 6) | (W == 6)) * rand('side') + \
                     ((NE == 4) | (SE == 4) | (SW == 4) | (NW == 4) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * rand('corner') + \
                     ((N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5)) * med_penalty + \
                     ((N == 6) | (E == 6) | (S == 6) | (W == 6) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * low_penalty

    elif wind_direction == Direction.NORTH:
        fire_bonus = ((S == 4) | (S == 5) | (S == 6)) * rand('w_ppar') + \
                     ((E == 4) | (W == 4) | (E == 5) | (W == 5) | (E == 6) | (W == 6)) *rand('w_pp_side') + \
                     ((N == 4) | (N == 5) | (N == 6)) *rand('w_npar') + \
                     ((NE == 4) | (NW == 4) | (NE == 5) | (NW == 5) | (NE == 6) | (NW == 6)) * rand('w_ns_corner') + \
                     ((SE == 4) | (SW == 4) | (SE == 5) | (SW == 5) | (SE == 6) | (SW == 6)) * rand('w_ps_corner') + \
                     ((N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5)) * med_penalty + \
                     ((N == 6) | (E == 6) | (S == 6) | (W == 6) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * low_penalty

    elif wind_direction == Direction.NORTHEAST:
        fire_bonus = ((SW == 4) | (SW == 5) | (SW == 6)) * rand('w_ppar') + \
                     ((SE == 4) | (NW == 4) | (SE == 5) | (NW == 5) | (SE == 6) | (NW == 6)) *rand('w_pp_side') + \
                     ((NE == 4) | (NE == 5) | (NE == 6)) *rand('w_npar') + \
                     ((W == 4) | (S == 4) | (W == 5) | (S == 5) | (W == 6) | (S == 6)) * rand('w_ps_corner') + \
                     ((N == 4) | (E == 4) | (N == 5) | (E == 5) | (N == 6) | (E == 6)) * rand('w_ns_corner') + \
                     ((N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5)) * med_penalty + \
                     ((N == 6) | (E == 6) | (S == 6) | (W == 6) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * low_penalty
    elif wind_direction == Direction.EAST:
        fire_bonus = ((W == 4) | (W == 5) | (W == 6)) * rand('w_ppar') + \
                     ((N == 4) | (S == 4) | (N == 5) | (S == 5) | (N == 6) | (S == 6)) *rand('w_pp_side') + \
                     ((E == 4) | (E == 5) | (E == 6)) *rand('w_npar') + \
                     ((NW == 4) | (SW == 4) | (NW == 5) | (SW == 5) | (NW == 6) | (SW == 6)) * rand('w_ps_corner') + \
                     ((SE == 4) | (NE == 4) | (SE == 5) | (NE == 5) | (SE == 6) | (NE == 6)) * rand('w_ns_corner') + \
                     ((N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5)) * med_penalty + \
                     ((N == 6) | (E == 6) | (S == 6) | (W == 6) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * low_penalty
    elif wind_direction == Direction.SOUTHEAST:
        fire_bonus = ((SE == 4) | (SE == 5) | (SE == 6)) * rand('w_npar') + \
                     ((NE == 4) | (SW == 4) | (NE == 5) | (SW == 5) | (NE == 6) | (SW == 6)) *rand('w_pp_side') + \
                     ((NW == 4) | (NW == 5) | (NW == 6)) *rand('w_ppar') + \
                     ((E == 4) | (S == 4) | (E == 5) | (S == 5) | (E == 6) | (S == 6)) * rand('w_ns_corner') + \
                     ((N == 4) | (W == 4) | (N == 5) | (W == 5) | (N == 6) | (W == 6)) * rand('w_ps_corner') + \
                     ((N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5)) * med_penalty + \
                     ((N == 6) | (E == 6) | (S == 6) | (W == 6) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * low_penalty
    elif wind_direction == Direction.SOUTH:
        fire_bonus = ((N == 4) | (N == 5) | (N == 6)) * rand('w_ppar') + \
                     ((E == 4) | (W == 4) | (E == 5) | (W == 5) | (E == 6) | (W == 6)) *rand('w_pp_side') + \
                     ((S == 4) | (S == 5) | (S == 6)) *rand('w_npar') + \
                     ((NE == 4) | (NW == 4) | (NE == 5) | (NW == 5) | (NE == 6) | (NW == 6)) * rand('w_ps_corner') + \
                     ((SE == 4) | (SW == 4) | (SE == 5) | (SW == 5) | (SE == 6) | (SW == 6)) * rand('w_ns_corner') + \
                     ((N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5)) * med_penalty + \
                     ((N == 6) | (E == 6) | (S == 6) | (W == 6) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * low_penalty
    elif wind_direction == Direction.SOUTHWEST:
        fire_bonus = ((NE == 4) | (NE == 5) | (NE == 6)) * rand('w_ppar') + \
                     ((SE == 4) | (NW == 4) | (SE == 5) | (NW == 5) | (SE == 6) | (NW == 6)) *rand('w_pp_side') + \
                     ((SW == 4) | (SW == 5) | (SW == 6)) *rand('w_npar') + \
                     ((E == 4) | (N == 4) | (E == 5) | (N == 5) | (E == 6) | (N == 6)) * rand('w_ps_corner') + \
                     ((S == 4) | (W == 4) | (S == 5) | (W == 5) | (S == 6) | (W == 6)) * rand('w_ns_corner') + \
                     ((N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5)) * med_penalty + \
                     ((N == 6) | (E == 6) | (S == 6) | (W == 6) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * low_penalty
    elif wind_direction == Direction.WEST:
        fire_bonus = ((E == 4) | (E == 5) | (E == 6)) * rand('w_ppar') + \
                     ((N == 4) | (S == 4) | (N == 5) | (S == 5) | (N == 6) | (S == 6)) *rand('w_pp_side') + \
                     ((W == 4) | (W == 5) | (W == 6)) *rand('w_npar') + \
                     ((NE == 4) | (SE == 4) | (NE == 5) | (SE == 5) | (NE == 6) | (SE == 6)) * rand('w_ps_corner') + \
                     ((NW == 4) | (SW == 4) | (NW == 5) | (SW == 5) | (NW == 6) | (SW == 6)) * rand('w_ns_corner') + \
                     ((N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5)) * med_penalty + \
                     ((N == 6) | (E == 6) | (S == 6) | (W == 6) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * low_penalty
    elif wind_direction == Direction.NORTHWEST:
        fire_bonus = ((SE == 4) | (SE == 5) | (SE == 6)) * rand('w_ppar') + \
                     ((NE == 4) | (SW == 4) | (NE == 5) | (SW == 5) | (NE == 6) | (SW == 6)) *rand('w_pp_side') + \
                     ((NW == 4) | (NW == 5) | (NW == 6)) *rand('w_npar') + \
                     ((E == 4) | (S == 4) | (E == 5) | (S == 5) | (E == 6) | (S == 6)) * rand('w_ps_corner') + \
                     ((N == 4) | (W == 4) | (N == 5) | (W == 5) | (N == 6) | (W == 6)) * rand('w_ns_corner') + \
                     ((N == 5) | (E == 5) | (S == 5) | (W == 5) |
                      (NE == 5) | (SE == 5) | (SW == 5) | (NW == 5)) * med_penalty + \
                     ((N == 6) | (E == 6) | (S == 6) | (W == 6) |
                      (NE == 6) | (SE == 6) | (SW == 6) | (NW == 6)) * low_penalty

    # Probability of fire starting
    chaparral_chance = BASE_CHAPARRAL * fire_bonus * np.random.rand(GRID[0], GRID[1])
    grassland_chance = BASE_GRASSLAND * fire_bonus * np.random.rand(GRID[0], GRID[1])
    forest_chance = BASE_FOREST * fire_bonus * np.random.rand(GRID[0], GRID[1])

    willChaparralBurn = random.uniform(0, 1) < chaparral_chance
    willGrasslandBurn = random.uniform(0, 1) < grassland_chance
    willForestBurn = random.uniform(0, 1.5) < forest_chance

    # If a cell is not on fire, and it currently has neighbours burning, and it is not a lake
    # then it will burn with a chance depends on its terrain type
    chaparral_burn = (grid == 0) & willChaparralBurn
    grassland_burn = (grid == 1) & willGrasslandBurn
    forest_burn = (grid == 2) & willForestBurn

    # set squares on fire
    grid[chaparral_burn | grassland_burn | forest_burn] = 4

    # setup decay grids for burning tiles to track how long they have been alive
    # when the time limit is reached set them to burnt (dead) tiles
    burning_cells = (grid == 4) | (grid == 5) | (grid == 6)
    decaygrid[burning_cells] -= 1
    decaygrid[chaparral_burn] = CHAPARRAL_DURATION
    decaygrid[grassland_burn] = GRASSLAND_DURATION
    decaygrid[forest_burn] = FOREST_DURATION

    # Change the state of burning terrain based on their decay status
    grid[(decaygrid < CHAPARRAL_DURATION / 2) & (terrain_map == 0) |
         (decaygrid < GRASSLAND_DURATION / 2) & (terrain_map == 1) |
         (decaygrid < FOREST_DURATION / 2) & (terrain_map == 2) & (grid == 4)] = 5
    grid[(decaygrid < CHAPARRAL_DURATION / 3.4) & (terrain_map == 0) |
         (decaygrid < GRASSLAND_DURATION / 3.4) & (terrain_map == 1) |
         (decaygrid < FOREST_DURATION / 3.25) & (terrain_map == 2) & (grid == 5)] = 6
    grid[decaygrid == 0] = 7

    return grid


def setup(args):
    """
    Set up the cellular automata model

    :param args: The path of the config
    :return: The configuration
    """

    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest Fire Simulation"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [CHAPARRAL, GRASSLAND, FOREST, LAKE, HIGH_FIRE, MED_FIRE, LOW_FIRE, DEAD, TOWN]
    config.initial_grid = np.zeros(GRID)

    # Grassland setup
    config.initial_grid[20:140, 130:140] = 1

    # Forest setup
    config.initial_grid[120:160, 60:100] = 2

    # Lake setup
    config.initial_grid[40:60, 20:60] = 3

    # Short-term intervention water
    # config.initial_grid[85:98, 50:63] = 3

    # Long-term intervention forest
    # config.initial_grid[120:160, 40:60] = 2
    # config.initial_grid[160:170, 60:100] = 2
    # config.initial_grid[80:120, 60:100] = 2

    # Town setup
    config.initial_grid[195:200, 0:10] = 8

    # Fire setup
    config.initial_grid[0][0] = 4  # Power plant
    # config.initial_grid[0][-1] = 4 # proposed incinerator

    config.grid_dims = GRID
    config.num_generations = TIMESCALE
    config.wrap = False

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    """
    The main function

    :return: None
    """

    # Open the config object
    config = setup(sys.argv[1:])

    # Set the default burning duration as Chaparral burning duration
    decaygrid = np.zeros(config.grid_dims)
    decaygrid.fill(CHAPARRAL_DURATION)

    grid = Grid2D(config, (transition_func, config.initial_grid, decaygrid))

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
